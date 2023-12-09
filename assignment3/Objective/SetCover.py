from Objective.Objective import Objective
from Objective.SetCoverSolution import SetCoverSolution
import numpy as np

class SetCover(Objective):
    
    """
    There are n sets, which cover a universe of m elements
    """

    def __init__(self, mono, unif_cost=False, args=None):
        super(SetCover, self).__init__()
        self.sets = [] # Takes set ids 0,...,n-1 to the universe elements in 0,...,m-1 that are covered by that set (Ordered)
        self.m = 0 # number of elements in the universe
        self.mono = mono # Variable that gives tradeoff between similarity and diversity (how non-mono)
        self.readInstance(args=args)
        self.univ = [True] * len(self.sets)
        if len(self.costs) == 0:
            self.costs = [1.0] * len(self.sets)
        self.unif_cost = unif_cost
        self.calculateMinCost()
        # self.logInstance()
        
    def readInstance(self, args=None):
        max_id = 0
        with open(f"{args.data_dir}", 'r') as f:
            for line in f.readlines():
                if ':' in line:
                    cost_elts = line.strip(',\n ').split(':')
                    cost = float(cost_elts[0])
                    if cost_elts[1] == '':
                        set = []
                    else:
                        set = list(map(int, cost_elts[1].split(',')))
                else:
                    cost = 1
                    elts_line = line.strip(',\n ')
                    # print(f"elts_line is {elts_line}")
                    if elts_line == '':
                        set = []
                    else:
                        set = list(map(int, elts_line.split(',')))
                
                self.costs.append(cost)
                set.sort()
                self.sets.append(set)
                if not len(set) == 0:
                    set_max_id = np.max(set)
                    if set_max_id > max_id:
                        max_id = set_max_id
        self.m = max_id + 1
        
        
    def updateAdd(self, id, soln: SetCoverSolution):
        assert not soln.inSet(id)
        
        # Update covered
        if len(self.sets[id]) > 0:
            for i in self.sets[id]:
                soln.covered[i] += 1
                
        # Update cost        
        soln.cost += self.getCost(id)
        
        # Update sets
        soln.X[id] = True
        soln.X_set.append(id)
        
    def deltaf(self, id):
        assert self.univ[id]
        self.evals += 1
        return len(self.sets[id])
        
    def getNewlyCovered(self, id, soln: SetCoverSolution):
        newly_covered = 0
        for i in self.sets[id]:
            if soln.covered[i] == 0:
                newly_covered += 1
        return newly_covered 
    
    def getSize(self, a):
        assert 0 <= a < len(self.sets)
        return len(self.sets[a])  