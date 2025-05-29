import numpy as np
import math
from mesa.experimental.cell_space import CellAgent

## Helper function to get distance between two cells
def get_distance(cell_1, cell_2):
    x1, y1 = cell_1.coordinate
    x2, y2 = cell_2.coordinate
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx**2 + dy**2)

class StrategyAgent(CellAgent):
    ## Initialize agent
    def __init__(self, model, cell, learner_type=None):
        super().__init__(model)
        self.cell = cell
        self.strategy = self.initialize_strategy()
        if learner_type is None:
            self.learner_type = "horizontal" if self.random.random() < self.model.horizontal_ratio else "vertical"
        else:
            self.learner_type = learner_type
        self.is_role_model = False
        self.role_model_age = 0
        self.gain = self.calculate_gain()

    # Generate initial strategy for each agent
    # The accuracy to key should be a normal distributuon. 
    # A few agents are highly accurate, e.g., 24/25, while most agents have mediocre strategy, e.g., 12/25. 
    def initialize_strategy(self):
        strategy = self.model.key_matrix.copy()
        accuracy = int(np.clip(np.random.normal(loc=12.5, scale=3), 0, 25))
        correct_indices = self.random.sample(range(25), accuracy)
        for i in range(25):
            if i not in correct_indices:
                strategy[i] = self.random.choice([x for x in range(10) if x != self.model.key_matrix[i]])
        return strategy


    # Comparing the agent's strategy to the key, and calculate its gain. 1 point for 1 correct digit. 
    def calculate_gain(self):
        return sum(1 for s, k in zip(self.strategy, self.model.key_matrix) if s == k)

    def step(self):
        if self.is_role_model:
            self.role_model_age += 1  # Track aging of role models. They can only live for two generations. 
            return # Role models cannot conduct social learning. 
        if self.learner_type == "horizontal":
            self.horizontal_learn()
        else:
            self.vertical_learn()
        self.gain = self.calculate_gain()

# define horizontal and vertical learning
    def horizontal_learn(self):
        # look for all peer neighbors
        peer_neighbors = [a for a in self.cell.neighborhood.agents if not a.is_role_model and a != self]
        # If there are peer neighbors, find the most successful peer neighbor
        if peer_neighbors:
            best_peer = max(peer_neighbors, key=lambda a: a.gain)
        # If there aren't peer neighbors, find the closest peer neighbor in the grid  
        else: 
            all_peers = [a for a in self.model.agents if not a.is_role_model and a != self]
            # make a list of their cell
        # If there are no peers in the grid, return
            if not all_peers:
                return
            best_peer = min(all_peers, key=lambda a: get_distance(self.cell, a.cell))
        # If the agent is the most successful itself, don't learn. 
        if best_peer.gain > self.gain:
            self.adopt_strategy(best_peer)

    def vertical_learn(self):
        # look for all senior neighbors ("role models")
        role_model_neighbors = [a for a in self.cell.neighborhood.agents if a.is_role_model]
        # If there are senior neighbors, find the most successful senior neighbor
        if role_model_neighbors:
            best_model = max(role_model_neighbors, key=lambda a: a.gain)
        # If there aren't senior neighbors, find the closest senior neighbor in the grid  
        else:
            all_models = [a for a in self.model.agents if a.is_role_model]
        # If there are no seniors in the grid, return
            if not all_models:
                return 
            best_model = min(all_models, key=lambda a: get_distance(self.cell, a.cell))
        # If the agent is the most successful itself, don't learn. 
        if best_model.gain > self.gain:
            self.adopt_strategy(best_model)

    # After deciding the object of social learning, agents blindly learn one digit from this object.
    # Note that they get to keep their original correct digits.
    def adopt_strategy(self, other):
        error_indices = [i for i, (s, k) in enumerate(zip(self.strategy, self.model.key_matrix)) if s != k]
        learnable_indices = [i for i in error_indices if self.strategy[i] != other.strategy[i]]
        if learnable_indices:
            idx = self.random.choice(learnable_indices)
            self.strategy[idx] = other.strategy[idx]
