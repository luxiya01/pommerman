import py_trees
from pommerman.agents import BaseAgent
from pommerman import constants, utility


class PyTreeAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super(PyTreeAgent, self).__init__(*args, **kwargs)
        self.tree = self.create_tree()

    def act(self, obs, action_space):
        pass

    def _create_tree(self):
        root = py_trees.composites.Selector(name='Test tree')

        bomb_nearby_root = py_trees.composites.Sequence(
            name='bomb nearby root')
        # bomb_nearby =
