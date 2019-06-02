import sys

import numpy as np
import tkinter as tk

import constants
from constants import Direction
from q_agent import QAgent
from random_agent import RandomAgent
from model import GameModel


class View:
    def __init__(self, agent=None):
        self.root = tk.Tk()
        self.model = GameModel(agent)
        self.agent = agent

        self.colours = ['salmon', 'light salmon', 'orange', 'dark orange', 'coral', 'light coral', 'tomato',
                        'orange red', 'red']

        self.label_grid = []
        self.init_grid()

        if agent is None:
            self.root.bind('<Left>', self.left_key)
            self.root.bind('<Right>', self.right_key)
            self.root.bind('<Up>', self.up_key)
            self.root.bind('<Down>', self.down_key)
            self.root.bind('<Escape>', self.close)
        else:
            self.agent_action()

        self.root.mainloop()

    def init_grid(self):
        for r in range(constants.GRID_WIDTH):
            self.label_grid.append([])
            for c in range(constants.GRID_HEIGHT):
                label = tk.Label(self.root, text='', borderwidth=4, width=5, height=2,
                                 font=("Helvetica", 40), relief="raised")
                label.grid(row=r, column=c)
                self.label_grid[r].append(label)

        self.update_grid()

    def update_grid(self):
        game_grid = self.model.grid
        for game_row, label_row in zip(game_grid, self.label_grid):
            for i in range(constants.GRID_WIDTH):
                if game_row[i] == 0:
                    text = ""
                    colour = "snow"
                else:
                    text = str(game_row[i])
                    colour = self.colours[min(int(np.log2(game_row[i])), len(self.colours) - 1)]

                label_row[i].configure(text=text, background=colour)

    def left_key(self, event):
        self.model.process_input(Direction.LEFT)
        self.update_grid()

    def up_key(self, event):
        self.model.process_input(Direction.UP)
        self.update_grid()

    def right_key(self, event):
        self.model.process_input(Direction.RIGHT)
        self.update_grid()

    def down_key(self, event):
        self.model.process_input(Direction.DOWN)
        self.update_grid()

    @staticmethod
    def close(event):
        sys.exit()

    def agent_action(self):
        """Hook to allow agent to interact"""
        self.model.agent_action()
        self.update_grid()

        self.root.after(1, self.agent_action)


def main():
    View(QAgent())


if __name__ == "__main__":
    main()
