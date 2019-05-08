import py_trees


class TestTree:
    def __init__(self):
        self.tree = self.create_tree()

    def create_tree(self):
        root = py_trees.composites.Selector(name='Test tree')

        bomb_nearby_root = py_trees.composites.Sequence(
            name='bomb nearby root')
