from netmiko import ConnectHandler
from dotenv import load_dotenv
import os
import json
from ntc_templates.parse import parse_output
from rich import print
# Load environment variables from .env file
load_dotenv()

switch = ConnectHandler(
    device_type="cisco_nxos",
    host=os.getenv("SW2NXOS_HOST"),
    username=os.getenv("SW_USER"),
    password=os.getenv("SW_PASS"),
    session_log="router_session1.txt"
)

# Commands to be sent to the device
command1 = "show version"
command2 = "show vlan"

# Send the commands to the device
output1 = switch.send_command(command1)
output2 = switch.send_command(command2)

# Parse the output using the ntc-templates library
parsed_output1 = parse_output(platform="cisco_nxos", command="show version", data=output1)
parsed_output2 = parse_output(platform="cisco_nxos", command="show vlan", data=output2)

# Extract OS version
os_version = parsed_output1[0]["os"]
print(os_version)

# Extract VLAN information
for vlan in parsed_output2:
    print(vlan["vlan_id"] + " " + vlan["vlan_name"])

# Ask the user if they want to add or remove a VLAN
action = input("Do you want to add or remove a VLAN? (add/remove): ").strip().lower()
# Add a new VLAN

if action == "add":
    vlan_id = input("New VLAN ID: ").strip()
    vlan_name = input("New VLAN Name: ").strip()
    
    config_commands = [
        f"vlan {vlan_id}",
        f"name {vlan_name}"
    ]
    switch.send_config_set(config_commands)
    print(f"VLAN {vlan_id} has been added with the name {vlan_name}")
    
elif action == "remove":
    vlan_id = input("VLAN ID to remove: ").strip()
    config_commands = [
        f"no vlan {vlan_id}"
    ]
    switch.send_config_set(config_commands)
    print(f"VLAN {vlan_id} has been removed.")
else:
    print("Invalid action. Please enter 'add' or 'remove'.")
# Save the configuration
switch.save_config()
# Close the connection
switch.disconnect()
