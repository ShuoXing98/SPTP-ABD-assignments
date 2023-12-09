from Objective.SetCoverJaccard import SetCoverJaccard
from Objective.SetCoverSolution import SetCoverSolution
from Algorithms.THRESSTREAM import ThresStream
from Algorithms.GREEDY import Greedy
from Algorithms.RESERVOIRSAMPLING import Reservoirsampling
from utils.logger import setup_logger
import argparse
import wandb
import matplotlib.pyplot as plt

def print_args(args):
    print("***************")
    print("** Arguments **")
    print("***************")
    optkeys = list(args.__dict__.keys())
    optkeys.sort()
    for key in optkeys:
        print("{}: {}".format(key, args.__dict__[key]))

def main(args):
    
    print_args(args)
    setup_logger(args.log_dir)
    mono = args.mono
    unif_cost = args.unif_cost
    
    sample_report = {
                'f_val' : [],
                'query_complexity' : []
              }
    greedy_report = {
                'f_val' : [],
                'query_complexity' : []
              }
    
    thres_report = {
                'f_val' : [],
                'query_complexity' : []
              }
    
    print("*******************************")
    print("** Using Set Cover Objective **")
    print("*******************************")
        
    if len(args.epsilon) == 1:  
        x_axis = 'k'
        x_axis_list = args.car_cons
        epsilon = args.epsilon[0]
    elif len(args.car_cons) == 1:
        x_axis = 'epsilon'
        x_axis_list = args.epsilon
        k = args.car_cons[0]
        
    # k = args.car_cons
    # epsilon = args.epsilon[0]
    
    
    wandb.log({"mono": mono})
    wandb.log({"unif_cost": unif_cost})
    
    
    for value in x_axis_list:
        if x_axis == 'k':
            k = value
        elif x_axis == 'epsilon':
            epsilon = value
    
    # if args.algorithm == "threshold":
    #     algorithm =  ThresStream(objective, solution, k=k, epsilon=epsilon, args=args)  
        
    # if args.algorithm == "greedy":
    #     algorithm =  Greedy(objective, solution, k=k, args=args)     
        
    # if args.algorithm == "sample":
    #     algorithm =  Reservoirsampling(objective, solution, k=k, args=args) 
        wandb.log({"epsilon": epsilon})
        wandb.log({"cardinality-constraint": k}) 
        
        if x_axis == 'k':
            sample_objective = SetCoverJaccard(mono, unif_cost=unif_cost, args=args)
            sample_solution = SetCoverSolution(sample_objective.getN(), sample_objective.m)
            sample = Reservoirsampling(sample_objective, sample_solution, k=k, args=args) 
            sample_solution = sample.run(args)
            sample_report['f_val'].append(sample_solution.getf())
            sample_report['query_complexity'].append(sample_objective.getEvals())
            
            greedy_objective = SetCoverJaccard(mono, unif_cost=unif_cost, args=args)
            greedy_solution = SetCoverSolution(greedy_objective.getN(), greedy_objective.m)
            greedy = Greedy(greedy_objective, greedy_solution, k=k, args=args)
            greedy_solution = greedy.run(args)
            greedy_report['f_val'].append(greedy_solution.getf())
            greedy_report['query_complexity'].append(greedy_objective.getEvals())
            
        thres_objective = SetCoverJaccard(mono, unif_cost=unif_cost, args=args)
        thres_solution = SetCoverSolution(thres_objective.getN(), thres_objective.m)
        thres = ThresStream(thres_objective, thres_solution, k=k, epsilon=epsilon, args=args)
        thres_solution = thres.run(args)
        thres_report['f_val'].append(thres_solution.getf())
        thres_report['query_complexity'].append(thres_objective.getEvals())
    
    # solution = algorithm.run(args)
    
    # print(f"algrithm={args.algorithm} n={objective.getN()} m={objective.m} mono={mono} constraint={k} epsilon={epsilon} fval={solution.getf()} evals={objective.getEvals()}\n")
    
        wandb.log({"n": thres_objective.getN()})
        wandb.log({"m": thres_objective.m})
        
        if x_axis == 'k':
            wandb.log({"sample_fval": sample_solution.getf()})
            wandb.log({"sample_evals": sample_objective.getEvals()}) 
            
            wandb.log({"greedy_fval": greedy_solution.getf()})
            wandb.log({"greedy_evals": greedy_objective.getEvals()}) 
        
        wandb.log({"thres_fval": thres_solution.getf()})
        wandb.log({"thres_evals": thres_objective.getEvals()}) 
    
    if x_axis == 'k':
        print("\n")
        print("**********The results of algorithm Reservoir Sampling**********")
        print(f"The value of f is {sample_report['f_val']}")
        print(f"The number of queries is {sample_report['query_complexity']}")
        
        print("\n")
        print("**********The results of algorithm Standard Greedy**********")
        print(f"The value of f is {greedy_report['f_val']}")
        print(f"The number of queries is {greedy_report['query_complexity']}")
        
    print("\n")
    print("**********The results of algorithm Threshold Streaming**********")
    print(f"The value of f is {thres_report['f_val']}")
    print(f"The number of queries is {thres_report['query_complexity']}")
    
    plt.figure(1)
    if x_axis == 'k':
        l1, = plt.plot(x_axis_list, sample_report['f_val'], label='reservoir sampling')
        l1, = plt.plot(x_axis_list, greedy_report['f_val'], label='standard greedy')
    l1, = plt.plot(x_axis_list, thres_report['f_val'], label='streaming threshold')
    plt.xlabel(x_axis)
    plt.ylabel('value of f')
    plt.legend(loc = 'upper right')
    plt.savefig(f'./assignment2/pics/f_val_{x_axis}.jpg')
    
    
    plt.figure(2)
    if x_axis == 'k':
        l1, = plt.plot(x_axis_list, sample_report['query_complexity'], label='reservoir sampling')
        l1, = plt.plot(x_axis_list, greedy_report['query_complexity'], label='standard greedy')
    l1, = plt.plot(x_axis_list, thres_report['query_complexity'], label='streaming threshold')
    plt.xlabel(x_axis)
    plt.ylabel('query complexity')
    plt.legend(loc = 'upper right')
    plt.savefig(f'./assignment2/pics/query_complexity_{x_axis}.jpg')
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-dir', default='logs/', help='Path to store logs of experiments')
    parser.add_argument('--data-dir', default='assignment2/data/corel.txt', help='Path to the dataset')
    parser.add_argument('--project-name', default='submodular-optimizition', help='Name of the wandb project')
    parser.add_argument('--epsilon', nargs="+", default=[0.3], type=float, help='Value of the input epsilon') 
    parser.add_argument('--mono', default=0.0, type=float, help='Value of the variable that gives tradeoff between similarity and diversity for Set Cover')
    parser.add_argument("--unif-cost", action="store_true", help="Whether to use uniform cost")
    parser.add_argument("--car-cons", nargs="+", default=[100], type=int, help="Cardinality constraints")
    parser.add_argument('--wandb-key', default='c9039a6663b7aa3fa1260f5c004c21cce2584bd1', help='Key of your own wandb account') # replace your own wandb key if there are multiple wandb accounts in your server
    args = parser.parse_args()
    
    wandb.login(key=args.wandb_key) 
    wandb.init(project=args.project_name)
    wandb.config.update(args)
    
    main(args)
