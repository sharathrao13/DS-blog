import threading
import socket
from message import Message
from config_reader import ConfigReader
from network_interface import sendObject, receiveObject


class Server(object):
    def __init__(self):

        config_reader = ConfigReader('../config.ini')
        self.clock = 0

        # Config information
        self.current_server_id = int(config_reader.getConfiguration("CurrentServer", "sid"))
        self.total_nodes = int(config_reader.getConfiguration("GeneralConfig", "nodes"))
        self.peers = config_reader.get_peer_servers(self.current_server_id, self.total_nodes)

        # log: Each list corresponds to each node
        self.log = list()
        self.timeTable = [[0 for i in range(self.total_nodes)] for i in range(self.total_nodes)]

        # Blogs at this server
        self.blogs = list()

        # New server socket to listen to requests from Client/Peers
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSock.bind((config_reader.get_ip_and_port_of_server("Server" + str(self.current_server_id))))
        self.serverSock.listen(128)

    # Crux of server functionality. Main logic goes here
    def requestHandler(self, server_socket, address):

        print "New Thread..."

        msg = receiveObject(server_socket)

        if "post" == msg.operation:
            # Increment clock and Insert in respective log
            self.clock += 1
            self.log[self.current_server_id].append((self.clock, msg.blog))
            self.timeTable[self.current_server_id][self.current_server_id] += 1
            self.blogs.append(msg.blog)

            print "Log: %s" % self.log
            print "TT: %s" % self.timeTable
            print "Msg: %s" % msg
            print "Clock: %s" % self.clock

        elif "lookup" == msg.operation:
            sendObject(server_socket, self.blogs)
            print "Log: %s" % self.log
            print "TT: %s" % self.timeTable
            print "Msg: %s" % msg
            print "Clock: %s" % self.clock

        # Client sends the message sync so that the given server syncs with the given parameter
        elif "sync" == msg.operation:

            # all the entries where hasRec is false
            filtered_log = self.filter_log(self.log, msg.server_to_sync)
            message = Message(operation="server_sync", timeTable=self.timeTable, logs=filtered_log,
                              sent_server_id=self.current_server_id)

            sock_to_other = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_to_other.connect(self.config_reader.get_ip_and_port_of_server("Server" + msg.server_to_sync))
            sendObject(sock_to_other, message)
            sock_to_other.close()

            print "Filtered Log: %s" % self.filtered_log
            print "TT: %s" % self.timeTable
            print "Msg: %s" % msg
            print "Clock: %s" % self.clock

        # Received from a server. Update the logs and sync servers to complete replication
        elif "server_sync" == msg.operation:

            sent_server = msg.sent_server_id
            other_log = msg.logs
            other_time_table = msg.timeTable

            self.add_new_events_to_log_and_blog(other_time_table, other_log)
            self.update_max_elements(other_time_table)
            self.update_rows(other_time_table, sent_server)


            print "Log: %s" % self.log
            print "TT: %s" % self.timeTable
            print "Msg: %s" % msg
            print "Clock: %s" % self.clock

        else:
            print "Received an unknown operation %s" % msg.operation

        server_socket.close()

    def start(self):
        # Start listening for incoming requests
        while True:
            connection, address = self.serverSock.accept()
            threading.Thread(target=self.requestHandler, args=(connection, address)).start()

    def filter_log(self, log, server_id):
        pass

    def update_max_elements(self, other_time_table):
        for i in range(0, self.total_nodes):
            for j in range(0, self.total_nodes):
                self.timeTable[i][j] = max(self.timeTable[i][j], other_time_table[i][j])

    def update_rows(self, other_time_table, sent_server):
        for i in range(0, self.total_nodes):
            self.timeTable[self.current_server_id][i] = max(self.timeTable[self.current_server_id][i],
                                                            other_time_table[sent_server][i])

    def has_rec(self, server_to_send):
        # TT[i][k] = t => Site i knows that event k took place at latest of time t
        return self.timeTable[self.current_server_id][server_to_send] > time(e)

    def add_new_events_to_log_and_blog(self, other_time_table, other_log):
        #Add to Log
        #Add to Dictionary
        pass


if __name__ == "__main__":

    try:
        current_server = Server()
        print "Starting server %s (of total %s) with peers %s" % (
            current_server.current_server_id, current_server.total_nodes, current_server.peers)
        current_server.start()

    except Exception as details:
        print details
        current_server.serverSock.close()
