from socket import *

import nmap3


def scan_ports(ip_addr, min_port=0, max_port=65535):
    print('List of available ports:')
    for port in range(min_port, max_port + 1):
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.settimeout(0.3)
        res = client_socket.connect_ex((ip_addr, port))
        if port % 10 == 0:
            print(port)
        if res == 0:
            client_socket.close()
            print(f"Open port: {port}")
            continue


def nmap_scanner(address):
    nmap = nmap3.NmapScanTechniques()
    result = nmap.nmap_ping_scan(address)
    return result


if __name__ == '__main__':
    address = input("IP address to scan: ")
    print(scan_ports(address))
