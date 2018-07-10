import netifaces #pip3 install netifaces


def get_address(addresses, protocol):
    address = ""
    try:
        address = addresses[protocol][0]["addr"]
    except:
        #we can output message that address is missing if required
        pass
    return address


print("Device, IPv4, IPv6")
for device in netifaces.interfaces():
    addresses = netifaces.ifaddresses(device)

    ipv4_address = get_address(addresses, netifaces.AF_INET)
    ipv6_address = get_address(addresses, netifaces.AF_INET6)

    device_info = ",".join([device, ipv4_address, ipv6_address])
    print(device_info)