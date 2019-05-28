import ray
from p5 import *
import numpy as np
from fast_boid.fastboid import Boid, Vec2D


x = 100
y = 100

width = 1000
height = 1000

variance = 100
mean_x = width/2
mean_y = height/2
v1 = Vec2D(400, 300)
ray.init(num_gpus=1)

flock = [Boid(*np.random.rand(2)*1000, width, height) for _ in range(90)]


def show(boid):
    stroke(255)

    # point(self.position.x, self.position.y)
    circle((boid.position.x, boid.position.y), radius=10)

def update(boid):
        boid.position += boid.velocity
        boid.velocity += boid.acceleration
        #limit
        if np.linalg.norm(boid.velocity) > boid.max_speed:
            boid.velocity = boid.velocity / np.linalg.norm(boid.velocity) * boid.max_speed

        boid.acceleration = Vec2D(*np.zeros(2))

@ray.remote
def align(boid, boids):
        steering = Vec2D(*np.zeros(2))
        total = 0
        vec = Vec2D(*np.zeros(2))
        for boid in boids:
            if np.linalg.norm(boid.position - boid.position) < boid.perception:
                vec += boid.velocity
                total += 1
        #print(total)
        if total > 0:
            vec /= total
            steering = Vec2D(vec.x, vec.y)
            steering = (steering / np.linalg.norm(steering)) * boid.max_speed
            steering -= boid.velocity
            #print(np.linalg.norm(steering))
            #steering = (steering /np.linalg.norm(steering)) * self.max_force

        return steering

@ray.remote
def cohesion(boid, boids):
        steering = Vec2D(*np.zeros(2))
        total = 0
        vec = Vec2D(*np.zeros(2))
        for boid in boids:
            if np.linalg.norm(boid.position - boid.position) < boid.perception:
                vec += boid.position
                total += 1
        #print(total)
        if total > 0:
            vec /= total
            steering = Vec2D(vec.x, vec.y)
            steering -= boid.position
            if np.linalg.norm(steering) > 0:
                steering = (steering / np.linalg.norm(steering)) * boid.max_speed
            steering -= boid.velocity
            # print(np.linalg.norm(steering))
            if np.linalg.norm(steering)> boid.max_force:
                steering = (steering /np.linalg.norm(steering)) * boid.max_force

        return steering

@ray.remote
def separation(boid, boids):
    steering = Vec2D(*np.zeros(2))
    total = 0
    vec = Vec2D(*np.zeros(2))
    for boid in boids:
        distance = np.linalg.norm(boid.position - boid.position)
        if boid.position != boid.position and distance < boid.perception:
            diff = boid.position - boid.position
            diff /= distance
            vec += diff
            total += 1
    #print(total)
    if total > 0:
        vec /= total
        steering = Vec2D(*vec)
        if np.linalg.norm(steering) > 0:
            steering = (steering / np.linalg.norm(steering)) * boid.max_speed
        steering -= boid.velocity
        # print(np.linalg.norm(steering))
        if np.linalg.norm(steering)> boid.max_force:
            steering = (steering /np.linalg.norm(steering)) * boid.max_force

    return steering

def apply_behaviour(boid, flock):
    alignment_val = align.remote(boid, flock)
    cohesion_val = cohesion.remote(boid, flock)
    separation_val = separation.remote(boid, flock)

    alignment_val = ray.get(alignment_val)
    cohesion_val = ray.get(cohesion_val)
    separation_val = ray.get(separation_val)

    boid.acceleration += alignment_val
    boid.acceleration += cohesion_val
    boid.acceleration += separation_val



def setup():
    #this happens just once
    size(width, height) #instead of create_canvas


def draw():
    global flock


    background(200, 30, 100)

    for boid in flock:

        if boid.position.x > boid.width:
            boid.position.x = 0
        elif boid.position.x < 0:
            boid.position.x = boid.width

        if boid.position.y > boid.height:
            boid.position.y = 0
        elif boid.position.y < 0:
            boid.position.y = boid.height

        apply_behaviour(boid, flock)
        update(boid)
        show(boid)


#run(frame_rate=100)
#run(frame_rate=200)
run()