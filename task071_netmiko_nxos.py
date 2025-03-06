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

