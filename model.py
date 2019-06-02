import numpy as np

import constants
from constants import Direction
from q_agent import QAgent
from utils import PerformanceTracker


class GameModel:
    def __init__(self, agent):
        # np.random.seed(0)

        self.logger = PerformanceTracker()

        self.agent = agent
        self.score = 0
        self.grid = None

        self.init_model()

    def init_model(self):
        self.grid = np.zeros((constants.GRID_WIDTH, constants.GRID_HEIGHT), dtype=int)
        self.add_random_tile()
        self.add_random_tile()

        self.score = 0

    def agent_action(self):
        """Have the agent take an action, update grid, and reward agent"""
        old_score = self.get_score()

        direction = self.agent.get_action(self.grid)
        self.process_input(direction)

        if self.game_over():
            self.agent.reward(-100, self.grid)
            self.logger.new_high_score(self.get_score())

            print(len(self.logger.high_scores))

            self.init_model()
        else:
            score_difference = self.get_score() - old_score
            self.agent.reward(1, self.grid)

    def game_over(self):
        if np.any(self.grid == 0):
            return False

        # horizontal pass
        for line in self.grid:
            for i in range(len(line) - 1):
                if line[i] == line[i + 1]:
                    return False

        # vertical pass
        for line in self.grid.T:
            for i in range(len(line) - 1):
                if line[i] == line[i + 1]:
                    return False

        return True

    def get_score(self):
        return self.score

    def add_random_tile(self):
        """Add a '2' to a random unoccupied space on the grid"""
        x, y = np.where(self.grid == 0)
        i = np.random.randint(len(x))
        random_pos = x[i], y[i]
        self.grid[random_pos] = 2

    def process_input(self, direction):
        grid = None

        if direction == Direction.UP:
            grid = self.grid.T
        elif direction == Direction.DOWN:
            grid = np.flip(self.grid.T, 1)
        elif direction == Direction.LEFT:
            grid = self.grid
        elif direction == Direction.RIGHT:
            grid = np.flip(self.grid, 1)

        if self.process_lines(grid):
            self.add_random_tile()

    def move_element(self, line, old_index, new_index):
        if old_index != new_index:
            line[new_index] += line[old_index]
            line[old_index] = 0

            self.score += line[new_index]

            return True
        else:
            return False

    def process_lines(self, arr):
        """Collapse each line towards index 0"""
        changed = False

        for line in arr:
            current_index = 0
            for i in range(len(line)):
                if i != current_index and line[i] != 0:
                    # move if empty space at index 0 or we just merged
                    # index not updated - this element could still be merged
                    if line[current_index] == 0:
                        changed = self.move_element(line, i, current_index) or changed

                    # merge if values equal
                    elif line[current_index] == line[i]:
                        current_index += 1
                        changed = self.move_element(line, i, current_index - 1) or changed

                    # add to next index if different values
                    elif line[current_index] != line[i]:
                        current_index += 1
                        changed = self.move_element(line, i, current_index) or changed

        return changed


def main():
    model = GameModel(QAgent())
    while True:
        model.agent_action()


if __name__ == "__main__":
    main()
