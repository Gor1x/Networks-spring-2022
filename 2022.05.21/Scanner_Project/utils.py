import socket

HOME_IP = '192.168.43.6'
NETWORK_IP = '192.168.43.0'
HOME_MAC = '64-5D-86-86-5B-64'
HOME_HOST_NAME = socket.gethostbyaddr(HOME_IP)[0]
MASK = [255, 255, 255, 0]
