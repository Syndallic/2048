"""Based on https://github.com/MorvanZhou/PyTorch-Tutorial/blob/master/tutorial-contents-notebooks/405_DQN_Reinforcement_learning.ipynb"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from constants import Direction

BATCH_SIZE = 32
LR = 0.01  # learning rate
EPSILON = 0.5  # greedy policy
GAMMA = 0.9  # reward discount
TARGET_REPLACE_ITER = 100  # target update frequency
MEMORY_CAPACITY = 2000

input_size = 16
N_ACTIONS = 4

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Net(nn.Module):
    def __init__(self, ):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, 50)
        self.fc1.weight.data.normal_(0, 0.1)  # initialization
        self.out = nn.Linear(50, N_ACTIONS)
        self.out.weight.data.normal_(0, 0.1)  # initialization

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        actions_value = self.out(x)
        return actions_value


class DQN(object):
    def __init__(self):
        self.eval_net, self.target_net = Net().to(device), Net().to(device)

        self.learn_step_counter = 0  # for target updating
        self.memory_counter = 0  # for storing memory
        self.memory = np.zeros((MEMORY_CAPACITY, input_size * 2 + 2))  # initialize memory
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=LR)
        self.loss_func = nn.MSELoss()

    def choose_action(self, x):
        x = torch.unsqueeze(torch.FloatTensor(x), 0).to(device)
        # input only one sample
        if np.random.uniform() < EPSILON:  # greedy
            actions_value = self.eval_net.forward(x)
            action = torch.max(actions_value, 1)[1].cpu().data.numpy()
            action = action[0]  # return the argmax index
        else:  # random
            action = np.random.randint(0, N_ACTIONS)
        return action

    def store_transition(self, s, a, r, s_):
        transition = np.hstack((s, [a, r], s_))
        # replace the old memory with new memory
        index = self.memory_counter % MEMORY_CAPACITY
        self.memory[index, :] = transition
        self.memory_counter += 1

    def learn(self):
        if self.memory_counter < MEMORY_CAPACITY:
            return

        # target parameter update
        if self.learn_step_counter % TARGET_REPLACE_ITER == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step_counter += 1

        # sample batch transitions
        sample_index = np.random.choice(MEMORY_CAPACITY, BATCH_SIZE)
        b_memory = self.memory[sample_index, :]
        b_s = torch.FloatTensor(b_memory[:, :input_size]).to(device)
        b_a = torch.LongTensor(b_memory[:, input_size:input_size + 1].astype(int)).to(device)
        b_r = torch.FloatTensor(b_memory[:, input_size + 1:input_size + 2]).to(device)
        b_s_ = torch.FloatTensor(b_memory[:, -input_size:]).to(device)

        # q_eval w.r.t the action in experience
        q_eval = self.eval_net(b_s).gather(1, b_a)  # shape (batch, 1)
        q_next = self.target_net(b_s_).detach()  # detach from graph, don't backpropagate
        q_target = b_r + GAMMA * q_next.max(1)[0].view(BATCH_SIZE, 1)  # shape (batch, 1)
        loss = self.loss_func(q_eval, q_target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


class QAgent:
    def __init__(self):
        self.model = DQN()
        self.last_state = None
        self.last_action = None

    def get_action(self, grid):
        self.last_state = self.get_state(grid)
        self.last_action = self.model.choose_action(self.last_state)
        return Direction(self.last_action)

    def reward(self, reward, grid):
        new_state = self.get_state(grid)
        self.model.store_transition(self.last_state, self.last_action, reward, new_state)
        self.model.learn()

    def get_state(self, grid):
        """Rank based"""
        grid = grid.flatten()
        unique_values = np.unique(grid)
        for i, value in enumerate(unique_values):
            grid[grid == value] = i
        return grid
