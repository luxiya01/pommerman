import py_trees
import utils
import numpy as np
import time


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

        if board[best_next_step[0],best_next_step[1]]== 2 and self.blackboard.obs['ammo']>0:
            self.blackboard.action = 5

        elif board[best_next_step[0],best_next_step[1]]== 1:
            return py_trees.common.Status.FAILURE
        else:
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

        position = self.blackboard.obs['position']
        board = self.blackboard.obs['board']
        enemies = (self.blackboard.obs['enemies'][0].value,
                   self.blackboard.obs['enemies'][1].value)
        enemy_board = np.logical_or(board == enemies[0], board == enemies[1])
        enemy_positions = np.argwhere(enemy_board)

        best_next_step = position
        min_cost = float('inf')
        for enemy in enemy_positions:
            path_and_cost = utils.astar(board, position, tuple(enemy))

            if path_and_cost['cost'] < min_cost:
                min_cost = path_and_cost['cost']
                best_next_step = path_and_cost['path'][-1]
                target_enemy = enemy

        # if wooden wall: bomb
        if board[best_next_step[0], best_next_step[1]] == 2 and self.blackboard.obs['ammo']>0:
            self.blackboard.action = 5
        # if rigid wall: cannot do anything
        elif board[best_next_step[0], best_next_step[1]] == 1:
            return py_trees.common.Status.FAILURE
        elif utils.calculate_manhattan(position, target_enemy)== 1:
            self.blackboard.action = 5
        else:
            self.blackboard.action = utils.next_action(position, best_next_step)

        return py_trees.common.Status.SUCCESS


class WoodenWallCheck(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(WoodenWallCheck, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        # print(self.blackboard)
        board = self.blackboard.obs['board']
        wooden_board = board == 2
        wooden_walls = np.nonzero(wooden_board)
        #if we can see wooden walls we return ture
        if wooden_walls[0].shape[0]>0:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


class BombWoodenWall(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(BombWoodenWall, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):

        board = self.blackboard.obs['board']
        position = self.blackboard.obs['position']
        wooden_board = board == 2
        wooden_indices = np.transpose(np.nonzero(wooden_board))

        best_next_step = position
        min_cost = np.inf
        for index in wooden_indices:
            path_and_cost = utils.astar(board, position, tuple(index))

            if path_and_cost['cost'] < min_cost:
                min_cost = path_and_cost['cost']
                best_next_step = path_and_cost['path'][-1]


        if board[best_next_step[0],best_next_step[1]]== 2 and self.blackboard.obs['ammo'] > 0:
            self.blackboard.action = 5

        elif board[best_next_step[0],best_next_step[1]]== 1:
            return py_trees.common.Status.FAILURE
        else:
            self.blackboard.action = utils.next_action(position, best_next_step)


        return py_trees.common.Status.SUCCESS

class ExploreRandomly(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(ExploreRandomly, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        # print(self.blackboard)
        position = self.blackboard.obs['position']
        board = self.blackboard.obs['board']
        traversable_neighbors = []
        traversable_actions = []
        for neighbour in utils.get_neighbour_indices(position):

            if board[neighbour[0],neighbour[1]] == 1:
                continue
            else:
                traversable_neighbors.append(neighbour)
                traversable_actions.append(utils.next_action(position, neighbour))



        self.blackboard.action = np.random.choice(traversable_actions)
        return py_trees.common.Status.SUCCESS
