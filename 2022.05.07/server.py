import cv2
import socket
import numpy as np

import asyncio


class CanvasServer:
    def __init__(self, color=(0, 255, 0), updateTime=30, canvasName="Server"):
        self.updateTime = updateTime
        self.img = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
        self.color = color
        self.canvasName = canvasName
        cv2.namedWindow(winname=self.canvasName)
        self.show()

    def show(self):
        cv2.imshow(self.canvasName, self.img)

    def drawLine(self, xFrom, yFrom, xTo, yTo):
        cv2.line(self.img, (xFrom, yFrom), (xTo, yTo), self.color, thickness=5)

    def destroy(self):
        cv2.destroyWindow(self.canvasName)

    def shouldStop(self):
        return cv2.waitKey(self.updateTime) == 27


class SocketServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(100)
        self.host = "127.0.0.1"
        self.port = 1337
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.conn, self.addr =  self.socket.accept()

    async def connect(self):
        return

    async def getData(self):
        return

    def getCoordinates(self):
        data = self.conn.recv(1024).decode()
        print("Info:", data)
        for info in data.split("."):
            strings = info.split()
            if len(strings) < 4:
                continue
            if strings[0] == "None":
                continue
            coordinates = list(map(int, strings))
            yield coordinates

    def close(self):
        self.conn.close()


def runServer():
    print("Start server")
    canvas = CanvasServer()
    sock = SocketServer()

    while True:
        canvas.show()
        if canvas.shouldStop():
            break
        for info in sock.getCoordinates():
            canvas.drawLine(*info)

    sock.close()
    canvas.destroy()


if __name__ == '__main__':
    runServer()
