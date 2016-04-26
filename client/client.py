import socket
from message import Message
from network_interface import sendObject, receiveObject
from config_reader import ConfigReader

class Client(object):

    def __init__(self):

        # Configuration
        self.config_reader = ConfigReader("../client_config.ini")
        self.total_servers = int(self.config_reader.getConfiguration("GeneralConfig", "nodes"))

    def publish_post(self, blog, server_id):

        # Create new socket
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(self.config_reader.get_ip_and_port_of_server("Server" + server_id))

        # Create and post the message
        message = Message(operation="post",blog = blog)
        sendObject(client_sock, message)

        # Close socket
        client_sock.close()

    def read_posts(self,server_id):
        
        # Create new socket
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(self.config_reader.get_ip_and_port_of_server("Server" + server_id))

        # Send "lookup" message
        message = Message(operation="lookup")
        sendObject(client_sock, message)

        # Receive blogs from server
        received_message = receiveObject(client_sock)

        # Close the socket
        client_sock.close()

        return received_message.blog

    def sync_with_server(self, server_id):
       
        while True:

            sync_server = int(raw_input("Which server do you want Server " + server_id + " to sync with ?\nServer range : (0 - " + str(self.total_servers - 1) + ")\nEnter server number: "))

            if ((sync_server == int(server_id)) or not ( 0 <= sync_server < self.total_servers)):
                print "Incorrect input. Please check"
                continue
            else:
                break

        # Create new socket
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(self.config_reader.get_ip_and_port_of_server("Server" + server_id))

        # Send "sync" message
        message = Message(operation="sync", syncServer = sync_server)
        sendObject(client_sock, message)

        # Close the socket
        client_sock.close()

    def start_console(self):
        
        while True:
            print "\nClient running..."
            print"\nChoose server to connect: \n"
            
            for i in range(self.total_servers):
                print "%s.Server %s"%(i,i)
            
            print "-1. Exit"

            server_to_connect = raw_input("\nYour choice: ")

            if (int(server_to_connect) == -1):
                break

            if not (0 <= int(server_to_connect) < self.total_servers):
                print "Incorrect choice..."
                continue


            operation = int(raw_input("\n\nEnter the operation to run: \n\n1. Post"
                        "Blog\n2. Lookup all Blogs\n3. Sync\n4. Exit"
                        "\n\nYour choice: "))

            if (operation == 1):
                blog = raw_input("Blog:")
                self.publish_post(blog, server_to_connect)

            elif (operation == 2):
                posts = self.read_posts(server_to_connect)
                print posts

            elif (operation == 3):
                self.sync_with_server(server_to_connect)

            elif (operation == 4):
                break
            else:
                print "Received incorrect option\n"

if __name__ == "__main__":

    try:
        client = Client()
        client.start_console()

    except Exception as details:
        print details

