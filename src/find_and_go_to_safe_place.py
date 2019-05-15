import py_trees
import numpy as np
import utils


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
