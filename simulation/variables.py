'''
Created on Nov 14, 2013

@author: akaiser
'''

import math

number_of_cars = 10
time_per_iteration = 0.1  # Seconds between iterations
num_of_iterations = 1000
coeffient_of_drag = 0.3
min_dist_to_goal = 1
animation_frame_interval = 5.0  # Number of seconds between the animation frames

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)