# potential-octo-funicular

This is an implementation of the [QuadTree](https://en.wikipedia.org/wiki/Quadtree) data structure based on a video made by [Daniel Shiffman](https://shiffman.net/), a.k.a., [The Coding Train](https://thecodingtrain.com/). QuadTrees have a myriad of applications, including image processing, collision detection, and even simulation Conway's game of life. I'm hoping to explore most of these at some point within this repository.

## Dependencies
* numpy
* matplotlib


## Query Images
![Successful query of rectangular region](https://github.com/sdawley1/potential-octo-funicular/blob/main/images/query_success.png?raw=true)

![Successful query of rectangular region w/ QuadTree displayed](https://github.com/sdawley1/potential-octo-funicular/blob/main/images/query_success_outlines.png?raw=true)


## Two Closest Schools in Vermont
A friend of mine generated an algorithm for determining the two closest schools in VT in O(nlogn) using Java (which can be found [here](https://github.com/jamiehax/closest-schools)). Since a QuadTree is well-suited for two-dimensional spatial data and is capable of operating at O(logn) time for querying the points, I figured I could try and write an algorithm that outperforms his. Whether or not I actually achieve that goal is better left to someone who understands time complexity, but nevertheless this method affords the correct answer (for anyone interested, the answer is, unsurprisingly, People's Academy and People's Academy Middle School). Below is a visualization of the schools with a QuadTree overlayed on the state. Also, the data can be found [here](https://geodata.vermont.gov/).

![Two closest schools in VT](https://github.com/sdawley1/potential-octo-funicular/blob/main/images/closest_schools.png?raw=true)
![Two closest schools in VT 2](https://github.com/sdawley1/potential-octo-funicular/blob/main/images/closest_schools_zoom.png?raw=true)

