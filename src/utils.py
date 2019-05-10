import numpy as np
import py_trees

SUCCESS = -float('inf')


def check_bomb_range(position, bomb_blast_strength):
    nonzero_indices = np.transpose(np.nonzero(bomb_blast_strength))

    for i in nonzero_indices:
        row, col = i
        # Bomb in the same row as the agent
        if position[0] == row:
            distance = abs(position[1] - col)
            if distance <= bomb_blast_strength[row, col]:

                return distance
        if position[1] == col:
            distance = abs(position[0] - row)
            if distance <= bomb_blast_strength[row, col]:

                return distance
    return SUCCESS


def check_visibility(position, board):
    nonzero_indices = np.transpose(np.nonzero(board))

    if nonzero_indices.size > 0:
        print('Check visibility')
        return py_trees.common.Status.SUCCESS
    return py_trees.common.Status.FAILURE

def calculate_manhattan(candidate_position1, candidate_position2):
    x_dist = np.absolute(candidate_position1[0]-candidate_position2[0])
    y_dist = np.absolute(candidate_position1[1]-candidate_position2[1])

    return x_dist+y_dist

