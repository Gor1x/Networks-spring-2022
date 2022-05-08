import socket

import cv2
import numpy as np


class Canvas:
    def __init__(self, color=(0, 0, 255), movePointerCallback=None, updateTime=30, canvasName="Client"):
        self.img = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
        self.isDrawing = False
        self.color = color
        self.x = None
        self.y = None
        self.canvasName = canvasName
        self.drawingCallback = movePointerCallback
        self.updateTime = updateTime

        cv2.namedWindow(winname=self.canvasName)
        cv2.setMouseCallback(self.canvasName,
                             self._mouseCallback)

    def _mouseCallback(self, event, x, y, flags, param):
        self._movePointerTo(x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.isDrawing = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.isDrawing = False

    def _movePointerTo(self, x, y):
        if self.isDrawing:
            if self.drawingCallback is not None:
                self.drawingCallback(self.x, self.y, x, y)
            cv2.line(self.img, (self.x, self.y), (x, y), self.color, thickness=5)
        self.x = x
        self.y = y

    def show(self):
        cv2.imshow(self.canvasName, self.img)

    def destroy(self):
        cv2.destroyWindow(self.canvasName)

    def shouldStop(self):
        return cv2.waitKey(self.updateTime) == 27


class Socket:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 1337
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def sendCoordinates(self, xFrom, yFrom, xTo, yTo):
        self.socket.send(f'{xFrom} {yFrom} {xTo} {yTo}.'.encode())

    def close(self):
        self.socket.close()


def runClient():
    sock = Socket()
    canvas = Canvas(movePointerCallback=sock.sendCoordinates)
    while True:
        canvas.show()
        if canvas.shouldStop():
            break
    canvas.destroy()


if __name__ == '__main__':
    runClient()
