import random
import socket
import time


def is_package_lost(percent: int) -> bool:
    return random.randint(0, 99) < percent


def create_server_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 1337))
    return sock


def main():
    server_socket = create_server_socket()
    print("Run server socket")
    while True:
        print("Waiting for connection")
        message, address = server_socket.recvfrom(1024)
        print(f"Connected to {address}")
        message = message.upper()
        #time.sleep(0.000001)  # Моделирование задержки
        if not is_package_lost(20):
            server_socket.sendto(message, address)


if __name__ == '__main__':
    main()
