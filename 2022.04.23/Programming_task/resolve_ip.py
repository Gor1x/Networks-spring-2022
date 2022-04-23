import psutil


def resolve_address_port():
    address = psutil.net_if_addrs()
    for name, data in address.items():
        for item in data:
            if item.address.startswith("192.168"):
                return name, item.address, item.netmask
    return None


if __name__ == '__main__':
    data = resolve_address_port()
    if data is not None:
        name, address, port = data
        print(f"address: {address}, port: {port} with name {name}")
    else:
        print("Something went wrong")
