import py_trees
from pommerman.agents import BaseAgent
from pommerman import constants, utility
from custom_behaviours import *
from bomb_nearby_side_behaviours import *
from explore_behavious import *
import numpy as np


class PyTreeAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super(PyTreeAgent, self).__init__(*args, **kwargs)
        self.blackboard = py_trees.blackboard.Blackboard()
        self.tree = self._create_tree()
        self.tree.setup_with_descendants()

        self.tmp_counter = 0
        self.blackboard.action = 0
        self.blackboard.recently_kicked_bomb = 5

    def act(self, obs, action_space):
        """
        if self.tmp_counter < 1:
            self.tmp_counter += 1
            return 5
            #return np.random.randint(0, 6)
    """
        self.blackboard.obs = obs
        self.tree.tick_once()

        #print("blackboard action: "+ str(self.blackboard.action))

        return int(self.blackboard.action)

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
        kick_or_hide_root = py_trees.composites.Selector(
            name='Kick or hide root')
        kick_root = py_trees.composites.Sequence(name='Kick root')
        kick_check = KickCheck(name='Kick check')
        kick = Kick(name='Kick')
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

        explore_map_root = py_trees.composites.Selector(
            name='Explore map root')

        explore_wooden_wall_root = py_trees.composites.Sequence(
            name='Explore wooden wall root')

        enemy_close_by_check = EnemyCloseByCheck(name='Enemy close by?')

        place_bomb = PlaceBomb(name='place bomb')

        wooden_wall_check = WoodenWallCheck(name='Wooden wall check')

        bomb_wooden_wall = BombWoodenWall(name='Bomb wooden wall')

        explore_randomly = ExploreRandomly(name='Explore randomly')

        # Build tree
        ## Bomb side
        safe_place_root.add_children(
            [safe_place_check])  #, wait_for_explosion])
        kick_or_hide_root.add_children(
            [kick_root, check_and_find_safe_place_root])
        kick_root.add_children([kick_check, kick])
        check_and_find_safe_place_root.add_children(
            [safe_place_root, find_and_go_to_safe_place])
        bomb_nearby_root.add_children(
            [bomb_nearby_check, message_teammate, kick_or_hide_root])

        ## Explore side
        enemy_close_by_root.add_children([enemy_close_by_check, place_bomb])
        bomb_enemy_or_explore_map_root.add_children(
            [enemy_close_by_root, explore_map_root])
        explore_map_root.add_children(
            [explore_wooden_wall_root, explore_randomly])
        explore_wooden_wall_root.add_children(
            [wooden_wall_check, bomb_wooden_wall])
        power_up_root.add_children([power_up_check, take_power_up])
        explore_root.add_children(
            [power_up_root, bomb_enemy_or_explore_map_root])

        ## Final root!
        root.add_children([bomb_nearby_root, explore_root])

        return root
