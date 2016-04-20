import threading
import socket
from serverHelper import *
from message import Message

class Server(object):

    def __init__(self, sid):
        self.sid = sid
        self.clock = 0
        self.n = int(getConfiguration("GeneralConfig", "nodes"))
        # log: list of lists. Each list corresponds to each node
        self.log = [[] for i in range(self.n)]
        self.timeTable = [[0 for i in range(self.n)] for i in range(self.n)]
        self.peers = initialize(self.sid, self.n)
        # New server socket to listen to requests from Client/Peers
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSock.bind((getServer("Server" + str(self.sid))))
        self.serverSock.listen(128)

    # Crux of server functionality. Main logic goes here
    def requestHandler(self, connection, address):
        print "New Thread..."

        msg = receiveObject(connection)
    
        if msg.operation == "post":
            # Increment clock and Insert in respective log
            self.clock += 1
            self.log[self.sid].append((self.clock, msg.blog))
            self.timeTable[self.sid][self.sid] += 1
            # TODO: Update blog to persistent storage
            print self.log
            print self.timeTable

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
        s = Server(1)
        print s.sid
        print s.n
        print s.peers
        print s.log
        print s.timeTable
        s.start()
    except Exception as details:
        print details
        s.serverSock.close()

