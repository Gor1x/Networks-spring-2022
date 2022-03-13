import argparse
from pathlib import Path
from socket import *

from ThreadPool import ThreadPool


def error_response() -> bytes:
    response = f"HTTP/1.1 404 Not Found\r\n"
    return response.encode("utf-8")


def bad_request_response() -> bytes:
    response = f"HTTP/1.1 400 Bad Request\r\n"
    return response.encode("utf-8")


def processRequest(query: bytes) -> bytes:
    file = getFileFromQuery(query)
    if file is None:
        return bad_request_response()
    try:
        file.resolve(strict=True)
        with open(file, "r") as f:
            filedata = f.read()
            response_string = f"HTTP/1.1 200 OK\r\n" \
                              f"Content-Length: {len(filedata)}\r\n\r\n" \
                              f"{filedata}"
            return response_string.encode("utf-8")
    except Exception as e:
        return error_response()


def getFileFromQuery(query: bytes):
    str_query = query.decode("utf-8")
    headers = str_query.split("\n")
    filename_part = headers[0].strip().removeprefix("GET /").removesuffix("HTTP/1.1").strip()
    pos_from = filename_part.find('"')
    pos_to = filename_part.rfind('"')
    if pos_to == -1 or pos_from == -1 or pos_from == pos_to:
        return None
    path = Path(filename_part[pos_from + 1:pos_to])
    return path


def run_processing(connection_socket, addr):
    query = connection_socket.recv(1024)
    connection_socket.sendall(processRequest(query))
    connection_socket.close()
    print(f"{addr} end job")


def main(thread_count, port):
    pool = ThreadPool(thread_count, run_processing).start()
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen()
    # server_socket.setblocking(True)
    print('Waiting for connection')
    while True:
        connection_socket, addr = server_socket.accept()
        print(f"Addr {addr} connected")
        pool.add_task(connection_socket, addr)

    pool.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("max_threads", type=int, default=2)
    parser.add_argument("port", type=int)
    args = parser.parse_args()
    main(args.max_threads, args.port)
