import datetime
import time
import socket


def create_client_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.0)
    return sock


def build_message(ping_index: int) -> bytes:
    cur_time = datetime.datetime.now().strftime('%H:%M:%S.%f')
    return f'Ping {ping_index} {cur_time}'.encode()


class RttStatistics:
    def __init__(self):
        self.min_rtt = None
        self.max_rtt = None
        self.sum_rtt = 0
        self.count_all = 0
        self.count_lost = 0

    def add_rtt(self, rtt):
        if self.min_rtt is None:
            self.min_rtt = rtt
        if self.max_rtt is None:
            self.max_rtt = rtt
        self.max_rtt = max(self.max_rtt, rtt)
        self.min_rtt = min(self.min_rtt, rtt)
        self.sum_rtt += rtt
        self.count_all += 1

    def add_lost_package(self):
        self.count_lost += 1
        self.count_all += 1

    def get_average_rtt(self):
        return self.sum_rtt // self.count_all

    def print_package_loss(self):
        print(
            f"Package sent {self.count_all}, package got {self.count_all - self.count_lost}, package lost {self.count_lost}\n"
            f"Loss percent is about {int(self.count_lost / self.count_all * 100)}%")


def message_output(param, stat):
    print(f'{param}\n'
          f'\tRTT in microseconds: Min - {stat.min_rtt}, Max - {stat.max_rtt}, Average - {stat.get_average_rtt()}')


def main():
    addr = ("127.0.0.1", 1337)
    client_socket = create_client_socket()
    stat = RttStatistics()
    for pings in range(10):
        message = build_message(pings)
        start_time = datetime.datetime.now()
        client_socket.sendto(message, addr)
        try:
            data, server = client_socket.recvfrom(1024)
            end_time = datetime.datetime.now()
            elapsed = (end_time - start_time).microseconds
            stat.add_rtt(elapsed)
            message_output(data.decode(), stat)
        except socket.timeout:
            stat.add_lost_package()
            print('Request timed out')
    print()
    stat.print_package_loss()


if __name__ == '__main__':
    main()
