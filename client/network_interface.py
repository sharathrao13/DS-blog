import cPickle as pickle
import socket
from config_reader import ConfigReader

class NetworkHandler:

    def __init__(self):
        self.config_reader = ConfigReader("../client_config.ini")
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def sendObject(self, obj, server_id):
        """
        Use this to send objects across dataCenters
        """

        server = "Server"+str(server_id)
        ip_and_port = self.config_reader.get_ip_and_port_of_server(server)

        self.client_sock.connect(ip_and_port)

        try:
            data = pickle.dumps(obj)
            self.client_sock.send(data)
        except Exception as details:
            print details
            return None

    def receiveObject(self):
        """
        Use this to receive objects across dataCenters
        """
        try:
            data = self.client_sock.recv(1024)
            obj = pickle.loads(data)
            return obj
        except Exception as details:
            print details
            return None