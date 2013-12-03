'''
Created on Nov 9, 2013

@author: akaiser
'''

import random
import math
import variables
import matplotlib.pyplot as plt

class Environment:

    def __init__(self, grid):
        self.grid = grid
        self.cars = []
        self.objects = []
        self.states = {}
        
    def add_car(self, car, x=0, y=0, vel=0, deg=0, goal_x=0, goal_y=0, rand=True):
        self.cars.append(car)
        if rand:
            x = random.random()*1000
            y = random.random()*1000
            deg = random.random()*360
#            deg = 180
            vel = 0
            goal_x = random.random()*1000
            goal_y = random.random()*1000
            self.states[car] = State(car.uid,x,y,vel,deg,goal_x,goal_y)
        else:
            self.states[car] = State(car.uid,x,y,vel,deg,goal_x,goal_y)
        
    def add_object(self, thing, x=None, y=None):
        self.objects.append(thing)
    
    def do_moves(self):
        for c in self.cars:
            pos = self.states[c]
            pos.vel += self.grid.get_accel_with_friction(pos.x, pos.y, pos.vel, c.accel)*variables.time_per_iteration
            pos.deg += c.turn_velocity*variables.time_per_iteration
            pos.x += math.cos(math.radians(pos.deg))*pos.vel*variables.time_per_iteration
            pos.y += math.sin(math.radians(pos.deg))*pos.vel*variables.time_per_iteration
            if variables.distance(pos.x, pos.y, pos.goal_x, pos.goal_y) < variables.min_dist_to_goal:
                pos.goal_x = random.random()*1000
                pos.goal_y = random.random()*1000
        self.crashes()
        
    def crashes(self):
        keys = self.states.keys()
        for i in range(len(keys)-1):
            for j in range(len(keys)-i-1):
                if overlap(keys[i], self.states[keys[i]], keys[i+j+1], self.states[keys[i+j+1]]):
                    print 'Crash'
                    print self.states[keys[i]]
                    print self.states[keys[i+j+1]]
                    raise Exception("There was a crash of cars")
    
    def calculate_moves(self):
        for c in self.cars:
            c.calculate_move()
        for o in self.objects:
            o.calculate_move()
            
    def print_env(self, iteration_number):
        x_vals = []
        y_vals = []
        for c in self.cars:
            state = self.states[c]
            x_vals.append(state.x)
            y_vals.append(state.y)
            print state
#        if ((iteration_number * variables.time_per_iteration) % 5.0 == 0):
#            plt.plot(x_vals, y_vals, 'bo')
#            plt.show()
            
class State:
    
    def __init__(self, uid, x, y, vel, deg, goal_x, goal_y):
        self.uid = uid
        self.x = x
        self.y = y
        self.vel = vel
        self.deg = deg
        self.goal_x = goal_x
        self.goal_y = goal_y
        
    def __repr__(self):
        return str(["uid: " + str(self.uid), "x: " + str(self.x), "y: " + str(self.y), 
               "vel: " + str(self.vel), "deg: " + str(self.deg), "goal x: " + str(self.goal_x), "goal y: " + str(self.goal_y)])
            
def overlap(car1, state1, car2, state2):
    rect1 = find_corners(car1, state1)
    rect2 = find_corners(car1, state2)
    lines1 = find_borders(rect1)
    lines2 = find_borders(rect2)
    for l1 in lines1:
        for l2 in lines2:
            if does_cross(l1, l2):
                return True
    if complete_overlap(rect1, rect2):
        return True
    return False
    
def find_corners(car, state):
    corner1 = (state.x, state.y)
    corner2 = (state.x + car.width*(math.cos(math.radians(state.deg - 90))), 
               state.y + car.width*(math.sin(math.radians(state.deg - 90))))
    corner3 = (corner2[0] + car.height*(math.cos(math.radians(state.deg + 180))),
               corner2[1] + car.height*(math.sin(math.radians(state.deg + 180))))
    corner4 = (state.x + car.height*(math.cos(math.radians(state.deg + 180))), 
               state.y + car.height*(math.sin(math.radians(state.deg + 180))))
    return [corner1, corner2, corner3, corner4]
    
def find_borders(rect):
    line1 = (rect[0], rect[1])
    line2 = (rect[1], rect[2])
    line3 = (rect[2], rect[3])
    line4 = (rect[3], rect[0])
    return [line1, line2, line3, line4]
    
def does_cross(l1, l2):
    xa1 = l1[0][0]
    ya1 = l1[0][1]
    xa2 = l1[1][0]
    ya2 = l1[1][1]
    xb1 = l2[0][0]
    yb1 = l2[0][1]
    xb2 = l2[1][0]
    yb2 = l2[1][1]
    denominator = (yb2 - yb1)*(xa2 - xa1) - (xb2 - xb1)*(ya2 - ya1)
    ua = ((xb2 - xb1)*(ya1 - yb1) - (yb2 - yb1)*(xa1 - xb1)) / denominator
    ub = ((xa2 - xa1)*(ya1 - yb1) - (ya2 - ya1)*(xa1 - xb1)) / denominator
    if ua >= 0 and ua <= 1 and ub >= 0 and ub <= 1:
        return True
    else:
        return False

def complete_overlap(rect1, rect2):
    # Test if rect1 is in rect2
    if rect_inside(rect1, rect2):
        return True
    # Test if rect2 is in rect1
    elif rect_inside(rect2, rect1):
        return True
    else:
        return False
    
def rect_inside(rect1, rect2):
    inside = True
    for point in rect1:
        borders = find_borders(rect2)
        for edge in borders:
            A = -1 * (edge[1][1] - edge[0][1])
            B = edge[1][0] - edge[0][0]
            C = -1 * (A * edge[0][0] + B * edge[0][1])
            D = A * point[0] + B * point[1] + C
            if D < 0:
                inside = False
                break
        if not inside:
            break
    if inside:
        return True
    else:
        return False
    
    