class Message(object):

    def __init__(self, operation, sent_server_id = -1, timeTable = None, logs = None, blog = None, syncServer = None):

        # Possible operations: post, lookup, sync
        self.operation = operation
        self.sent_server_id = sent_server_id
        self.timeTable = timeTable
        # logs can be a list of lists. Each list corresponding to a particular node
        self.logs = logs
        self.blog = blog
        # syncServer is the server id (integer)
        self.syncServer = syncServer

    def __repr__(self):
        return "Class: %s, Operation: %s, TimeTable: %s, Logs: %s" %(self.__class__.__name__, self.operation, self.timeTable, self.logs)
