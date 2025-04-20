from mesa import Agent
import random # Modification: I imported random. 

class SchellingAgent(Agent):
    ## Initiate agent instance, inherit model trait from parent class
    def __init__(self, model, agent_type):
        super().__init__(model)
        ## Set agent type
        self.type = agent_type
    ## Define basic decision rule
    def move(self):
        ## Get list of neighbors within range of sight
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore = True, radius = self.model.radius, include_center = False)
        ## Count neighbors of same type as self
        similar_neighbors = len([n for n in neighbors if n.type == self.type])
        ## If an agent has any neighbors (to avoid division by zero), calculate share of neighbors of same type
        if (valid_neighbors := len(neighbors)) > 0:
            share_alike = similar_neighbors / valid_neighbors
        else:
            share_alike = 0
        ## If unhappy with neighbors, move to random empty slot. Otherwise add one to model count of happy agents.
        if share_alike < self.model.desired_share_alike:
            # Modification: The random number (larger or equal to 0, smaller than 1) represents the circumstances of the agent.
            # It is random, because various factors influence the individual's ability to move. 
            # This can include financial affordability, determination, job market competence, family structure, etc.  
            # 
            if random.random() > self.model.friction: 
                self.model.grid.move_to_empty(self)
        else: 
            self.model.happy +=1   
