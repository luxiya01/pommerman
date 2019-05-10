import py_trees
import numpy as np
import utils


class SafePlaceCheck(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(SafePlaceCheck, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        # print(self.blackboard)
        # return py_trees.common.Status.RUNNING
        position = self.blackboard.obs['position']
        bomb_blast_strength = self.blackboard.obs['bomb_blast_strength']

        # Do nothing if we are in a safe place and there is a bomb around
        if utils.check_bomb_range(position,
                                  bomb_blast_strength) == utils.SUCCESS:
            self.blackboard.action = 0
            #print('I am safe!')
            return py_trees.common.Status.SUCCESS

        # Not in safe place
        return py_trees.common.Status.FAILURE
