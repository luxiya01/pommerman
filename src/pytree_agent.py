import py_trees
from pommerman.agents import BaseAgent
from pommerman import constants, utility
from custom_behaviours import *
from bomb_nearby_check import BombNearByCheck
from safety_place_check import SafePlaceCheck
from find_and_go_to_safe_place import FindAndGoToSafePlace
import numpy as np


class PyTreeAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super(PyTreeAgent, self).__init__(*args, **kwargs)
        self.blackboard = py_trees.blackboard.Blackboard()
        self.tree = self._create_tree()
        self.tree.setup_with_descendants()

        self.tmp_counter = 0

    def act(self, obs, action_space):
        self.blackboard.obs = obs
        if self.tmp_counter < 1:
            self.tmp_counter += 1
            return 5
            #return np.random.randint(0, 6)

        self.blackboard.action = 0
        self.tree.tick_once()

        print(self.blackboard.action)

        return self.blackboard.action

    def _create_tree(self):
        # Define nodes
        root = py_trees.composites.Selector(name='Test tree')

        ## Bomb side
        bomb_nearby_root = py_trees.composites.Sequence(
            name='bomb nearby root')
        bomb_nearby_check = BombNearByCheck(name='Bomb nearby?')

        message_teammate = MessageTeammate(name='Message teammate')

        check_and_find_safe_place_root = py_trees.composites.Selector(
            name='Check and find safe place root')
        safe_place_root = py_trees.composites.Sequence(name='Safe place root')
        safe_place_check = SafePlaceCheck(name='safe place?')
        # wait_for_explosion = WaitForExplotion(name='Wait for explosion')
        find_and_go_to_safe_place = FindAndGoToSafePlace(
            name='Find and go to safe place')

        ## Explore side
        explore_root = py_trees.composites.Selector(name='Explore root')
        power_up_root = py_trees.composites.Sequence(name='Power up root')
        power_up_check = PowerUpCheck(name='Power up check')
        take_power_up = TakePowerUp(name='Take power up')

        bomb_enemy_or_explore_map_root = py_trees.composites.Selector(
            name='Explore check')
        enemy_close_by_root = py_trees.composites.Sequence(
            name='Enemy close by root')
        enemy_close_by_check = EnemyCloseByCheck(name='Enemy close by?')
        place_bomb = PlaceBomb(name='place bomb')

        explore_and_update_map = ExploreAndUpdateMap(
            name='Explore and update map')

        # Build tree
        ## Bomb side
        safe_place_root.add_children(
            [safe_place_check])  #, wait_for_explosion])
        check_and_find_safe_place_root.add_children(
            [safe_place_root, find_and_go_to_safe_place])
        bomb_nearby_root.add_children([
            bomb_nearby_check, message_teammate, check_and_find_safe_place_root
        ])

        ## Explore side
        enemy_close_by_root.add_children([enemy_close_by_check, place_bomb])
        bomb_enemy_or_explore_map_root.add_children(
            [enemy_close_by_root, explore_and_update_map])
        power_up_root.add_children([power_up_check, take_power_up])
        explore_root.add_children(
            [power_up_root, bomb_enemy_or_explore_map_root])

        ## Final root!
        root.add_children([bomb_nearby_root, explore_root])

        return root
