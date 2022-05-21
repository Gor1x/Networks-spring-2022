import PySimpleGUI as sg
from utils import *
import scapy.all as scapy


# noinspection PyBroadException
class GuiWindow:
    def __init__(self):
        sg.theme('DarkAmber')
        self.progress_bar_length = list(get_all_neighbours(f'{NETWORK_IP}/24'))
        self.layout = [
            [sg.Output(size=(150, 30), key='-OUTPUT-')],
            [sg.Submit('Scan')],
            [sg.ProgressBar(len(self.progress_bar_length), orientation='h', size=(54, 20), key='loading_progress_bar')],
        ]
        self.window = sg.Window('Net scanner', self.layout)

    def _startScan(self):
        self.window['-OUTPUT-'].update('')
        self._printLocalHostData()

        progress_bar = self.window['loading_progress_bar']
        for i, host in enumerate(get_all_neighbours(f'{NETWORK_IP}/24')):
            ip, mac_address = host['ip'], host['mac']
            if ip == HOME_IP:
                continue
            try:
                host_name = socket.gethostbyaddr(ip)[0]
            except Exception:
                host_name = 'Name not found'
            print(f'{str(ip):30}{str(mac_address):30}{str(host_name):30}')
            progress_bar.UpdateBar(i + 1)
        progress_bar.UpdateBar(len(self.progress_bar_length))

    def run(self):
        while True:
            event, values = self.window.read(timeout=100)

            if event in (None, 'Exit'):
                break

            if event == 'Scan':
                self._startScan()

    def close(self):
        self.window.close()

    @staticmethod
    def _printLocalHostData():
        print(f'{"IP адрес":30}{"MAC адрес":30}{"Имя хоста":30}')
        print('Этот компьютер:')
        print(f'{HOME_IP:30}{HOME_MAC:30}{HOME_HOST_NAME:30}')
        print('Локальная сеть:')


def get_all_neighbours(ip):
    for i in scapy.srp(
            scapy.Ether(dst='ff:ff:ff:ff:ff:ff') / scapy.ARP(pdst=ip),
            timeout=1,
            verbose=False)[0]:
        yield {
            'ip': i[1].psrc,
            'mac': i[1].hwsrc
        }


def main():
    window = GuiWindow()
    window.run()
    window.close()


if __name__ == '__main__':
    main()
