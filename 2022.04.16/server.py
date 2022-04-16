import random
import socket

from stop_and_wait import *


class StopAndWaitServer:
    def __init__(self, bind=('', 1337)):
        self._package_loss_percent = 30
        self.binds_to = bind
        self.socket = None
        self.bind(bind)

    def bind(self, binder=('', 1337)):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(binder)
        self.socket.settimeout(TIMEOUT)

    def _parse(self, data):
        data = data.decode()
        index = int(data[0])
        message = data[1:]
        return index, message

    def _read_message_length(self):
        while True:
            try:
                data_size = int(self._receive_info(LENGTH_SIZE + 1, 1))
                break
            except socket.timeout or ValueError:
                pass
        return data_size

    def _receive_info(self, length, index):
        data = None
        try:
            while True:
                print(f"Receiving info of length {length}")
                packet, address = self.socket.recvfrom(length)
                message_index, message = self._parse(packet)
                print(f"Got {packet}, index {index}")
                if randint(1, 3) == 1:
                    print("Packet lost")
                    raise socket.timeout()
                self.socket.sendto(f"ACK{message_index}".encode(), address)
                if message_index == index % 2:
                    data = message
                break
        except socket.timeout:
            raise
        print(f"Received {data}")
        return data

    def receive(self):
        data_size = self._read_message_length()
        current_index = 2
        received_data = ""
        while data_size > 0:
            print(f"Getting {data_size}")
            try:
                length = min(data_size + 1, MESSAGE_SIZE)
                message = self._receive_info(length, current_index)
                current_index += 1
                if message is not None:
                    received_data += message
                    data_size -= len(message)

            except socket.timeout:
                print('timed out')
                continue
        return received_data


def main():
    connection = StopAndWaitServer()
    print("Server started")

    print("Receiving")
    connection.bind()
    data = connection.receive()
    print(f"Full message is:\n{data}")


if __name__ == '__main__':
    main()
