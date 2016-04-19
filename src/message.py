class Message(object):

<<<<<<< HEAD
    def __init__(self, operation, sid = -1, timeTable = None, logEntries = None):
=======
    def __init__(self, operation, sid = -1, timeTable = None, logs = None):
>>>>>>> suraj1
        # Possible operations: post, lookup, sync
        self.operation = operation
        self.sid = sid
        self.timeTable = timeTable
<<<<<<< HEAD
        # Log entries can be list of lists. Each list corresponding to one server
        self.logEntries = logEntries
=======
        # logs can be a list of lists. Each list corresponding to a particular node
        self.logs = logs
>>>>>>> suraj1

    def __repr__(self):
        return "Class: %s, State: %s, TimeTable: %s, Blog: %s" %(self.__class__.__name__, self.state, self.timeTable, self.blog)
