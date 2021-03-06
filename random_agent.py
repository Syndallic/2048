import numpy as np

from constants import Direction


class RandomAgent:

    def get_action(self, state):
        directions = [d for d in Direction]
        return np.random.choice(directions)

    def reward(self, reward):
        pass
