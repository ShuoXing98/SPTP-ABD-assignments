import numpy as np
import random
import matplotlib.pyplot as plt 

"""
Radomly generate images that could be in connected shapes by changing no more than epsilon fraction pixels.

The image would only have white and black pixels.

For the image matrix, 0 represents white pixels, and 1 represents balck pixels.

If the shape of the black pixels is connected, we call the image is in a connected shape.    

"""

def random_generate_connected_image(m=10, n=100): # m is the number of the generated images, n is the size of the images 
    generated_images = []
    image_black_pixels = []
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    for _ in range(m):
        image = [[0 for i in range(n)] for j in range(n)]
        black_pixels = []
        i = random.randint(0, n-1)
        j = random.randint(0, n-1)
        image[i][j] = 1
        black_pixels.append((i,j))
        for _ in range(50*n):
            while 1:
                di,dj = random.choice(directions)
                temp_i = i + di
                temp_j = j + dj
                if 0 <= temp_i and temp_i < n and 0 <= temp_j and temp_j < n:
                    image[temp_i][temp_j] = 1
                    black_pixels.append((temp_i,temp_j))
                    i, j = black_pixels[-1]
                    break
        generated_images.append(image) 
        black_pixels = list(set(black_pixels))
        image_black_pixels.append(black_pixels)   
    return generated_images, image_black_pixels

def spec_generate_connected_image(n=100): # s shape
    image = [[0 for i in range(n)] for j in range(n)]
    black_pixels = []
    for i in range(0, n ,4):
        for j in range(n):
            image[i][j] = 1 
            black_pixels.append((i,j))
            image[i+2][j] = 1 
            black_pixels.append((i+2,j))
        image[i+1][0] = 1 
        black_pixels.append((i+1,0))
        image[i+3][n-1] = 1 
        black_pixels.append((i+3,n-1))
    return image, black_pixels 

def delete_epsilon_black_pixels(image, black_pixels, epsilon=0.2):
    size = len(image[0])
    total_deleted_number = int(epsilon * size**2)
    deleted_black_pixels = random.choices(black_pixels, k=total_deleted_number)
    for i,j in deleted_black_pixels:
        image[i][j] = 0
    black_pixels = [item for item in black_pixels if item not in deleted_black_pixels]
    return image, black_pixels

def filp_entry(image, black_pixels, q):
    # connectness = True
    size = len(image[0])
    for i in range(size):
        for j in range(size):
            if random.random() < q:
                if image[i][j] == 0:
                    image[i][j] = 1
                    black_pixels.append((i,j))
                    # if image[i+1][j] == 0 and image[i-1][j] == 0 and image[i][j+1] == 0 and image[i][j-1] == 0:
                    #     connectness = False
                    
                    
                    # for x,y in [(1,0),(-1,0),(0,1),(0,-1)]:
                    #     temp_i = i + x
                    #     temp_j = j + y
                    #     connectness = False
                    #     if 0 <= temp_i and temp_i < size  and 0 <= temp_j and temp_j < size:
                    #         if image[temp_i][temp_j] == 1:
                    #             connectness = False
                    #             break
                                
                        
                else:
                    image[i][j] = 0
                    black_pixels.remove((i,j))
    return image, black_pixels