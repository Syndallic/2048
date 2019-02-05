import numpy as np

from constants import Direction


class RandomAgent:

    def get_action(self):
        directions = [d for d in Direction]
        return np.random.choice(directions)

    def update_last_reward(self, reward):
        print(reward)