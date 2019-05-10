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
        power_ups_board = np.logical_and(board>5, board <9)

        return utils.check_visibility(position,power_ups_board)

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
        pos_x,pos_y = position
        board = self.blackboard.obs['board']
        power_ups_board = np.logical_and(board > 5, board < 9)

        power_ups = np.argwhere(power_ups_board)

        positions = np.clip(
            np.array([(pos_x - 1, pos_y), (pos_x + 1, pos_y), (pos_x,
                                                               pos_y - 1),
                      (pos_x, pos_y + 1)]), 0, 10)

        max_dist = np.inf
        closest_powerup = 0

        for i, pos in enumerate(positions):
            if board[pos[0],pos[1]] >0 and board[pos[0],pos[1]]<5:
                continue
            for power in power_ups:
                distance = utils.calculate_manhattan(pos, power)
                if distance<max_dist:
                    max_dist = distance
                    closest_powerup = i
        self.blackboard.action = closest_powerup+1

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
        print("checking enemies")
        return utils.check_visibility(position, enemy_board)