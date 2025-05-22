import networkx as nx
from collections import Counter
import random
import matplotlib.pyplot as plt
import tqdm


class Game:
    def __init__(self, graph, payoff_matrix, pos=None):
        self.graph = graph
        self.pos = pos
        self.payoff_matrix = payoff_matrix

        self.colors = {
            list(self.payoff_matrix.keys())[0]: "blue",
            list(self.payoff_matrix.keys())[1]: "red",
        }

    def reset_graph(self):
        actions = list(self.payoff_matrix.keys())

        for node in self.graph.nodes():
            self.graph.nodes[node]["action"] = (
                actions[0] if random.random() < 0.5 else actions[1]
            )
            self.graph.nodes[node]["payoff"] = 0

    def update_strategy(self):
        for node_name in self.graph.nodes():
            node = self.graph.nodes[node_name]
            neighbors = list(self.graph.neighbors(node_name))

            max_payoff = node["curr_payoff"]
            best_neighbors = [node_name]

            for neighbor_name in neighbors:
                neighbor = self.graph.nodes[neighbor_name]
                if neighbor["curr_payoff"] > max_payoff:
                    max_payoff = neighbor["curr_payoff"]
                    best_neighbors = [neighbor_name]
                elif neighbor["curr_payoff"] == max_payoff:
                    best_neighbors.append(neighbor_name)

            if best_neighbors:
                chosen = random.choice(best_neighbors)
                node["action"] = self.graph.nodes[chosen]["action"]

    def play_network(self):
        total_counter = Counter()

        for node_name in self.graph.nodes():
            total_counter[self.graph.nodes[node_name]["action"]] += 1
            node1 = self.graph.nodes[node_name]
            node1["curr_payoff"] = 0
            for neighbor_name in self.graph.neighbors(node_name):
                node2 = self.graph.nodes[neighbor_name]
                action1, action2 = node1["action"], node2["action"]
                payoff1, _ = self.payoff_matrix[action1][action2]
                node1["curr_payoff"] += payoff1

            n = len(list(self.graph.neighbors(node_name)))
            if n > 0:
                node1["curr_payoff"] /= n
            else:
                node1["curr_payoff"] = 0
        return total_counter

    def visualize_graph(self):
        nx.draw(
            self.graph,
            pos=self.pos,
            node_size=20,
            node_color=[
                self.colors[self.graph.nodes[node]["action"]]
                for node in self.graph.nodes()
            ],
            with_labels=False,
        )
        plt.show()

    def play_iter(self, iterations, plot=False):
        counters = []
        for i in tqdm.trange(iterations):
            counters.append(self.play_network())
            self.update_strategy()
        if plot:
            action1, action2 = list(self.payoff_matrix.keys())
            total_nodes = len(self.graph.nodes())
            plt.plot(
                range(iterations),
                [(counters[i][action1] / total_nodes) * 100 for i in range(iterations)],
                label=action1.capitalize(),
                color=self.colors[action1],
            )
            plt.plot(
                range(iterations),
                [(counters[i][action2] / total_nodes) * 100 for i in range(iterations)],
                label=action2.capitalize(),
                color=self.colors[action2],
            )
            plt.xlabel("Iterations")
            plt.ylabel("Percentage of Nodes")

            plt.legend()
            plt.show()
        return counters
