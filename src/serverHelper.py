import ConfigParser
import cPickle as pickle
"""
List of helper functions for server
"""

def getConfiguration(section, entry):
    """
    Parameters:
    section : section in [] in config.ini
    entry   : entry under correspoding section

    Gets configuration details defined in "config.ini" file
    After calling this function, check if None returned for exception and handle accordingly
    """
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    try:
        return config.get(section, entry)
    except Exception as details:
        print details
        return None

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
