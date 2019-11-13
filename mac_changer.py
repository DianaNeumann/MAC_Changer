#!/usr/bi/env python

import subprocess
import optparse
import re


def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="new MAC address")
    (values, agruments) = parser.parse_args()
    if not values.interface:
        parser.error("[-] Please specify an interface,use --help for more info")
    elif not values.new_mac:
        parser.error("[-] Please specify a mac,use --help for more info")

    return values
  
  
def change_mac(interface, new_mac):
    print("[+] Changing the mac address of " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    
    
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig",interface])
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_result.group(0):
        return mac_result.group(0)
    else:
        print("[-] Could not read MAC address")

values = get_args()
change_mac(values.interface, values.new_mac)
current_mac = get_current_mac(values.interface)
print(current_mac)
