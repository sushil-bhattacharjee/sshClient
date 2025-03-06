from netmiko import ConnectHandler
from dotenv import load_dotenv
import os
import json
from ntc_templates.parse import parse_output
from rich import print


# Load environment variables from .env file
load_dotenv()

router_coneection = ConnectHandler(
    device_type="cisco_ios",
    host=os.getenv("CE61_HOST"),
    username=os.getenv("ROUTER_USER"),
    password=os.getenv("ROUTER_PASS"),
    session_log="router_session1.txt"
)

output = router_coneection.send_command("show interfaces")

# convert the output to a list of lines
# for line in output.split("\n"):
#     if "Ethernet" in line or "address" in line:
#         print(line)

parsed_output = parse_output(platform="cisco_ios", command="show interfaces", data=output)
print(json.dumps(parsed_output, indent=2))

for intf in parsed_output:
    print(f"Interface: {intf['interface']}")
    print(f"IP Address: {intf['ip_address']}")
    print(f"MAC Address: {intf['mac_address']}")
    print(f"Description: {intf['description']}")
    print(f"MTU: {intf['mtu']}")

commands = [
    "interface GigabitEthernet1",
    "description Connection to the management switch"
]

router_coneection.send_config_set(commands) #Netmiko doesn't change the configuration in stratup (like scrapli does), 
                                            #it changes only in running config. Therefore, you need to save the 
                                            # configuration with the command below                                          
router_coneection.save_config() #This command saves the configuration in the startup config