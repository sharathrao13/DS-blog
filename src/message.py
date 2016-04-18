class Message(object):

    def __init__(self, state, timeTable = None, blog = None):
        # Possible states: sync, get, update
        self.state = state
        self.timeTable = timeTable
        self.blog = blog

    def __repr__(self):
        return "Class: %s, State: %s, TimeTable: %s, Blog: %s" %(self.__class__.__name__, self.state, self.timeTable, self.blog)
