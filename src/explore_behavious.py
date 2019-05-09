import py_trees
import utils
import numpy as np


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
