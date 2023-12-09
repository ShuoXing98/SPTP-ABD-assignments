import numpy as np
import math
import copy
from utils.constraints import Cardinality_Constriant

class AdaptiveSeq:
    def __init__(self, objective, solution, epsilon=0.5, k=None, args=None):
        super(AdaptiveSeq, self).__init__()
        # input parameter
        self.objective = objective
        self.epsilon = epsilon
        self.k = k
        # state parameter
        self.iteration = None
        self.solution = solution
        self.element = None
        self.threshold = None
        self.rand_seq = []
        self.X = None
        self.constraint = None
        self.X_i = None
        self.adaptivity = 0

    def initialization(self):
        self.constraint = Cardinality_Constriant(self.k)
        self.iteration = int(math.ceil(1 / self.epsilon * np.log(self.k / self.epsilon)))
        self.get_threshold()
        
    def get_threshold(self):
         self.threshold = self.objective.maxSingleton(self.solution)

    def get_rand_seq(self):
        sequence = []
        remainig_ground_set = copy.deepcopy(self.X) 
        np.random.shuffle(remainig_ground_set)
        for a_i in remainig_ground_set:
            find_feasible = False
            if self.is_feasible(self.solution.X_set + sequence) and not a_i in self.solution.X_set:
                find_feasible = True
                sequence.append(a_i)
            if not find_feasible:
                break
        self.rand_seq = sequence

    def get_X_i(self):
        self.X_i = []
        temp_solution = copy.deepcopy(self.solution)
        temp_objective = copy.deepcopy(self.objective)
        temp_objective.evals = 0
        for id in self.rand_seq:
            X_i = []
            temp_objective.add(id, temp_solution)
            for jd in self.X:
                if self.is_feasible(temp_solution.X_set) and temp_objective.deltaf(jd, temp_solution) >= self.threshold:
                        X_i.append(jd)
            self.X_i.append(X_i)
        self.objective.evals += temp_objective.evals

    def is_feasible(self, sequence):
    # Move the feasibility check to a separate method for clarity
        return self.constraint.feasibility(sequence)

    def run(self, args=None):
        self.initialization()
        for iter in range(self.iteration):
            self.X = list(range(self.solution.getN()))
            while 1:
                self.get_rand_seq()
                self.get_X_i()
                for i in range(len(self.X_i)):
                    if len(self.X_i[i]) <= (1 - self.epsilon) * len(self.X):
                        i_star = i
                        break
                for j in range(i_star + 1):
                    self.objective.add(self.rand_seq[j], self.solution)
                self.X = self.X_i[i_star]
                self.adaptivity += 1
                if len(self.X) == 0:
                    break
            if len(self.solution.X_set) == self.k:
                break
            self.threshold = (1 - self.epsilon) * self.threshold
        return self.solution, self.adaptivity
            

