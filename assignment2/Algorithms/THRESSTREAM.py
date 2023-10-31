import numpy as np
import math
import copy

class ThresStream:
    def __init__(self, objective, solution, k=20, epsilon=0.5, args=None):
        super(ThresStream, self).__init__()
        # input parameter
        self.objective = objective
        self.epsilon = epsilon
        self.k = k
        # state parameter
        self.iteration = 1
        self.solution = solution
        self.element = None
        # key parameter
        self.O = []
        self.S_v = {}
        self.m = 0
        
    def opt_guess(self, i):
        update_m = False
        Singletonf = self.objective.Singletonf(i)
        if self.m < Singletonf:
            self.m =  Singletonf
            update_m = True
        return update_m
            
    def get_O(self):
        i = math.floor(np.log(self.m) / np.log(1 + self.epsilon))
        while 1:
            v = (1 + self.epsilon) ** i
            if v >= self.m and v <= 2 * self.k * self.m:
                self.O.append(v)
            elif v > 2 * self.k * self.m:
                break
            i += 1
            
    def get_S_v(self):
        if len(self.S_v) == 0:
            for i in self.O:
                self.S_v[i] = copy.deepcopy(self.solution)
        else:
            for i in self.O:
                if i not in list(self.S_v.keys()):
                    self.S_v[i] = copy.deepcopy(self.solution)
            index_delete = list(self.S_v.keys()).index(self.O[0])
            delete_list = list(self.S_v.keys())[0:index_delete]
            for item in delete_list:
                self.S_v.pop(item)
                    
    def run(self, args=None):
        for i in range(self.objective.getN()):
            update_max = self.opt_guess(i)
            if update_max:
                self.get_O()
                self.get_S_v()
            for v in self.O:
                if self.objective.deltaf(i, self.S_v[v]) >= v / (2 * self.k) and len(self.S_v[v].X_set) < self.k:
                    self.objective.add(i, self.S_v[v])
        solution_value_list = [self.S_v[v].getf() for v in list(self.S_v.keys())]
        returned_v = list(self.S_v.keys())[np.argmax(solution_value_list)]
        return self.S_v[returned_v]

            

                

