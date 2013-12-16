'''
Created on Nov 5, 2013

@author: akaiser
'''

from motors import engine
from brain import brain

class Car:
    num_of_cars = 0
    all_cars = {}

    def __init__(self, width, height, hp, env, nn=None):
        self.uid = Car.num_of_cars
        Car.num_of_cars += 1
        Car.all_cars[self.uid] = self
        self.width = width
        self.height = height
        self.motor = engine.Engine(hp)
        self.env = env
        self.brain = brain.Brain(self, nn)
        self.accel = 0  # this is in m/s
        self.turn_velocity = 0 # deg/sec
        self.max_turn_radius = 90
        self.max_turn_velocity = 90 # deg/sec
        
    def calculate_move(self):
        self.accel, self.turn_velocity = self.brain.calculate_move()