# SPTP-ABD-assignments
Thie repo is for my assignments of the `23 FALL CSCE 689 602: SPTP: ALGORITHMS FOR BIG DATA` which is instructed by Professor [Victoria Crawford](https://engineering.tamu.edu/cse/profiles/crawford-victoria.html) at *Texas A&M University*. 


## Installation
Simple run the following command to create virtual enviornment and install all dependencies automatically.

```
source install.sh
```
## Assignment 1: implementation of connected shape tester for images.
Assignment 1 is the about testing whether a image contains a connected shape consisted by black pixels, through implementing the Algorithm `T3` and `T4` of [this paper](http://people.csail.mit.edu/sofya/pixels.pdf).


### Generate images with connected shape
We randomly generate images which have the target property (connected shape) by random walk of a randomly selected black pixel (every pixel can be repeatedly visited). Suppode the size of the image is `n*n`.

1. Generate an `n*n` empty (all entries are `0`) matrix `M`.
2. Randomly choose a pixel (a `(i,j)` pair), and let `M(i,j) = 1` (which represents blakc pixel).
3. Randomly select the next pixel with directions `(0,1), (0,-1), (1,0), (-1,0)`.
4. Repeat the above process `10*n` times.

We can get an image like the following one:

![Generated Random image with connected shape](https://github.com/ShuoXing98/SPTP-ABD-assignments/blob/main/assignment1/pics/generated_random_image.png)

Then we flip each entry in the image matrix `M` with some probability `q`, where if `q=0` then the image has the property and as `q` gets higher (up to a certain point) the image would get further away from having the connectness property. 

We can get the flipped image of the above one with `q=0.1`:

![Flipped image](https://github.com/ShuoXing98/SPTP-ABD-assignments/blob/main/assignment1/pics/flipped_image.png)

### Implementation
The codes of algorithms `T3` and `T4` can be found in `./assingment1/algorithms`. And one can get the connectness epsilon-testing results (`quert complexity` and `false positive rate`) of the `1000*1000` random image (by repeating `50` times) with `epsilon=0.1` and different `q` just by runing the following command in Terminal with a python evn after cloning this repo:

```
python ./assignment1/main.py \
  --epsilon 0.1   \
  --size 1000  \
  --q 0.0005 0.001 0.0015 0.002 0.0025 0.003 0.0035 0.004 0.0045 0.005 0.0055 0.006
```
 

Or can quick start with the following command:

```
bash assignment1/run.sh
```

And one may get the output like the following:

```
************************************************************
** epsilon-tester for whether an image is connected shape **
************************************************************

**********The results of algorithm T3**********
The number of queries to the pixels is [5703.62, 5604.36, 4981.6, 4328.74, 3902.76, 3408.24, 3283.04, 3117.02, 2949.92, 2735.86]
The false positive rate is [0.96, 0.88, 0.46, 0.1, 0.04, 0.0, 0.0, 0.0, 0.0, 0.0]

**********The results of algorithm T4**********
The number of queries to the pixels is [11016.6, 8296.82, 5020.68, 4044.2, 3584.92, 3264.84, 3117.24, 3030.28, 2863.94, 2687.66]
The false positive rate is [0.64, 0.16, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
```