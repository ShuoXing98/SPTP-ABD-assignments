# SPTP-ABD-assignments

## Assignment 1: implementation of connected shape tester for images.
Assignment 1 is the about testing whether a image contains a connected shape consisted by black pixels, through implementing the Algorithm `T3` and `T4` in [this paper](http://people.csail.mit.edu/sofya/pixels.pdf).


### Generate images with connected shape
We randomly generate images which have the target property (connected shape) by random walk of a randomly selected black pixel (every pixel can be repeatedly visited). Suppode the size of the image is `n*n`.

1. Generate an `n*n` empty (all entries are `0`) matrix `M`.
2. Randomly choose a pixel (`(i,j)` pair for the matrix), and let `M(i,j) = 1` (which represents blakc pixel).
3. Randomly select the next pixel with directions `(0,1), (0,-1), (1,0), (-1,0)`.
4. Repeat the above process `10*n` times.

We can get an image like the following one:

![Generated Random image with connected shape](https://github.com/ShuoXing98/SPTP-ABD-assignments/blob/main/assignment1/pics/random_connect_image.png)

Then we flip each entry in the image matrix `M` with some probability `q`, where if `q=0` then the image has the property and as `q` gets higher (up to a certain point) the image would get further away from having the connectness property. 

We can get the flipped image of the above one with `q=0.2`:
