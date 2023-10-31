from Objective.SetCoverJaccard import SetCoverJaccard
from Objective.SetCoverSolution import SetCoverSolution
from Algorithms.THRESSTREAM import ThresStream
from Algorithms.GREEDY import Greedy
from Algorithms.RESERVOIRSAMPLING import Reservoirsampling
from utils.logger import setup_logger
import argparse
import wandb

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
    
    if args.application == 'setcover':
        print("*******************************")
        print("** Using Set Cover Objective **")
        print("*******************************")

    if args.application == 'setcover':
        objective = SetCoverJaccard(mono, unif_cost=unif_cost, args=args)
        solution = SetCoverSolution(objective.getN(), objective.m)
    
    k = args.car_cons
    epsilon = args.epsilon[0]
    
    wandb.log({"epsilon": epsilon})
    wandb.log({"mono": mono})
    wandb.log({"unif_cost": unif_cost})
    wandb.log({"cardinality-constraint": k}) 
    
    if args.algorithm == "threshold":
        algorithm =  ThresStream(objective, solution, k=k, epsilon=epsilon, args=args)  
        
    if args.algorithm == "greedy":
        algorithm =  Greedy(objective, solution, k=k, args=args)     
        
    if args.algorithm == "sample":
        algorithm =  Reservoirsampling(objective, solution, k=k, args=args) 

    solution = algorithm.run(args)
    
    print(f"algrithm={args.algorithm} n={objective.getN()} m={objective.m} mono={mono} constraint={k} epsilon={epsilon} fval={solution.getf()} evals={objective.getEvals()}\n")
    
    wandb.log({"n": objective.getN()})
    wandb.log({"m": objective.m})
    wandb.log({"fval": solution.getf()})
    wandb.log({"evals": objective.getEvals()}) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--algorithm', default="atg", help='Algorithms for submodular optimizition')
    parser.add_argument('--log-dir', default='logs/', help='Path to store logs of experiments')
    parser.add_argument('--data-dir', default='Data/corel.txt', help='Path to the dataset')
    parser.add_argument('--project-name', default='submodular-optimizition', help='Name of the wandb project')
    parser.add_argument('--application', default='setcover', help='Type of applications')
    parser.add_argument('--epsilon', nargs="+", default=[0.3], type=float, help='Value of the input epsilon') 
    parser.add_argument('--mono', default=0.0, type=float, help='Value of the variable that gives tradeoff between similarity and diversity for Set Cover')
    parser.add_argument("--unif-cost", action="store_true", help="Whether to use uniform cost")
    parser.add_argument("--car-cons", default=100, type=int, help="Cardinality constraints")
    parser.add_argument('--wandb-key', default='c9039a6663b7aa3fa1260f5c004c21cce2584bd1', help='Key of your own wandb account') # replace your own wandb key if there are multiple wandb accounts in your server
    args = parser.parse_args()
    
    wandb.login(key=args.wandb_key) 
    wandb.init(project=args.project_name)
    wandb.config.update(args)
    
    main(args)
