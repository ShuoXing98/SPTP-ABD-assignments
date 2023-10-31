from Objective.Solution import Solution


class SetCoverSolution(Solution):
    def __init__(self, n, m):
        super(SetCoverSolution, self).__init__(n)
        self.covered = [0] * m # Takes universe elements between 0,...,m-1 to how many sets in the solution cover them
        
        # The two parts of the objective
        self.f_sim = 0.0 
        self.f_div = 0.0 
        
    def countCovered(self):
        cov = 0
        for item in self.covered:
           if item > 0: 
               cov += 1
        return cov 
