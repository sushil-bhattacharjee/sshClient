from scrapli.driver.core import NXOSDriver
from dotenv import load_dotenv
import os
import json 

load_dotenv()

switch = NXOSDriver(
    host=os.getenv("SW2NXOS_HOST"),
    auth_username=os.getenv("SW_USER"),
    auth_password=os.getenv("SW_PASS"),
    auth_strict_key=False
)

switch.open()

output = switch.send_command("show interface brief")
print(output.result) # if print(output) it will show the object, but if print(output.result) it will show the result

parsed_output = output.textfsm_parse_output()
print(json.dumps(parsed_output, indent=2))

commands = [
    "interface mgmt0",
    "description Connection to the management switch"
    "Copy run start"
]

switch.send_configs(commands)
