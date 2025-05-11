import numpy as np
from mesa.experimental.cell_space import CellAgent

class StrategyAgent(CellAgent):
    ## Initialize agent
    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell
        self.strategy = self.initialize_strategy()
        self.learner_type = "horizontal" if self.random.random() < self.model.horizontal_ratio else "vertical"
        self.is_role_model = False
        self.gain = self.calculate_gain()

    # Generate initial strategy for each agent
    def initialize_strategy(self):
        strategy = self.model.key_matrix.copy()
        # TODO: incomplete code. The accuracy to key should be a normal distributuon. 
        # A few agents are highly accurate, e.g., 24/25, while most agents have mediocre strategy, e.g., 10/25. 

    # Comparing the agent's strategy to the key, and calculate its gain. 1 point for 1 correct digit. 
    def calculate_gain(self):
        return sum(1 for s, k in zip(self.strategy, self.model.key_matrix) if s == k)

    def step(self):
        if self.is_role_model:
            return # Role models cannot conduct social learning. 
        if self.learner_type == "horizontal":
            self.horizontal_learn()
        else:
            self.vertical_learn()
        self.gain = self.calculate_gain()

    # TODO: incomplete code. If the agent itself is the most successful, then its strategy remain unchanged. 
    # If there are no peer agents in the neighborhood, the agent learns from the closest peer.   
    def horizontal_learn(self):
        neighbors = list(self.cell.neighborhood.agents)
        if not neighbors:
            return
        best_neighbor = max(neighbors, key=lambda a: a.gain)
        self.adopt_strategy(best_neighbor)

    def vertical_learn(self):
        neighbors = list(self.cell.neighborhood.agents)
        # TODO: This part of code needs examination. 
        seniors = [a for a in neighbors if a.is_role_model]
        if not seniors: # If there are no senior agents in the neighborhood, the agent learns from the closest role model. 
            seniors = [a for a in self.model.schedule.agents if a.is_role_model]
            if not seniors:
                return
            seniors.sort(key=lambda a: self.model.grid.get_distance(self.cell, a.cell))
        best_senior = max(seniors, key=lambda a: self.model.grid.get_distance(self.cell, a.cell))
        self.adopt_strategy(best_senior)

    # After deciding the object of social learning, agents blindly learn one digit from this object.
    def adopt_strategy(self, other):
        diff_indices = [i for i, (s, o) in enumerate(zip(self.strategy, other.strategy)) if s != o]
        if diff_indices:
            idx = self.random.choice(diff_indices)
            self.strategy[idx] = other.strategy[idx]
