import numpy as np
import math
import copy

np.random.seed(42)

class Reservoirsampling:
    def __init__(self, objective, solution, k=20, args=None):
        super(Reservoirsampling, self).__init__()
        # input parameter
        self.objective = objective
        self.k = k
        # state parameter
        self.iteration = 1
        self.solution = solution
        self.element = None
    
    def run(self, args=None):
        S=[]
        for i in range(self.objective.getN()):
            if len(S) < self.k:
                S.append(i)
            else:
                if np.random.random() < self.k / (i + 1):
                    y = np.random.choice(S,1)
                    S.remove(y)
                    S.append(i)
        for e_i in S:
            self.objective.add(e_i, self.solution)
        return self.solution

            

                

