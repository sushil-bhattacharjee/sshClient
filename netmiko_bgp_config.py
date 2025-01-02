import yaml
from netmiko import ConnectHandler
from rich import print

# Load variables from the YAML file
with open("ospf_bgp_config.yml", "r") as file:
    config = yaml.safe_load(file)

# Define the target router IP
target_router_ip = "10.1.10.12"  # Replace with your target router's IP

# Filter routers to match the target IP and ensure BGP is configured
routers = [router for router in config["routers"] if router["ip"] == target_router_ip and "bgp" in router]

if not routers:
    print(f"No router with BGP configuration found for IP: {target_router_ip}")
else:
    for router in routers:
        router_ip = router["ip"]
        username = router["username"]
        password = router["password"]
        enable_password = router.get("enable_password", None)
        bgp = router["bgp"]

        # Build connection details for Netmiko
        connection_params = {
            "device_type": "cisco_ios",
            "host": router_ip,
            "username": username,
            "password": password,
            "secret": enable_password,
        }

        try:
            print(f"Connecting to {router_ip}...")
            connection = ConnectHandler(**connection_params)
            connection.enable()

            # Build BGP configuration commands
            bgp_commands = [
                f"router bgp {bgp['process_id']}",
                f"bgp router-id {bgp['router_id']}",
            ]
            if bgp.get("log_neighbor_changes", False):
                bgp_commands.append("bgp log-neighbor-changes")
            for neighbor in bgp["neighbors"]:
                bgp_commands.append(f"neighbor {neighbor['remote_ip']} remote-as {neighbor['remote_as']}")
                bgp_commands.append(f"neighbor {neighbor['remote_ip']} update-source {neighbor['update_source']}")

            # Send BGP configuration commands
            print(f"Configuring BGP on {router_ip}...")
            output = connection.send_config_set(bgp_commands)
            print(output)

            # Save the configuration
            print("Saving configuration...")
            save_output = connection.save_config()
            print(save_output)

            # Close the connection
            connection.disconnect()
            print(f"Configuration complete and connection closed for {router_ip}.")

        except Exception as e:
            print(f"An error occurred for {router_ip}: {e}")
