import paramiko
import yaml
import time

# Load variables from the YAML file
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

router_ip = config["router"]["ip"]
username = config["router"]["username"]
password = config["router"]["password"]
interface = config["interface"]["name"]
description = config["interface"]["description"]

try:
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the router
    print(f"Connecting to {router_ip}...")
    ssh_client.connect(hostname=router_ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    print(f"Successfully connected to {router_ip}")

    # Start an interactive shell session
    conn = ssh_client.invoke_shell()
    # time.sleep(1)
    output = conn.recv(1000).decode("utf-8")
    print(output)

    # Check if we are in User EXEC mode ('>')
    if ">" in output:
        conn.send("enable\n")
        output = conn.recv(1000).decode("utf-8")
        if "Password" in output:
            conn.send(password + "\n")
            output = conn.recv(1000).decode("utf-8")
        print(output)

    # Enter configuration mode
    conn.send("configure terminal\n")
    
    conn.recv(1000)

    # Configure the interface
    conn.send(f"interface {interface}\n")
    conn.send(f"description {description}\n")
    conn.send("end\n")

    # Save the configuration
    conn.send("write memory\n")
    time.sleep(2)
    output = conn.recv(5000).decode("utf-8")
    print(output)

    # Close the connection
    ssh_client.close()
    print("Configuration complete and connection closed.")

except paramiko.AuthenticationException:
    print("Authentication failed. Please check the username and password.")
except paramiko.SSHException as ssh_exception:
    print(f"SSH error: {ssh_exception}")
except Exception as e:
    print(f"An error occurred: {e}")

