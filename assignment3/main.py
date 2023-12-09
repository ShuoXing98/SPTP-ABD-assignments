from Objective.SetCoverJaccard import SetCoverJaccard
from Objective.SetCoverSolution import SetCoverSolution
from Algorithms.ADAPTIVESEQ import AdaptiveSeq
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
    
    greedy_report = {
                'f_val' : [],
                'query_complexity' : [],
                'adaptivity' : []
              }
    
    adpseq_report = {
                'f_val' : [],
                'query_complexity' : [],
                'adaptivity' : []
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
    
    wandb.log({"mono": mono})
    wandb.log({"unif_cost": unif_cost})
    
    
    for value in x_axis_list:
        if x_axis == 'k':
            k = value
        elif x_axis == 'epsilon':
            epsilon = value
    
        wandb.log({"epsilon": epsilon})
        wandb.log({"cardinality-constraint": k}) 
        
        if x_axis == 'k':            
            greedy_objective = SetCoverJaccard(mono, unif_cost=unif_cost, args=args)
            greedy_solution = SetCoverSolution(greedy_objective.getN(), greedy_objective.m)
            greedy = Greedy(greedy_objective, greedy_solution, k=k, args=args)
            greedy_solution, greedy_adaptivity = greedy.run(args)
            greedy_report['f_val'].append(greedy_solution.getf())
            greedy_report['query_complexity'].append(greedy_objective.getEvals())
            greedy_report['adaptivity'].append(greedy_adaptivity)
            
        adpseq_objective = SetCoverJaccard(mono, unif_cost=unif_cost, args=args)
        adpseq_solution = SetCoverSolution(adpseq_objective.getN(), adpseq_objective.m)
        adpseq = AdaptiveSeq(adpseq_objective, adpseq_solution, epsilon=epsilon, k=k, args=args)
        adpseq_solution, adpseq_adaptivity = adpseq.run(args)
        adpseq_report['f_val'].append(adpseq_solution.getf())
        adpseq_report['query_complexity'].append(adpseq_objective.getEvals())
        adpseq_report['adaptivity'].append(adpseq_adaptivity)
    
        wandb.log({"n": adpseq_objective.getN()})
        wandb.log({"m": adpseq_objective.m})
        
        if x_axis == 'k':
            
            wandb.log({"greedy_fval": greedy_solution.getf()})
            wandb.log({"greedy_evals": greedy_objective.getEvals()}) 
        
        wandb.log({"adpseq_fval": adpseq_solution.getf()})
        wandb.log({"adpseq_evals": adpseq_objective.getEvals()}) 
    
    if x_axis == 'k':
        print("\n")
        print("**********The results of algorithm Standard Greedy**********")
        print(f"The value of f is {greedy_report['f_val']}")
        print(f"The number of queries is {greedy_report['query_complexity']}")
        print(f"The number of adaptive rounds is {greedy_report['adaptivity']}")
        
    print("\n")
    print("**********The results of algorithm Adaptive Sequencing**********")
    print(f"The value of f is {adpseq_report['f_val']}")
    print(f"The number of queries is {adpseq_report['query_complexity']}")
    print(f"The number of adaptive rounds is {adpseq_report['adaptivity']}")
    
    plt.figure(1)
    if x_axis == 'k':
        l1, = plt.plot(x_axis_list, greedy_report['f_val'], label='standard greedy')
    l1, = plt.plot(x_axis_list, adpseq_report['f_val'], label='adaptive sequencing')
    plt.xlabel(x_axis)
    plt.ylabel('value of f')
    plt.legend(loc = 'upper right')
    plt.savefig(f'./assignment3/pics/f_val_{x_axis}_cover2500.jpg')
    
    
    plt.figure(2)
    if x_axis == 'k':
        l1, = plt.plot(x_axis_list, greedy_report['query_complexity'], label='standard greedy')
    l1, = plt.plot(x_axis_list, adpseq_report['query_complexity'], label='adaptive sequencing')
    plt.xlabel(x_axis)
    plt.ylabel('query complexity')
    plt.legend(loc = 'upper right')
    plt.savefig(f'./assignment3/pics/query_complexity_{x_axis}_cover2500.jpg')

    plt.figure(3)
    if x_axis == 'k':
        l1, = plt.plot(x_axis_list, greedy_report['adaptivity'], label='standard greedy')
    l1, = plt.plot(x_axis_list, adpseq_report['adaptivity'], label='adaptive sequencing')
    plt.xlabel(x_axis)
    plt.ylabel('adaptivity')
    plt.legend(loc = 'upper right')
    plt.savefig(f'./assignment3/pics/adaptivity_{x_axis}_cover2500.jpg')
    

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
