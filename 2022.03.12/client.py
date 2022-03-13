import argparse
from datetime import datetime
from socket import *

import ServerParams
from ThreadPool import ThreadPool

BUFFER_SIZE = 1024


def readAllData(socket):
    message = []
    while True:
        chunk = socket.recv(BUFFER_SIZE)
        message.extend(chunk)
        if len(chunk) < BUFFER_SIZE:
            break

    return bytes(message).decode('utf-8')


def createTcpSocket(host=ServerParams.SERVER_NAME, port=ServerParams.SERVER_PORT):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    client_socket.setblocking(True)
    return client_socket


def testSendRequest(index, ans_filename):
    cl = 3 - index % 3
    filename = fr"C:\Users\Egor\Homeworks\Весенний семестр\Networks\2022.03.12\filesToCheck\lengthClass{cl}"
    result = sendRequest(filename, ServerParams.SERVER_NAME, ServerParams.SERVER_PORT)
    with open(ans_filename, 'w') as f:
        f.write(f"Length class of {cl}\n")
        f.write(str(index) + "\n")
        f.write(str(datetime.now().time()) + "\n")
        f.write(f"length of result is {len(result)}")


def sendRequest(filename, host, port):
    socket = createTcpSocket(host, port)
    socket.sendall(bytes(f'GET /"{filename}" HTTP/1.1\r\n\r\n', "utf-8"))
    response = readAllData(socket)
    socket.close()
    return response


def stressTesting():
    pool = ThreadPool(1000, testSendRequest)
    for i in range(300):
        pool.add_task(i, f"answers/task{i}")  # be careful with this amount of files!
    pool.start()
    pool.stop()


def main(host, port, filename):
    print(sendRequest(filename, host=host, port=port))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=str)
    parser.add_argument("port", type=int)
    parser.add_argument("filename", type=str)
    args = parser.parse_args()

    main(args.host, args.port, args.filename)
