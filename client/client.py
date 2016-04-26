from message import Message
from network_interface import NetworkHandler
from config_reader import ConfigReader

# Send Request to nearest datacenter

class Client:
    def __init__(self):
        print "Initializing Client ..."
        #self.config_reader = ConfigReader("../client_config.ini")
        self.network_handler = NetworkHandler()


    def publish_post(self, blog, server_id):
        print "Publishing: "
        message = Message(operation="publish",blog = blog)
        self.network_handler.sendObject(message,server_id)

    def read_posts(self,server_id):
        print "Reading: "
        message = Message(operation="lookup")
        self.network_handler.sendObject(message,server_id)
        received_message = self.network_handler.receiveObject()
        print received_message.blog

    def sync_with_server(self, server_id):
        print "Syncing with server %s"%server_id
        message = Message(operation="sync")
        self.network_handler.sendObject(message,server_id)

    def start_console(self):
        print "Starting Client ..."

        total_servers = 3#int(self.config_reader.getConfiguration("GeneralConfig","nodes"))
        server_to_connect =-1

        while True:
            operation = int(
                raw_input("Enter the operation to run\n1.Publish a Blog\n2.Lookup "
                          "all Blogs\n3.Sync with Servers\n4.Connect to a Server"))
            if(operation == 1):
                blog = raw_input("Blog:")
                self.publish_post(blog, server_to_connect)
            elif(operation==2):
                posts = self.read_posts(server_to_connect)
                print posts
            elif (operation==3):
                server_id = int(raw_input("Which server do you want to sync with?"))
                self.sync_with_server(server_id)
            elif (operation==4):
                print"Server to connect to:\n"
                for i in range(total_servers):
                    print "%s.Server %s\n"%(i,i)
                server_to_connect = int(raw_input("Your choice:"))
                #self.connect(server_to_connect)
            else:
                print "Received incorrect option\n"

if __name__ == "__main__":

    try:
        client = Client()
        client.start_console()

    except Exception as details:
        print details

