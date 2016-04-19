import threading
import socket
from serverHelper import *
from message import Message

class Server(object):

    def __init__(self, sid):
        self.sid = sid
        self.clock = 0
        self.n = int(getConfiguration("GeneralConfig", "nodes"))
        self.peers = initialize(self.sid, self.n)
        # New server socket to listen to requests from Client/Peers
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSock.bind((getServer("Server" + str(self.sid))))
        self.serverSock.listen(5)

    # Crux of server functionality. Main logic goes here
    def requestHandler(self, connection, address):
        print "New Thread..."

        msg = receiveObject(connection)
    
        if msg.operation == "post":
            pass
        if msg.operation == "lookup":
            pass
        if msg.operation == "sync":
            pass

        connection.close()

    def start(self):
        # Start listening for incoming requests
        while True:
            connection, address = self.serverSock.accept()
            threading.Thread(target = self.requestHandler, args = (connection, address)).start()


if __name__ == "__main__":
    try:
        s = Server(2)
        print s.sid
        print s.n
        print s.peers
        s.start()
    except Exception as details:
        print details
        s.serverSock.close()

