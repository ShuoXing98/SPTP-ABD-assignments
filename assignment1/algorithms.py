import random
import copy
import math

class algorithm:
    def __init__(self, image, black_pixels, epsilon=0.2, args=None):
        super(algorithm, self).__init__()
        self.image = image
        self.black_pixels = black_pixels
        self.epsilon = epsilon
        self.query_times = 0
        self.image_size = len(self.image[0])
        self.d = 4 / self.epsilon ** 2
        
    def query(self, i, j):
        self.query_times += 1
        return self.image[i][j]
    
    
    
    def random_query_list(self, query_number, tabu=None): # tabu is the section of the pixels which are not allowed to query
        query_list = []
        for _ in range(query_number):
            n = self.image_size
            if not tabu is None:
                while 1:
                    i = random.randint(0, n-1)
                    j = random.randint(0, n-1)
                    if i not in tabu[0] and j not in tabu[1]:
                        query_list.append((i,j))
                        break
            else:
                i = random.randint(0, n-1)
                j = random.randint(0, n-1)
                query_list.append((i,j))
        return query_list
    
    def BFS(self, i, j, bound):
        queue = []
        queue.append((i,j))
        query_history = copy.deepcopy(queue)
        count_black_pixels = 1
        if_stop = False
        while queue:
            current_len = len(queue)
            for _ in range(current_len):
                i,j = queue.pop(0)
                for x,y in [(1,0),(-1,0),(0,1),(0,-1)]:
                    temp_i = i + x
                    temp_j = j + y
                    if 0 <= temp_i and temp_i < self.image_size  and 0 <= temp_j and temp_j < self.image_size  and (temp_i, temp_j) not in query_history:
                        query_history.append((temp_i,temp_j))
                        if self.query(temp_i, temp_j) == 1:
                            queue.append((temp_i,temp_j))  
                            count_black_pixels += 1
                    if count_black_pixels >= bound:
                        if_stop = True
                        break
                if if_stop:
                    break  
            if if_stop:
                break
            
        return count_black_pixels      
    
    def outside_d_square(self, i, j):
        exist_black = False
        tabu = []
        tabu.append(list(range(i-self.d, i+self.d+1)))
        tabu.append(list(range(j-self.d, j+self.d+1)))
        random_query_list = self.random_query_list(int(2/self.epsilon), tabu)
        for i,j in random_query_list:
            if self.query(i,j) == 1:
                exist_black = True
                break
        return exist_black

class ConnectTest(algorithm):
    
    def __init__(self, image, black_pixels, epsilon=0.2, args=None):
        super(ConnectTest, self).__init__(image, black_pixels, epsilon=epsilon, args=args)
        self.delta = self.epsilon ** 2  / 4
        
    def run(self):
        self.d = round(self.d)
        accept = True
        random_query_list = self.random_query_list(math.ceil(2/self.delta))
        for i,j in random_query_list:
            if self.query(i,j) == 1:
                count_black_pixels = self.BFS(i,j,self.d)
                if count_black_pixels < self.d: # a small connected component is found 
                    if self.outside_d_square(i,j):
                        accept = False
                        return accept, self.query_times
        return accept, self.query_times
    
class ImpovedConnectTest(algorithm):
    
    def __init__(self, image, black_pixels, epsilon=0.2, args=None):
        super(ConnectTest, self).__init__(image, black_pixels, epsilon=epsilon, args=args)
        self.delta = self.epsilon ** 2  / 4
        
    def run(self):
        self.d = round(self.d)
        accept = True
        random_query_list = self.random_query_list(math.ceil(2/self.delta))
        for l in range(1,math.ceil(math.log(self.d))):
            random_query_list = self.random_query_list(math.ceil(4 * math.log(self.d) / (self.delta * 2 ** l)))
            for i,j in random_query_list:
                if self.query(i,j) == 1:
                    count_black_pixels = self.BFS(i,j,2**l)
                    if count_black_pixels < 2**l: # a small connected component is found 
                        if self.outside_d_square(i,j):
                            accept = False
                            return accept, self.query_times
        return accept, self.query_times
        
    
        
     