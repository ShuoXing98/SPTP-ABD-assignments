import argparse
import wandb
import numpy as np
import matplotlib.pyplot as plt

from generate_data import random_generate_connected_image, spec_generate_connected_image, delete_epsilon_black_pixels, filp_entry
from algorithms import ConnectTest, ImprovedConnectTest

def main(args):
    print("************************************************************")
    print("** epsilon-tester for whether an image is connected shape **")
    print("************************************************************")

    generated_images, image_black_pixels = random_generate_connected_image(m=args.repeat, n=args.size)
    
    t3_report = {
                'false_positive_rate' : [],
                'avg_query_times' : []
              }
    t4_report = {
                'false_positive_rate' : [],
                'avg_query_times' : []
              }
    for q in args.q:
        t3_results = []
        t4_results = []
        t3_ground_truth = [] 
        t4_ground_truth = []
        t3_query_times = []
        t4_query_times = []
        
        for i in range(len(generated_images)):
            image = generated_images[i]
            black_pixels = image_black_pixels[i]    
            image, black_pixels = filp_entry(image, black_pixels, q)
            t3 = ConnectTest(image, black_pixels, epsilon=args.epsilon)
            t4 = ImprovedConnectTest(image, black_pixels, epsilon=args.epsilon)
            
            t3_accept, t3_query_time, t3_connectness = t3.run()
            t4_accept, t4_query_time, t4_connectness = t4.run()
            
            t3_results.append(t3_accept)
            t3_ground_truth.append(t3_connectness)
            t3_query_times.append(t3_query_time)
            
            t4_results.append(t4_accept)
            t4_ground_truth.append(t4_connectness)
            t4_query_times.append(t4_query_time)
        
        t3_false_positive = 0
        t4_false_positive = 0
        
        for i in range(len(t3_ground_truth)):
            if t3_ground_truth[i] == False:
                if t3_results[i] == True:
                    t3_false_positive += 1
            if t4_ground_truth[i] == False:
                if t4_results[i] == True:
                    t4_false_positive += 1
                    
        t3_false_positive_rate = t3_false_positive / args.repeat
        t3_avg_query_times = np.mean(t3_query_times)
        
        t4_false_positive_rate = t4_false_positive / args.repeat
        t4_avg_query_times = np.mean(t4_query_times)
        
        t3_report['false_positive_rate'].append(t3_false_positive_rate)
        t3_report['avg_query_times'].append(t3_avg_query_times)
        
        t4_report['false_positive_rate'].append(t4_false_positive_rate)
        t4_report['avg_query_times'].append(t4_avg_query_times)
        
        wandb.log({"t3_false_positive_rate": t3_false_positive_rate})
        wandb.log({"t3_avg_query_times": t3_avg_query_times})
        
        wandb.log({"t4_false_positive_rate": t4_false_positive_rate})
        wandb.log({"t4_avg_query_times": t4_avg_query_times})
        
        wandb.log({"q": q})
    

    print("\n")
    print("**********The results of algorithm T3**********")
    print(f"The number of queries to the pixels is {t3_report['avg_query_times']}")
    print(f"The false positive rate is {t3_report['false_positive_rate']}")
    
    print("\n")
    print("**********The results of algorithm T4**********")
    print(f"The number of queries to the pixels is {t4_report['avg_query_times']}")
    print(f"The false positive rate is {t4_report['false_positive_rate']}") 
    
    plt.figure(1)
    l1, = plt.plot(args.q, t3_report['false_positive_rate'], label='T3')
    l1, = plt.plot(args.q, t4_report['false_positive_rate'], label='T4')
    plt.xlabel('q')
    plt.ylabel('false positive rate')
    plt.legend(loc = 'upper right')
    plt.savefig(f'./assignment1/pics/false_positive_rate_epsilon_{args.epsilon}.jpg')
    
    
    plt.figure(2)
    l1, = plt.plot(args.q, t3_report['avg_query_times'], label='T3')
    l1, = plt.plot(args.q, t4_report['avg_query_times'], label='T4')
    plt.xlabel('q')
    plt.ylabel('query complexity')
    plt.legend(loc = 'upper right')
    plt.savefig(f'./assignment1/pics/avg_query_times_epsilon_{args.epsilon}.jpg')
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-name', default='epsilon-tester', help='Name of the wandb project')
    parser.add_argument('--epsilon', default=0.1, type=float, help='Value of the input epsilon')
    parser.add_argument('--size', default=1000, type=int, help='Size of the generated image')
    parser.add_argument('--repeat', default=50, type=int, help='The number of repeated trails')
    parser.add_argument('--q', nargs="+", default=[0.001], type=float, help='Value of the probability of flipping each entry in the image matrix')
    parser.add_argument('--wandb-key', default='c9039a6663b7aa3fa1260f5c004c21cce2584bd1', help='Key of your own wandb account') # replace your own wandb key if there are multiple wandb accounts in your server
    args = parser.parse_args()
    wandb.login(key=args.wandb_key)
    wandb.init(project='assignment_big_data')
    wandb.config.update(args)
    
    main(args)