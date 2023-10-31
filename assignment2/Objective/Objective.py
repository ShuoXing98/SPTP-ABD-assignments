import numpy as np
from Objective.Solution import Solution

class Objective:
    
    """Base class for obejctive submodular functions."""

    def __init__(self):
        super(Objective, self).__init__()
        self.univ = [] # What is the ground set out of n elements 
        self.costs = [] # Takes elements in the universe to their cost
        self.evals = 0 # number of times objective has been queried
        self.unif_cost = False # Whether costs are to be taken into account or treat as uniform (IGNORED DURING getTrueCost)
        self.mincost = 0.0
        
    def getN(self):
        return len(self.univ)
    
    def getCost(self, id):
        if self.unif_cost:
            return 1
        else: 
            return self.costs[id]
        
    def inUniv(self, i):
        return self.univ[i]
  
    def getEvals(self):
        return self.evals
        
    def calculateMinCost(self):
        if not self.unif_cost:
            self.mincost = np.min(self.costs)
        else:
            self.mincost = 1
