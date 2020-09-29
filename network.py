import socket
import pickle

class Network:

    def __init__(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '51.178.84.118'
        self.port = 65432
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):

        return self.p

    def Connect(self):

        self.client.connect(self.addr)

        return self.client.recv(2048).decode()

    def Send(self, data):

        self.client.send(str.encode(data))

        return pickle.loads(self.client.recv(2048 * 2))