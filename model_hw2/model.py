import numpy as np
import mesa
from agents import StrategyAgent
from mesa.experimental.cell_space import OrthogonalMooreGrid

class StrategyModel(mesa.Model): 
    # Initializing model
    # The grid size is 20 by 20. The key changes 50% by each generation (a volatile socieity).
    # There are 50% horizontal learners. 30% of senior agents get to be kept as role models to the next generation. 
    def __init__(self, width=20, height=20, seed=None, key_change=0.5, horizontal_ratio=0.5, role_model_ratio=0.3):
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        ## Initialize grid
        self.grid = OrthogonalMooreGrid((width, height), torus=True, random=self.random)
        self.schedule = mesa.time.BaseScheduler(self)
        self.generation = 0
        self.round = 0
        self.key_change = key_change
        self.horizontal_ratio = horizontal_ratio
        self.role_model_ratio = role_model_ratio
        self.key_matrix = self.generate_key_matrix()
        ## Set up datacollector, collects the average gain of different agents
        self.datacollector = mesa.DataCollector(
            {
                "Horizontal_Avg_Gain": lambda m: m.average_gain("horizontal"),
                "Vertical_Avg_Gain": lambda m: m.average_gain("vertical"),
                "Total_Gain": lambda m: m.total_gain(),
            }
        )
        self.init_agents()
        self.datacollector.collect(self)
        
    # generate the key strategy of the first generation
    def generate_key_matrix(self):
        return self.random.choices(range(10), k=25)
    
    # mutate the key strategy based on the proportion of key change for succeeding generations
    def mutate_key_matrix(self):
        new_key = self.key_matrix.copy()
        num_changes = int(self.key_change * 25)
        indices = self.random.sample(range(25), num_changes)
        for idx in indices:
            new_key[idx] = self.random.choice([i for i in range(10) if i != new_key[idx]])
        return new_key
    
    # Initialize new agents in a new generation. 
    # TODO: need to revise code here. In a new generation, role models will be kept while others are cleared.
    # The blank places will be filled in with new agents. 
    def init_agents(self):
        self.schedule = mesa.time.BaseScheduler(self)
        self.grid.clear()
        for cell in self.grid.all_cells.cells:
            agent = StrategyAgent(self, cell)
            self.grid.place_agent(agent, cell)
            self.schedule.add(agent)

    # Initialize a new generation. Change the key to the current generation. 
    def step(self):
        if self.round == 0:
            self.key_matrix = self.mutate_key_matrix()
            self.generation += 1
            self.init_agents() 
        self.schedule.step()
        self.round = (self.round + 1) % 5
        # When a generation reaches its end, selece new role models. 
        # TODO: need to finalize how to deal with older role models here. 
        if self.round == 0:  
            self.select_role_models()
        self.datacollector.collect(self)

    # keep the most successful agents as role models into the next generation. 
    # TODO: role models can be kept for only one generation. In other words, the calculation and elimination 
    # at the end of each generation include only active agents. Role models will be eliminated at the third generation
    # after it was created. 
    def select_role_models(self):
        agents = list(self.schedule.agents)
        agents.sort(key=lambda a: a.gain, reverse=True)
        num_keep = int(len(agents) * self.role_model_ratio)
        keep_agents = agents[:num_keep]
        for agent in keep_agents:
            agent.is_role_model = True
        for agent in agents[num_keep:]:
            self.grid.remove_agent(agent)
            self.schedule.remove(agent)

    # Calculate the average gain of all active vertical/horizontal learners. 
    def average_gain(self, learner_type):
        agents = [a for a in self.schedule.agents if a.learner_type == learner_type and not a.is_role_model]
        if agents:
            return sum(a.gain for a in agents) / len(agents)
        return 0
    
    # Calculate the gross gain of all active agents. 
    # TODO: Incomplete code. This is the gross gain of one single generation. It will be reset after each generation. 
    # What we want to observe is how the proportion of different learners affect global accumulative gain. 
    # We need to change this calculation to one settlement each generation, not each round. Then we will add 
    # up the gross gain of each generation. 
    def total_gain(self):
        return sum(a.gain for a in self.schedule.agents if not a.is_role_model)
