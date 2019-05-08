import py_trees


class BombNearBy(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(BombNearBy, self).__init__(name)

    def setup(self, obs):
        self.obs = obs

    def initialise(self):
        pass

    def update(self):

