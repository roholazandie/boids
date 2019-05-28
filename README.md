## What is Boids?
[Boids](https://en.wikipedia.org/wiki/Boids) is an artificial life program developed by Craig Reynolds which simultes the flocking behaviour of birds.As with most artificial life simulations, Boids is an example of emergent behavior; that is, the complexity of Boids arises from the interaction of individual agents (the boids, in this case) adhering to a set of simple rules. The rules applied in the simplest Boids world are as follows:

* separation: steer to avoid crowding local flockmates
* alignment: steer towards the average heading of local flockmates
* cohesion: steer to move towards the average position (center of mass) of local flockmates

## About this repository
This repository tries to reimplement [this](https://www.youtube.com/watch?v=mhjuuHl6qHM) which is in p5.js.
This repo is based on the python version of p5.

## Installation
 Run:
 ```
 sudo apt-get install libglfw3
 ```
 ```
pip install -r requirements.txt
```
For using fast boid:
```
pip install ray
```

## A technical detail
The implemented boid is slow for large number of boids. The fast_boid is a try usign [ray](https://github.com/ray-project/ray) to make it faster. In current implementation, it doesn't make a huge difference though. If someone could figure out to make it faster just send me a push request.
