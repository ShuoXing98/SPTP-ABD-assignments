import argparse
import numpy as np
import wandb

from generate_data import random_generate_connected_image, spec_generate_connected_image, delete_epsilon_black_pixels, filp_entry
from algorithms import ConnectTest, ImprovedConnectTest

def main(args):
    print("************************************************************")
    print("** epsilon-tester for whether an image is connected shape **")
    print("************************************************************")

    generated_images, image_black_pixels = random_generate_connected_image(m=args.repeat, n=args.size)
    
    report = {
                'false_positive_rate' : [],
                'avg_query_times' : []
              }
    for q in args.q:
        results = []
        ground_truth = [] 
        query_times = []
        for i in range(len(generated_images)):
            image = generated_images[i]
            black_pixels = image_black_pixels[i]    
            image, black_pixels = filp_entry(image, black_pixels, q)
            if args.algorithm == 'ct3':
                algorithm = ConnectTest(image, black_pixels, epsilon=args.epsilon)
            elif args.algorithm == 'ct4':
                algorithm = ImprovedConnectTest(image, black_pixels, epsilon=args.epsilon)
            accept, query_time, connectness = algorithm.run()
            results.append(accept)
            ground_truth.append(connectness)
            query_times.append(query_time)
        
        false_positive = 0
        for i in range(len(ground_truth)):
            if ground_truth[i] == False:
                if results[i] == True:
                    false_positive += 1
        false_positive_rate = false_positive / args.repeat
        avg_query_times = np.mean(query_times)
        
        report['false_positive_rate'].append(false_positive_rate)
        report['avg_query_times'].append(avg_query_times)
        
        wandb.log({"false_positive_rate": false_positive_rate})
        wandb.log({"avg_query_times": avg_query_times})
        wandb.log({"q": q})
        
    print(f"The number of queries to the pixels is {report['avg_query_times']}")
    print(f"The false positive rate is {report['false_positive_rate']}")
    # print(f'The ground truth is {ground_truth}')
    # print(f'The results is {results}')
    # print(f'The number of queries to the pixels is {avg_query_times}')
    # print(f'The false positive rate is {false_positive_rate}')    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--algorithm', default="ct3", help='Algorithms for testing properties')
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