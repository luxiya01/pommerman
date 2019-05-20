import py_trees


class MessageTeammate(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(MessageTeammate, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        # print(self.blackboard)
        return py_trees.common.Status.SUCCESS













