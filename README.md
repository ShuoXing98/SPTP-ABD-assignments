# SPTP-ABD-assignments

## Assignment 1: implementation of connected shape tester for images.
Assignment 1 is the about testing whether a image contains a connected shape consisted by black pixels, through implementing the Algorithm `T3` and `T4` in [this paper](http://people.csail.mit.edu/sofya/pixels.pdf).


### Generate images with connected shape
We randomly generate images which have the target property (connected shape) by random walk of a randomly selected black pixel (every pixel can be repeatedly visited). Suppode the size of the image is `n*n`.

1. Generate a `n*n` empty (all entries are `0`) matrix.