# SPTP-ABD-assignments
Thie repo is for Shuo Xing's assignments of the class `23 FALL CSCE 689 602: SPTP: ALGORITHMS FOR BIG DATA` which is instructed by Professor [Victoria Crawford](https://engineering.tamu.edu/cse/profiles/crawford-victoria.html) at Texas A&M University. 


## Installation
Simple run the following command to create virtual enviornment and install all dependencies automatically.

```
source install.sh
```
## Assignment 1: implementation of connected shape tester for images.
Assignment 1 is the about testing whether a image contains a connected shape consists of black pixels, through implementing the Algorithm `T3` and `T4` of [this paper](http://people.csail.mit.edu/sofya/pixels.pdf).

### Generate images with connected shape
Suppode the size of the image is `n*n`. The random image which has the connectivity property are generated through random walk initiated from a randomly selected black pixel by the following steps. 

1. Generate an `n*n` empty (all entries are `0`) matrix `M`.
2. Randomly choose a pixel (a `(i,j)` pair), and let `M(i,j) = 1`.
3. Randomly select the next pixel `(i+di, j+di)` with `(di, dj) \in {(0,1), (0,-1), (1,0), (-1,0)}`, and let `M(i+di, j+di) = 1`.
4. Repeat the above process `50*n` times, and every pixel can be repeatedly visited.

Then flip each entry `M(i,j)` in the image matrix `M` with some probability `q`, where if `q=0` then the image has the property and as `q` gets higher (up to a certain point) the image would get further away from having the connectivity property. Here is an example of a randomly generated image with and the corresponding flipped image with `q=0.1`:

<img src="https://github.com/ShuoXing98/SPTP-ABD-assignments/blob/main/assignment1/pics/generated_image.png" alt="Image" width="400"><img src="https://github.com/ShuoXing98/SPTP-ABD-assignments/blob/main/assignment1/pics/flipped_image.png" alt="Image" width="400">

<!-- ![Generated Random image with connected shape](https://github.com/ShuoXing98/SPTP-ABD-assignments/blob/main/assignment1/pics/generated_image.png) -->



<!-- The following flipped image of the generated image can be obtained by setting `q` to `0.1`: -->

<!-- ![Flipped image](https://github.com/ShuoXing98/SPTP-ABD-assignments/blob/main/assignment1/pics/flipped_image.png) -->

### Implementation
The core code of algorithms `T3` and `T4` can be found in `./assingment1/algorithms`. And the connectivity epsilon-testing results (includes `query complexity` and `false positive rate`) of a `1000*1000` random image (by repeating `50` times) with `epsilon=0.1` and different `q` can be obtained just by runing the following command:

```
python ./assignment1/main.py \
  --epsilon 0.1   \
  --size 1000  \
  --q 0.0005 0.001 0.0015 0.002 0.0025 0.003 0.0035 0.004 0.0045 0.005 0.0055 0.006
```
 

Or quick start with the following command:

```
bash assignment1/run.sh
```

And output like the following can be obtained after about `2 hrs`:

```
************************************************************
** epsilon-tester for whether an image is connected shape **
************************************************************

**********The results of algorithm T3**********
The number of queries to the pixels is [21661.34, 21220.14, 19691.7, 18483.54, 17360.62, 15799.54, 14183.4, 12958.64, 12084.32, 11685.7, 10829.08, 10055.66]
The false positive rate is [0.96, 0.86, 0.62, 0.4, 0.24, 0.1, 0.06, 0.0, 0.02, 0.0, 0.0, 0.0]

**********The results of algorithm T4**********
The number of queries to the pixels is [24111.2, 20251.96, 17131.34, 15940.56, 15367.88, 14159.64, 12843.82, 11981.5, 11320.4, 11197.64, 10545.36, 9766.64]
The false positive rate is [0.66, 0.18, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
```

Also we can get the following plots (which are saved in `./assignment1/pics`):

<!-- ![False positive rate](https://github.com/ShuoXing98/SPTP-ABD-assignments/blob/main/assignment1/pics/false_positive_rate_epsilon_0.1_50n.jpg) -->

<!-- ![Query complexity](https://github.com/ShuoXing98/SPTP-ABD-assignments/blob/main/assignment1/pics/avg_query_times_epsilon_0.1_50n.jpg){width=400px} -->

<img src="https://github.com/ShuoXing98/SPTP-ABD-assignments/blob/main/assignment1/pics/false_positive_rate_epsilon_0.1_50n.jpg" alt="Image" width="400"><img src="https://github.com/ShuoXing98/SPTP-ABD-assignments/blob/main/assignment1/pics/avg_query_times_epsilon_0.1_50n.jpg" alt="Image" width="400">