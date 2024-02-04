import socket
import pickle
#  192.168.1.26 | 9000


class Network:
    def __init__(self, address, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = address
        self.port = int(port)
        self.addr = (self.server, self.port)
        self.player_count = self.connect()

    def get_player_count(self):
        return self.player_count

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception as e:
            print(e)
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            #  data = pickle.loads(self.client.recv(4096))
            return pickle.loads(self.client.recv(9202))
        except socket.error as e:
            print(e)
