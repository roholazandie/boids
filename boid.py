from p5 import *
import numpy as np

class Boid():

    def __init__(self, x, y, width, height):
        self.position = Vector(x, y)
        vec = (np.random.rand(2) - 0.5)*10

        self.velocity = Vector(*vec)

        vec = (np.random.rand(2) - 0.5)/2
        self.acceleration = Vector(*vec)
        self.max_force = 0.1
        self.max_speed = 5
        self.perception = 100

        self.width = width
        self.height = height



    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        #limit
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

        self.acceleration = Vector(*np.zeros(2))

    def show(self):
        stroke(255)

        #point(self.position.x, self.position.y)
        circle((self.position.x, self.position.y), radius=10)


    def apply_behaviour(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)

        # ray.init()
        # results = ray.get([self.align.remote(boids),
        #                    self.cohesion.remote(boids),
        #                    self.separation.remote(boids)])
        #
        # print(results)

        self.acceleration += separation
        self.acceleration += alignment
        self.acceleration += cohesion


    def edges(self):
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height

    #@ray.remote
    def align(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        vec = Vector(*np.zeros(2))
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < self.perception:
                vec += boid.velocity
                total += 1
        #print(total)
        if total > 0:
            vec /= total
            steering = Vector(*vec)
            steering = (steering /np.linalg.norm(steering)) * self.max_speed
            steering -= self.velocity
            #print(np.linalg.norm(steering))
            #steering = (steering /np.linalg.norm(steering)) * self.max_force

        return steering

    #@ray.remote
    def cohesion(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        vec = Vector(*np.zeros(2))
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < self.perception:
                vec += boid.position
                total += 1
        #print(total)
        if total > 0:
            vec /= total
            steering = Vector(*vec)
            steering -= self.position
            if np.linalg.norm(steering) > 0:
                steering = (steering / np.linalg.norm(steering)) * self.max_speed
            steering -= self.velocity
            # print(np.linalg.norm(steering))
            if np.linalg.norm(steering)> self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force

        return steering

    #@ray.remote
    def separation(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        vec = Vector(*np.zeros(2))
        for boid in boids:
            distance = np.linalg.norm(boid.position - self.position)
            if self.position != boid.position and distance < self.perception:
                diff = self.position - boid.position
                diff /= distance
                vec += diff
                total += 1
        #print(total)
        if total > 0:
            vec /= total
            steering = Vector(*vec)
            if np.linalg.norm(steering) > 0:
                steering = (steering / np.linalg.norm(steering)) * self.max_speed
            steering -= self.velocity
            # print(np.linalg.norm(steering))
            if np.linalg.norm(steering)> self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force

        return steering