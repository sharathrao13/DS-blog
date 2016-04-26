import cPickle as pickle

class NetworkHandler:

    def __init__(self, sock):
        self.sock = sock

    def sendObject(self, obj):
        """
        Use this to send objects across dataCenters
        """
        try:
            data = pickle.dumps(obj)
            self.sock.send(data)
        except Exception as details:
            print details
            return None

    def receiveObject(self, sock):
        """
        Use this to receive objects across dataCenters
        """
        try:
            data = self.sock.recv(1024)
            obj = pickle.loads(data)
            return obj
        except Exception as details:
            print details
            return None