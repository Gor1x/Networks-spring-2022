import datetime
import socket

import socket
from random import randint
from stop_and_wait import *


class StopAndWaitClient:
    def __init__(self, timeout=TIMEOUT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.timeout = timeout
        self.socket.settimeout(timeout)
        self.connection = None

    def connect_to(self, address):
        self.connection = address

    def _split_data_with_indexes(self, message, batch_size=DEFAULT_BATCH_SIZE) -> list:
        return [
            f"{i % 2}{message[i: i + batch_size]}".encode()
            for i in range(0, len(message), batch_size)
        ]

    def _send_one_message(self, message, index):
        while True:
            try:
                print(f"sending message {message}")
                self.socket.sendto(message, self.connection)
                ack, _ = self.socket.recvfrom(4)
                if randint(1, 3) == 1:
                    print("timeout")
                    raise socket.timeout()
                print(f"{ack.decode()}, {index}")
                if ack.decode() == f"ACK{index % 2}":
                    print("Has been received")
                    break
            except socket.timeout:
                continue
            except ConnectionResetError:
                break

    def send_message(self, full_message):
        self._send_one_message(f"1{str(len(full_message)).zfill(LENGTH_SIZE)}".encode(), 1)
        for index, message in enumerate(self._split_data_with_indexes(full_message)):
            # print(f"Sending {message}")
            self._send_one_message(message, index)


def main():
    connection = StopAndWaitClient()
    print("Connecting to host")
    connection.connect_to(("127.0.0.1", 1337))
    print("Sending the message")
    with open('example_file.txt', 'r') as f:
        connection.send_message(f"{f.read()}")


if __name__ == '__main__':
    main()
