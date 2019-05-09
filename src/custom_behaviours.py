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


class PowerUpCheck(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(PowerUpCheck, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        # print(self.blackboard)
        return py_trees.common.Status.RUNNING


class TakePowerUp(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(TakePowerUp, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        # print(self.blackboard)
        return py_trees.common.Status.RUNNING


class EnemyCloseByCheck(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(EnemyCloseByCheck, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        # print(self.blackboard)
        return py_trees.common.Status.RUNNING


class PlaceBomb(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(PlaceBomb, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        # print(self.blackboard)
        return py_trees.common.Status.RUNNING


class ExploreAndUpdateMap(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(ExploreAndUpdateMap, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        # print(self.blackboard)
        return py_trees.common.Status.RUNNING
