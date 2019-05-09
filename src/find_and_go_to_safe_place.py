import py_trees
import numpy as np
import utils


class FindAndGoToSafePlace(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(FindAndGoToSafePlace, self).__init__(name)
        self.blackboard = py_trees.blackboard.Blackboard()
        self.enemy_nearby_threshold = 2
        LEFT = 3
        RIGHT = 4
        DOWN = 2
        UP = 1
        self.index_to_action = {0: UP, 1: DOWN, 2: LEFT, 3: RIGHT}

    def setup(self):
        pass

    def initialise(self):
        pass

    def update(self):
        pos_x, pos_y = self.blackboard.obs['position']
        indices = np.clip(
            np.array([(pos_x - 1, pos_y), (pos_x + 1, pos_y), (pos_x,
                                                               pos_y - 1),
                      (pos_x, pos_y + 1)]), 0, 10)
        scores = np.zeros((indices.shape[0], 1))

        for i, board_index in enumerate(indices):
            scores[i] = self._calculate_score(board_index)

        print(scores)

        optimum_index = scores.argmax()
        self.blackboard.action = self.index_to_action[optimum_index]
        return py_trees.common.Status.SUCCESS

    def _calculate_score(self, board_index):
        i, j = board_index
        board = self.blackboard.obs['board']
        bomb_blast_strength = self.blackboard.obs['bomb_blast_strength']
        enemies = (self.blackboard.obs['enemies'][0].value,
                   self.blackboard.obs['enemies'][1].value)

        # Is wall or bomb or enemy
        if (board[i, j] > 0
                and board[i, j] < 5) or (board[i, j] == enemies[0]
                                         or board[i, j] == enemies[1]):
            return -float('inf')

        total_score = 0

        # Is in range of bomb
        bomb_range = utils.check_bomb_range(board_index, bomb_blast_strength)
        if bomb_range != utils.SUCCESS:
            total_score -= bomb_range * 10

        # Is power up
        if board[i, j] > 5 and board[i, j] < 9:
            total_score += 5

        # Is enemy nearby
        for enemy in enemies:
            enemy_pos = np.transpose(np.nonzero(board == enemy))
            if enemy_pos.size > 0:
                if np.linalg.norm(np.array([i, j]) - enemy_pos.flatten()
                                  ) < self.enemy_nearby_threshold:
                    total_score += -2

        return total_score
