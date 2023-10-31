class Solution:
    
    """Base class for obejctive submodular functions."""

    def __init__(self, n):
        super(Solution, self).__init__()
        
        # Two ways to represent elements in the solution
        self.X = [False] * n
        self.X_set = []
        
        # Store the f value and total cost
        self.f = 0.0
        self.cost = 0.0
        
    def getCost(self):
        return self.cost

    def getSet(self):
        return self.X_set

    def inSet(self, i):
        return self.X[i]
    
    def getf(self):
        return self.f
        
    def updatef(self, deltaf):
        self.f += deltaf
        if self.f < -100:
            print("Error: f value is " + str(self.f))
            
    def empty(self):
        return len(self.X_set) == 0
    
    def getN(self):
        return len(self.X)