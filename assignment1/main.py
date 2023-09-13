import argparse
import wandb

from generate_data import random_generate_connected_image, spec_generate_connected_image, delete_epsilon_black_pixels
from algorithms import ConnectTest

def main(args):
    print("************************************************************")
    print("** epsilon-tester for whether an image is connected shape **")
    print("************************************************************")
    
    

# class Solution:
#     def orangesRotting(self, grid):
#         row = len(grid)
#         col = len(grid[0])
#         if row == 1 and col == 1 and grid[0][0] != 1:
#             return 0
#         queue = []  # 先进先出 队列
#         for i in range(row):
#             for j in range(col):
#                 if grid[i][j] == 2:
#                     queue.append((i,j))
#         time = -1
#         while queue:
#             current_len = len(queue)
#             for _ in range(current_len):
#                 i,j = queue.pop(0)
#                 for x,y in [(1,0),(-1,0),(0,1),(0,-1)]:
#                     temp_i = i + x
#                     temp_j = j + y
#                     if 0 <= temp_i and temp_i < row and 0 <= temp_j and temp_j < col and grid[temp_i][temp_j] == 1:
#                         grid[temp_i][temp_j] = 2
#                         queue.append((temp_i,temp_j))
#             time += 1
        
#         for eachrow in grid:
#             if 1 in eachrow:
#                 return -1
#         return time
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--algorithm', default="ct3", help='Algorithms for testing properties')
    parser.add_argument('--project-name', default='epsilon-tester', help='Name of the wandb project')
    parser.add_argument('--application', default='setcover', help='Type of applications')
    parser.add_argument('--epsilon', default=0.3, type=float, help='Value of the input epsilon') # 小一点 bound有意义
    parser.add_argument('--wandb-key', default='c9039a6663b7aa3fa1260f5c004c21cce2584bd1', help='Key of your own wandb account') # replace your own wandb key if there are multiple wandb accounts in your server
    args = parser.parse_args()
    wandb.login(key=args.wandb_key) 
    # wandb.init(project=args.project_name, name=args.meta_name)
    wandb.init(project=args.project_name)
    wandb.config.update(args)
    
    main(args)