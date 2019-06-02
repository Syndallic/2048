import matplotlib.pyplot as plt
import torch


class PerformanceTracker:
    def __init__(self):
        self.high_scores = []

    def new_high_score(self, score):
        self.high_scores.append(score)
        if len(self.high_scores) % 200 == 0:
            self.plot_performance()

    def plot_performance(self):
        plt.figure(2)
        plt.clf()
        rewards_t = torch.tensor(self.high_scores, dtype=torch.float)
        plt.title('Training')
        plt.xlabel('Episode')
        plt.ylabel('High Score')
        plt.plot(rewards_t.numpy(), 'r')
        # Take 100 episode averages and plot them too
        if len(rewards_t) >= 100:
            means = rewards_t.unfold(0, 100, 1).mean(1).view(-1)
            means = torch.cat((torch.zeros(99), means))
            plt.plot(means.numpy())
        plt.show()
