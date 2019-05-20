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
        board = self.blackboard.obs['board']
        bomb_blast_strength = self.blackboard.obs['bomb_blast_strength']
        flame_board = (board == 4)
        nonzero_indices = np.nonzero(flame_board)
        bomb_blast_strength [nonzero_indices]=1
        return utils.check_visibility(position, bomb_blast_strength)

class KickCheck(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(KickCheck, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        position = self.blackboard.obs['position']
        board = self.blackboard.obs['board']
        canKick = self.blackboard.obs['can_kick']
        if not canKick:
            return py_trees.common.Status.FAILURE

        neighbours = utils.get_neighbour_indices(position)

        for neibour in neighbours:
            if board[neibour[0],neibour[1]] == 3:
                return py_trees.common.Status.SUCCESS

        return py_trees.common.Status.FAILURE

class Kick(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(Kick, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        position = self.blackboard.obs['position']
        board = self.blackboard.obs['board']
        bomb_positions = []
        neighbours = utils.get_neighbour_indices(position)

        for neibour in neighbours:
            if board[neibour[0], neibour[1]] == 3:
                bomb_positions.append(neibour)

        return py_trees.common.Status.FAILURE

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
        board = self.blackboard.obs['board']
        flame_board = (board == 4)
        nonzero_indices = np.nonzero(flame_board)
        bomb_blast_strength[nonzero_indices] = 1

        # Do nothing if we are in a safe place and there is a bomb around
        if utils.check_bomb_range(position,
                                  bomb_blast_strength) == utils.SUCCESS:
            self.blackboard.action = 0
            #print('I am safe!')
            return py_trees.common.Status.SUCCESS

        # Not in safe place
        return py_trees.common.Status.FAILURE

class FindAndGoToSafePlace(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(FindAndGoToSafePlace, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        position = self.blackboard.obs['position']

        #Find scores of surrounding cells
        scores, positions = self.find_scores(position)

        #print(scores)

        optimum_index = np.argwhere(scores == np.amax(scores))
        if np.shape(optimum_index)[0] > 1:
            for neighbor in optimum_index:
                n_scores, _ = self.find_scores(positions[neighbor[0]])
                max_n_scores = np.amax(n_scores)
                scores[neighbor[0]] += max_n_scores

        best_index = np.argmax(scores)
        self.blackboard.action = best_index
        return py_trees.common.Status.SUCCESS

    def find_scores(self, position):

        pos_x, pos_y = position
        positions = np.clip(
            np.array([(pos_x, pos_y), (pos_x - 1, pos_y), (pos_x + 1, pos_y),
                      (pos_x, pos_y - 1), (pos_x, pos_y + 1)]), 0, 10)

        scores = np.zeros((positions.shape[0], 1))

        for i, board_index in enumerate(positions):

            scores[i] = utils.calculate_score(board_index)
        return scores, positions
