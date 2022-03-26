import argparse
import base64
import ssl
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from socket import *

BUFFER_SIZE = 1024


class SMTPClient:
    _username = "testtesthomework@mail.ru"
    _mailfrom = "testtesthomework@mail.ru"
    _mailserv = "smtp.mail.ru"
    _mailport = 465
    _password = ""

    def _createTcpSocket(self):
        context = ssl.create_default_context()
        sock = context.wrap_socket(socket(AF_INET, SOCK_STREAM), server_hostname=self._mailserv)
        sock.connect((self._mailserv, self._mailport))
        result = sock.recv(2048)
        return sock

    def __init__(self):
        with open("passwordfile", "r") as f:
            self._password = f.read()
        self._sock = self._createTcpSocket()
        self._sendMessageToSocket("HELO testtesthomework\r\n", resultCode=250)
        self._sendMessageToSocket("AUTH LOGIN\r\n", resultCode=334)
        self._inputLogin()
        self._inputPassword()

    def _inputLogin(self):
        user64 = base64.b64encode(self._username.encode('utf-8'))
        self._sock.send(user64)
        self._sendMessageToSocket("\r\n", resultCode=334)

    def _inputPassword(self):
        password64 = base64.b64encode(self._password.encode('utf-8'))
        self._sock.send(password64)
        self._sendMessageToSocket("\r\n", resultCode=235)

    def _sendMessageToSocket(self, message, resultCode):
        self._sock.send(message.encode("utf-8"))
        response_code = self._sock.recv(2048).split()[0]
        if int(response_code) != resultCode:
            raise Exception(f"Got {response_code} instead of {resultCode} for message {message}")

    def sendEmail(self, emailto, file):
        msg = f'MAIL FROM: <{self._mailfrom}>\r\n'
        self._sendMessageToSocket(msg, 250)
        msg = f'RCPT TO: <{emailto}>\r\n'
        self._sendMessageToSocket(msg, 250)
        msg = 'DATA\r\n'
        self._sendMessageToSocket(msg, 354)
        self._sock.send(self._build_message(file, emailto))
        self._sendMessageToSocket("\r\n.\r\n", 250)

    def _build_message(self, file: str, mailrcpt: str):
        message = MIMEMultipart()
        message["Subject"] = "Homework 5 lab"
        message["From"] = self._mailfrom
        message["To"] = mailrcpt

        message_path = Path(file)

        if message_path.suffix == ".txt":
            with open(message_path, "r") as f:
                part = MIMEText(f.read(), "plain")
        elif message_path.suffix == ".html":
            with open(message_path, "r") as f:
                part = MIMEText(f.read(), "html")
        elif message_path.suffix in [".png", ".jpg"]:
            with open(message_path, "rb") as f:
                part = MIMEImage(f.read())
        else:
            raise RuntimeError("Wrong file format")

        # message.attach(MIMEText("This message is send via python smtp client. Egor Postnikov\r\n"))
        message.attach(part)

        return message.as_bytes()

    def endWork(self):
        self._sendMessageToSocket('QUIT\r\n', 221)
        self._sock.close()


def main(address, file):
    client = SMTPClient()
    client.sendEmail(address, file)
    client.endWork()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("address", type=str)
    parser.add_argument("file", type=str)
    args = parser.parse_args()

    main(args.address, args.file)
