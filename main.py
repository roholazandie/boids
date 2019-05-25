from p5 import *
import random
import numpy as np
from boid import Boid
x = 100
y = 100

width = 1000
height = 1000

variance = 100
mean_x = width/2
mean_y = height/2
v1 = Vector(400, 300)
flock = [Boid(*np.random.rand(2)*1000, width, height) for _ in range(30)]


def setup():
    #this happens just once
    size(width, height) #instead of create_canvas


def draw():
    global flock


    background(200, 30, 100)

    for boid in flock:
        boid.edges()
        boid.apply_behaviour(flock)
        boid.update()
        boid.show()


#run(frame_rate=100)
#run(frame_rate=200)
run()