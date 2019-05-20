import numpy as np
import py_trees

SUCCESS = -float('inf')


def check_bomb_range(position, bomb_blast_strength):
    nonzero_indices = np.transpose(np.nonzero(bomb_blast_strength))
    blackboard = py_trees.blackboard.Blackboard()
    board = blackboard.obs['board']

    for i in nonzero_indices:
        row, col = i
        # Bomb in the same row as the agent
        if position[0] == row:
            distance = abs(position[1] - col)

            if distance <= bomb_blast_strength[row, col]:

                max_position = max(position[1],col)
                min_position = min(position[1], col)

                for cell in range(min_position,max_position):
                    if board[row,cell] == 1 or board[row,cell] == 2:
                        return SUCCESS

                return distance
        if position[1] == col:
            distance = abs(position[0] - row)
            if distance <= bomb_blast_strength[row, col]:

                max_position = max(position[0], row)
                min_position = min(position[0], row)

                for cell in range(min_position, max_position):
                    if board[cell,col] == 1 or board[cell,col] == 2:
                        return SUCCESS

                return distance
    return SUCCESS


def check_visibility(position, board):
    nonzero_indices = np.transpose(np.nonzero(board))

    if nonzero_indices.size > 0:
        # print('Check visibility')
        return py_trees.common.Status.SUCCESS
    return py_trees.common.Status.FAILURE


def calculate_manhattan(candidate_position1, candidate_position2):
    x_dist = np.absolute(candidate_position1[0] - candidate_position2[0])
    y_dist = np.absolute(candidate_position1[1] - candidate_position2[1])

    return x_dist + y_dist


def calculate_score(board_index, enemy_nearby_threshold=2):
    blackboard = py_trees.blackboard.Blackboard()
    i, j = board_index
    board = blackboard.obs['board']
    bomb_blast_strength = blackboard.obs['bomb_blast_strength']
    enemies = (blackboard.obs['enemies'][0].value,
               blackboard.obs['enemies'][1].value)
    team_mate = blackboard.obs['teammate'].value

    # Is wall or bomb or enemy
    #print("Board index: " + str(board[i, j]))
    if (board[i,j] == 1) or (board[i,j] == 3)or (board[i,j] == 4):
        return -1000

    if (board[i,j] == 2):
        return -100

    if (board[i, j] == enemies[0] or board[i, j] == enemies[1]):
        return -10

    if board[i, j] == team_mate:
        return -10

    total_score = -7

    # Is in range of bomb
    bomb_range = check_bomb_range(board_index, bomb_blast_strength)
    if bomb_range != SUCCESS:

        total_score -= 1 / (1 + bomb_range) * 100

    # Is power up
    if board[i, j] > 5 and board[i, j] < 9:
        total_score += -5

    # Is enemy nearby
    for enemy in enemies:
        enemy_pos = np.transpose(np.nonzero(board == enemy))
        if enemy_pos.size > 0:
            if np.linalg.norm(np.array([i, j]) -
                              enemy_pos.flatten()) < enemy_nearby_threshold:
                total_score += -10

    return total_score


def get_neighbour_indices(index):
    pos_x, pos_y = index
    neighbours = []
    neighbours_array = np.clip(np.array([(pos_x - 1, pos_y), (pos_x + 1, pos_y),
                  (pos_x, pos_y - 1), (pos_x, pos_y + 1)]), 0, 10)
    for neighbour in neighbours_array:
        if (neighbour[0]== pos_x) and  (neighbour[1]== pos_y):
            continue
        neighbours.append(tuple(neighbour))
    #print('neighbours: ', neighbours)
    return neighbours


def get_astar_path_and_cost(start_pos, goal_pos, came_from, costs):
    index = goal_pos
    total_cost = 0
    path = []
   # print('costs: ', costs)
    while index != start_pos:
        path.append(index)
       # print('index: ', index)
        total_cost += costs[index]
        index = came_from[index]
    #print('returning A* path')
    return {'path': path, 'cost': total_cost}


def next_action(start_pos, next_pos):
    start_x, start_y = start_pos
    next_x, next_y = next_pos

    if start_x - next_x == 1:
        # UP!
        return 1
    elif start_x - next_x == -1:
        # DOWN!
        return 2
    elif start_y - next_y == 1:
        # LEFT!
        return 3
    elif start_y - next_y == -1:
        # RIGHT!
        return 4
    return 0


def astar(grid, start_pos, goal_pos):
    x_dim, y_dim = grid.shape

    frontier = dict()
    frontier[start_pos] = 0

    came_from = {}
    cost_so_far = {}
    came_from[start_pos] = None
    cost_so_far[start_pos] = 0
    visited = set()


    while frontier:
        sorted_frontier = sorted(frontier.items(), key=lambda kv: kv[1])
      #  print('still in the while loop')
        current_pos = sorted_frontier[0][0]
        del frontier[current_pos]
        visited.add(current_pos)
        if current_pos == goal_pos:
           # print('break')
            break

        for neighbour in get_neighbour_indices(current_pos):
            #print('got into for loop')
            if grid[neighbour[0],neighbour[1]] == 5:
                continue
            neighbour_score = -calculate_score(neighbour,1)
            new_cost = cost_so_far[current_pos] + neighbour_score
            #print('neighbour is ', neighbour, ' score = ', neighbour_score)
            if (neighbour not in cost_so_far) or (new_cost <
                                                  cost_so_far[neighbour]):
             #   print('Update cost so far!')
                cost_so_far[neighbour] = new_cost
                priority = new_cost + calculate_manhattan(neighbour, goal_pos)
                if not neighbour in visited:
                    frontier[neighbour] = priority
                came_from[neighbour] = current_pos
    return get_astar_path_and_cost(start_pos, goal_pos, came_from, cost_so_far)
