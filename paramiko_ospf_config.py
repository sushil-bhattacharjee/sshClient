import paramiko
import yaml

# Load variables from the YAML file
with open("ospf_config.yml", "r") as file:
    config = yaml.safe_load(file)

# Filter the router for R3 (IP: 10.1.10.13)
target_router_ip = "10.1.10.13"  # Specify the target router IP
routers = [router for router in config["routers"] if router["ip"] == target_router_ip]

if not routers:
    print(f"No router found with IP: {target_router_ip}")
else:
    for router in routers:
        router_ip = router["ip"]
        username = router["username"]
        password = router["password"]
        ospf_process_id = router["ospf"]["process_id"]
        router_id = router["ospf"]["router_id"]
        networks = router["ospf"]["networks"]

        try:
            # Create a Transport (ConnectionHandler) object
            print(f"Connecting to {router_ip}...")
            transport = paramiko.Transport((router_ip, 22))
            transport.connect(username=username, password=password)
            print(f"Successfully connected to {router_ip}")

            # Open a session (channel) for communication
            channel = transport.open_session()
            channel.invoke_shell()

            def send_command(command, wait_for="#"):
                """Send a command and wait for the specified prompt."""
                channel.send(command + "\n")
                buffer = ""
                while not buffer.endswith(wait_for):
                    buffer += channel.recv(1024).decode("utf-8")
                return buffer

            # Send commands to configure OSPF
            print(send_command("enable", wait_for="#"))  # Enter privileged EXEC mode
            print(send_command("configure terminal", wait_for="(config)#"))  # Enter configuration mode
            print(send_command(f"router ospf {ospf_process_id}", wait_for="(config-router)#"))  # Start OSPF process
            print(send_command(f"router-id {router_id}", wait_for="(config-router)#"))  # Set router ID

            for network in networks:
                print(send_command(f"network {network}", wait_for="(config-router)#"))  # Configure OSPF networks

            print(send_command("exit", wait_for="(config)#"))  # Exit OSPF configuration mode
            print(send_command("do write memory", wait_for="#"))  # Save configuration

            # Close the channel and transport
            channel.close()
            transport.close()
            print(f"Configuration complete and connection closed for {router_ip}.")

        except paramiko.AuthenticationException:
            print(f"Authentication failed for {router_ip}. Please check the username and password.")
        except paramiko.SSHException as ssh_exception:
            print(f"SSH error for {router_ip}: {ssh_exception}")
        except Exception as e:
            print(f"An error occurred for {router_ip}: {e}")

