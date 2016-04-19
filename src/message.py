class Message(object):

    def __init__(self, operation, sid = -1, timeTable = None, logs = None):
        # Possible operations: post, lookup, sync
        self.operation = operation
        self.sid = sid
        self.timeTable = timeTable
        # logs can be a list of lists. Each list corresponding to a particular node
        self.logs = logs

    def __repr__(self):
        return "Class: %s, State: %s, TimeTable: %s, Blog: %s" %(self.__class__.__name__, self.state, self.timeTable, self.blog)
