import numpy as np
import math
import copy

class Greedy:
    def __init__(self, objective, solution, k=20, args=None):
        super(Greedy, self).__init__()
        # input parameter
        self.objective = objective
        self.k = k
        # state parameter
        self.iteration = 1
        self.solution = solution
        self.element = None

    def get_deltaf(self):
        marginal_gain = []
        for i in range(self.objective.getN()):
            marginal_gain.append(self.objective.deltaf(i, self.solution))
        return marginal_gain
    
    def run(self, args=None):
        while len(self.solution.X_set) < self.k:
            marginal_gain = self.get_deltaf()
            e_i = np.argmax(marginal_gain)
            self.objective.add(e_i, self.solution)
        return self.solution, self.k

            

                

