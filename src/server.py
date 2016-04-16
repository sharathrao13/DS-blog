from serverHelper import *

class Server(object):

    def __init__(self, sid):
        self.sid = sid
        self.n = int(getConfiguration("GeneralConfig", "nodes"))
        self.peers = initialize(self.sid, self.n)

if __name__ == "__main__":
    s = Server(2)
    print s.sid
    print s.n
    print s.peers
