import cPickle as pickle

def sendObject(sock, obj):
    """
    Use this to send objects across dataCenters
    """
    try:    
        data = pickle.dumps(obj)
        sock.send(data)
    except Exception as details:
            print details
            return None

def receiveObject(sock):
    """
    Use this to receive objects across dataCenters
    """
    try:
        data = sock.recv(1024)
        obj = pickle.loads(data)
        return obj
    except Exception as details:
        print details
        return None
