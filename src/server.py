import threading
import socket
from message import Message
from config_reader import ConfigReader
from network_interface import NetworkHandler

class Server(object):

    def __init__(self):

        config_reader = ConfigReader('../config.ini')

        self.clock = 0

        #Config information
        self.current_server_id = int(config_reader.getConfiguration("CurrentServer", "sid"))
        self.total_nodes = int(config_reader.getConfiguration("GeneralConfig", "nodes"))
        self.peers = config_reader.get_peer_servers(self.current_server_id, self.total_nodes)

        # log: list of lists. Each list corresponds to each node
        self.log = [[] for i in range(self.total_nodes)]
        self.timeTable = [[0 for i in range(self.total_nodes)] for i in range(self.total_nodes)]

        # New server socket to listen to requests from Client/Peers

        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSock.bind((config_reader.get_ip_and_port_of_server("Server" + str(self.current_server_id))))
        self.serverSock.listen(128)
        self.networkHandler = NetworkHandler(self.serverSock)

    # Crux of server functionality. Main logic goes here
    def requestHandler(self, connection, address):

        print "New Thread..."

        msg = self.networkHandler.receiveObject(connection)
    
        if "post" == msg.opeation:
            # Increment clock and Insert in respective log
            self.clock += 1
            self.log[self.current_server_id].append((self.clock, msg.blog))
            self.timeTable[self.current_server_id][self.current_server_id] += 1
            # TODO: Update blog to persistent storage
            print self.log
            print self.timeTable
            print msg

        elif msg.operation == "lookup":
            print msg
        elif msg.operation == "sync":
            print msg
        else:
            print "Received an unknown operation %s"%msg.operation

        connection.close()

    def start(self):
        # Start listening for incoming requests
        while True:
            connection, address = self.serverSock.accept()
            threading.Thread(target = self.requestHandler, args = (connection, address)).start()


if __name__ == "__main__":

    try:
        current_server = Server()
        print "Starting server %s (of total %s) with peers %s"%(current_server.current_server_id, current_server.total_nodes, current_server.peers)
        current_server.start()

    except Exception as details:
        print details
        current_server.serverSock.close()

