import numpy as np
import mesa
from agents import StrategyAgent
from mesa.experimental.cell_space import OrthogonalMooreGrid

class StrategyModel(mesa.Model): 
    # Initializing model
    # The grid size is 20 by 20. The key changes 80% by each generation (a volatile socieity).
    # There are 50% horizontal learners. 30% of senior agents get to be kept as role models to the next generation. 
    def __init__(self, width=20, height=20, seed=None, key_change=0.8, horizontal_ratio=0.5, role_model_ratio=0.3):
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        ## Initialize grid
        self.grid = OrthogonalMooreGrid((width, height), torus=True, random=self.random)
        self.running = True # for batch run
        self.generation = 0
        self.round = 0
        self.key_change = key_change
        self.horizontal_ratio = horizontal_ratio
        self.role_model_ratio = role_model_ratio
        self.key_matrix = self.generate_key_matrix()
        ## Set up datacollector, collects the average gain of different agents
        self.datacollector = mesa.DataCollector(
            model_reporters=
            {
                "Horizontal_Avg_Gain": lambda m: m.average_gain("horizontal"),
                "Vertical_Avg_Gain": lambda m: m.average_gain("vertical"),
                "Total_Gain": lambda m: m.total_gain(),
                "Accumulated_Gain": lambda m: m.accumulated_gain,
                "Horizontal Final Average": lambda m: np.mean(m.horizontal_gains),
                "Vertical Final Average": lambda m: np.mean(m.vertical_gains)
            }
        )

        self.role_models = []

        #This record every round's "Horizontal/Vertical_Avg_Gain"
        self.horizontal_gains = []
        self.vertical_gains = []

        self.accumulated_gain = 0
        self.init_first_generation()
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

    def init_first_generation(self):
        empty_cells = [cell for cell in self.grid.all_cells.cells if not cell.agents]
        self.random.shuffle(empty_cells)
        num_horizontal = int(len(empty_cells) * self.horizontal_ratio)

        for i, cell in enumerate(empty_cells):
            learner_type = "horizontal" if i < num_horizontal else "vertical"
            StrategyAgent.create_agents(self, 1, cell=cell, learner_type=learner_type)

    def init_agents(self):
        for agent in list(self.agents):
            if not agent.is_role_model:
                agent.remove()

        # get all empty cells after cleaning up the non-role models
        empty_cells = [cell for cell in self.grid.all_cells.cells if not cell.agents]
        self.random.shuffle(empty_cells)
        num_horizontal = int(len(empty_cells) * self.horizontal_ratio)

        # fill in new agents
        for i, cell in enumerate(empty_cells):
            learner_type = "horizontal" if i < num_horizontal else "vertical"
            StrategyAgent.create_agents(self, 1, cell=cell, learner_type=learner_type)

    # Initialize a new generation. Change the key to the current generation. 
    def step(self):
        if self.round == 0:
            self.key_matrix = self.mutate_key_matrix()
            self.generation += 1
            self.init_agents() 

        self.agents.do("step")

        # Record this round's "Horizontal/Vertical_Avg_Gain"
        self.horizontal_gains.append(self.average_gain("horizontal"))
        self.vertical_gains.append(self.average_gain("vertical"))

        self.round = (self.round + 1) % 5
        
        # When a generation reaches its end, add to global wealth accumulation and select new role models. 
        if self.round == 0:  
            generation_gain = self.total_gain()
            self.accumulated_gain += generation_gain
            self.datacollector.collect(self)
            self.select_role_models() # keep role models and delete others
        else:
            self.datacollector.collect(self)

    # Identify the most successful agents as role models and only keep them in the grid
    def select_role_models(self):
        # delete previous role models
        for agent in self.role_models:
            agent.remove()

        # find the role model of this generation
        agents = [a for a in self.agents if not a.is_role_model]
        agents.sort(key=lambda a: a.gain, reverse=True)
        num_keep = int(len(agents) * self.role_model_ratio)
        keep_agents = agents[:num_keep]
        for agent in keep_agents:
            agent.is_role_model = True
        self.role_models = keep_agents

        # delete all other agents
        for agent in list(self.agents - set(keep_agents)):
            agent.remove()

    # Calculate the average gain of all active vertical/horizontal learners. 
    def average_gain(self, learner_type):
        agents = [a for a in self.agents if a.learner_type == learner_type and not a.is_role_model]
        if agents:
            return sum(a.gain for a in agents) / len(agents)
        return 0
    
    # Calculate the gross gain of all active agents. 
    def total_gain(self):
        return sum(a.gain for a in self.agents if not a.is_role_model)
