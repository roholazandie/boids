from p5 import setup, draw, size, background, run
import numpy as np
from boid import Boid


width = 1000
height = 1000

flock = [Boid(*np.random.rand(2)*1000, width, height) for _ in range(50)]


def setup():
    #this happens just once
    size(width, height) #instead of create_canvas


def draw():
    global flock


    background(30, 30, 47)

    for boid in flock:
        boid.edges()
        boid.apply_behaviour(flock)
        boid.update()
        boid.show()


#run(frame_rate=100)
#run(frame_rate=200)
run()