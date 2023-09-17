# SPTP-ABD-assignments
Thie repo is for my assignments of the `23 FALL CSCE 689 602: SPTP: ALGORITHMS FOR BIG DATA` which is instructed by Professor [Victoria Crawford](https://engineering.tamu.edu/cse/profiles/crawford-victoria.html) at *Texas A&M University*. 
## Assignment 1: implementation of connected shape tester for images.
Assignment 1 is the about testing whether a image contains a connected shape consisted by black pixels, through implementing the Algorithm `T3` and `T4` of [this paper](http://people.csail.mit.edu/sofya/pixels.pdf).


### Generate images with connected shape
We randomly generate images which have the target property (connected shape) by random walk of a randomly selected black pixel (every pixel can be repeatedly visited). Suppode the size of the image is `n*n`.

1. Generate an `n*n` empty (all entries are `0`) matrix `M`.
2. Randomly choose a pixel (`(i,j)` pair for the matrix), and let `M(i,j) = 1` (which represents blakc pixel).
3. Randomly select the next pixel with directions `(0,1), (0,-1), (1,0), (-1,0)`.
4. Repeat the above process `10*n` times.

We can get an image like the following one:

![Generated Random image with connected shape](https://github.com/ShuoXing98/SPTP-ABD-assignments/blob/main/assignment1/pics/generated_random_image.png)

Then we flip each entry in the image matrix `M` with some probability `q`, where if `q=0` then the image has the property and as `q` gets higher (up to a certain point) the image would get further away from having the connectness property. 

We can get the flipped image of the above one with `q=0.2`:

![Flipped image](https://github.com/ShuoXing98/SPTP-ABD-assignments/blob/main/assignment1/pics/flipped_image.png)

### Implementation
The codes of algorithms `T3` and `T4` can be found in `./assingment1/algorithms`. And one can just runing the following command in terminals with a python evn after clone this repo:

```
python ./assignment1/main.py \
  --algorithm "ct3"  \
  --epsilon 0.1   \
  --size 1000  \
  --q 0.001 0.002 0.003 0.004 0.005 0.006 0.007 0.008 0.009 0.01
```
 

Or one can quick start with the following command:

```
bash run.sh
```

And one may get the output like the following:

```
************************************************************
** epsilon-tester for whether an image is connected shape **
************************************************************
The number of queries to the pixels is [5909.06, 5728.82, 5432.36, 4588.7, 3932.64, 3662.78, 3507.94, 3325.42, 3092.06, 2918.48]
The false positive rate is [0.96, 0.84, 0.58, 0.12, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0]
```