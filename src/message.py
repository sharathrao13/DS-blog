class Message(object):

    def __init__(self, operation, sid = -1, timeTable = None, logEntries = None):
        # Possible operations: post, lookup, sync
        self.operation = operation
        self.sid = sid
        self.timeTable = timeTable
        # Log entries can be list of lists. Each list corresponding to one server
        self.logEntries = logEntries

    def __repr__(self):
        return "Class: %s, State: %s, TimeTable: %s, Blog: %s" %(self.__class__.__name__, self.state, self.timeTable, self.blog)
