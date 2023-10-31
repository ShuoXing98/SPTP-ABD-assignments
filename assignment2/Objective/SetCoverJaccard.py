from Objective.SetCover import SetCover
from Objective.SetCoverSolution import SetCoverSolution
import numpy as np
np.random.seed(42)
class SetCoverJaccard(SetCover):
    def __init__(self, mono, unif_cost=False, args=None):
        super(SetCoverJaccard, self).__init__(mono, unif_cost=unif_cost, args=args)
        self.mono = mono
        print("Mono=" + str(self.mono))
        
    def add(self, id, soln: SetCoverSolution):
        assert self.univ[id]
        if soln.inSet(id):
            return
        soln.f += self.deltaf(id, soln, count_eval=False)
        self.updateAdd(id, soln)
        
    def deltaf(self, id, soln: SetCoverSolution, count_eval=True):
        assert self.univ[id]
        if soln.inSet(id):
            return 0.0
        if count_eval:
            self.evals += 1
        return self.getNewlyCovered(id, soln)
    
    def Singletonf(self, id, count_eval=True):
        assert self.univ[id]
        if count_eval:
            self.evals += 1
        return len(self.sets[id])