import py_trees
import numpy as np
import utils


class BombNearByCheck(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(BombNearByCheck, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        position = self.blackboard.obs['position']
        bomb_blast_strength = self.blackboard.obs['bomb_blast_strength']
        return utils.check_euclidean_distance(position, bomb_blast_strength)
