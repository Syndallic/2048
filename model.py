import numpy as np

import constants
from constants import Direction


class GameModel:
    def __init__(self):
        # np.random.seed(0)

        self.score = 0

        self.grid = np.zeros((constants.GRID_WIDTH, constants.GRID_HEIGHT), dtype=int)
        self.add_random()
        self.add_random()

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
            self.add_random()

    def game_over(self):
        return not np.any(self.grid == 0)

    def get_score(self):
        return self.score

    def add_random(self):
        """Add a '2' to a random unoccupied space on the grid"""
        x, y = np.where(self.grid == 0)
        i = np.random.randint(len(x))
        random_pos = x[i], y[i]
        self.grid[random_pos] = 2

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
