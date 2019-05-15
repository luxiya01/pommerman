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
        position = self.blackboard.obs['position']
        board = self.blackboard.obs['board']
        power_ups_board = np.logical_and(board > 5, board < 9)

        return utils.check_visibility(position, power_ups_board)


class TakePowerUp(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(TakePowerUp, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        position = self.blackboard.obs['position']
        board = self.blackboard.obs['board']
        power_ups_board = np.logical_and(board > 5, board < 9)

        power_ups = np.argwhere(power_ups_board)

        best_next_step = position
        min_cost = float('inf')
        for power_up in power_ups:
            path_and_cost = utils.astar(board, position, tuple(power_up))
            if path_and_cost['cost'] < min_cost:
                min_cost = path_and_cost['cost']
                best_next_step = path_and_cost['path'][-1]

        self.blackboard.action = utils.next_action(position, best_next_step)

        return py_trees.common.Status.SUCCESS


class EnemyCloseByCheck(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(EnemyCloseByCheck, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        position = self.blackboard.obs['position']
        board = self.blackboard.obs['board']
        enemies = (self.blackboard.obs['enemies'][0].value,
                   self.blackboard.obs['enemies'][1].value)
        enemy_board = np.logical_or(board == enemies[0], board == enemies[1])
        # print("checking enemies")
        return utils.check_visibility(position, enemy_board)
