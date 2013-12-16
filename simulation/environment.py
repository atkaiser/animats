'''
Created on Nov 9, 2013

@author: akaiser
'''

import random
import math
import variables
import matplotlib.pyplot as plt
from matplotlib import animation
from simulation.cars import car

class Env:

    def __init__(self, grid):
        self.tick_number = 0
        self.grid = grid
        self.cars = []
        self.objects = []
        self.states = {}
        self.stored_states = {}
        self.times_reset = 0
        
    def reset(self):
        self.tick_number = 0
        self.cars = []
        self.objects = []
        self.states = {}
        self.stored_states = {}
        self.add_cars()
        self.times_reset += 1
        print "Reset: " + str(self.times_reset)
        
    def add_cars(self, nn=None):
        for i in range(variables.number_of_cars):
            self.add_car(car.Car(3, 5, 320, self, nn=nn))
        
    def add_car(self, car, x=0, y=0, vel=0, deg=0, goal_x=0, goal_y=0, rand=True):
        self.cars.append(car)
        if rand:
            x = random.random()*variables.grid_size
            y = random.random()*variables.grid_size
            deg = random.random()*360
            vel = 0
            goal_x = random.random()*variables.grid_size
            goal_y = random.random()*variables.grid_size
            self.states[car] = State(car.uid,x,y,vel,deg,goal_x,goal_y, random_color())
        else:
            self.states[car] = State(car.uid,x,y,vel,deg,goal_x,goal_y, random_color())
        
    def add_object(self, thing, x=None, y=None):
        self.objects.append(thing)
        
    def tick(self):
        self.tick_number += 1
    
    def do_moves(self):
        for c in self.cars:
            pos = self.states[c]
            if not pos.crashed:
                pos.vel += self.grid.get_accel_with_friction(pos.x, pos.y, pos.vel, c.accel)*variables.time_per_iteration
                pos.deg += c.turn_velocity*variables.time_per_iteration
                pos.deg = pos.deg % 360.0
                pos.last_x = pos.x
                pos.last_y = pos.y
                pos.x += math.cos(math.radians(pos.deg))*pos.vel*variables.time_per_iteration
                pos.y += math.sin(math.radians(pos.deg))*pos.vel*variables.time_per_iteration
                pos.total_dist += pos.vel*variables.time_per_iteration
                if variables.distance(pos.x, pos.y, pos.goal_x, pos.goal_y) < variables.min_dist_to_goal:
                    self.reach_goal(pos)
                else:
                    pos.reached_goal = False
            else:
                if (pos.time_of_last_crash + variables.crash_time) < (variables.time_per_iteration * self.tick_number):
                    pos.crashed = False
        self.crashes()
    
    def reach_goal(self, state):
        state.reached_goal = True
        state.goal_x = random.random()*variables.grid_size
        state.goal_y = random.random()*variables.grid_size
        state.num_goals_reached += 1
        state.dist_of_goals_reached += state.original_dist_to_next_goal
        state.original_dist_to_next_goal = variables.distance(state.x, state.y, state.goal_x, state.goal_y)
        
    def crashes(self):
        keys = self.states.keys()
        for i in range(len(keys)-1):
            for j in range(len(keys)-i-1):
                if (not self.states[keys[i]].crashed) and (not self.states[keys[i+j+1]].crashed):
                    if overlap(keys[i], self.states[keys[i]], keys[i+j+1], self.states[keys[i+j+1]]):
                        print 'Crash'
                        car1_state = self.states[keys[i]]
                        car2_state = self.states[keys[i+j+1]]
                        car1_state.crashed = True
                        car2_state.crashed = True
                        car1_state.num_of_crashes += 1
                        car2_state.num_of_crashes += 1
                        car1_state.time_of_last_crash = variables.time_per_iteration * self.tick_number
                        car2_state.time_of_last_crash = variables.time_per_iteration * self.tick_number
                        car1_state.vel = 0
                        car2_state.vel = 0
                        car1_state.deg = 0
                        car2_state.deg = 180
                        self.move_car_forward(car1_state, variables.distance_after_crash)
                        self.move_car_forward(car2_state, variables.distance_after_crash)
                    
                    
    def move_car_forward(self, state, distance):
        state.x += math.cos(math.radians(state.deg)) * distance
        state.y += math.sin(math.radians(state.deg)) * distance
    
    def calculate_moves(self):
        for c in self.cars:
            c.calculate_move()
        for o in self.objects:
            o.calculate_move()
            
    def print_env(self, iteration_number):
#        for c in self.cars:
#            print self.states[c]
        if ((iteration_number * variables.time_per_iteration) % 1.0 == 0):
            self.store_state()

    def store_state(self):
        state = []
        for c in self.cars:
            car_state = self.states[c]
            state.append((car_state.x, car_state.y, car_state.goal_x, car_state.goal_y, car_state.color))
        self.stored_states[len(self.stored_states)] = state

    def show_animation(self):
        fig = plt.figure()
#        ax = plt.axes(xlim=(-1 * variables.grid_size, variables.grid_size*2), ylim=(-1 * variables.grid_size, variables.grid_size*2))
        ax = plt.axes(xlim=(0, variables.grid_size), ylim=(0, variables.grid_size))
        self.plots = []
        for c in self.cars:
            car, = ax.plot([], [], 'o', color=self.states[c].color)
            dest, = ax.plot([], [], 'x', color=self.states[c].color)
            self.plots += [car, dest]
        
        anim = animation.FuncAnimation(fig, self.animate, init_func=self.init, frames=len(self.stored_states), interval=20)
        plt.show()
        
    def init(self):
        for plot in self.plots:
            plot.set_data([], [])
        return tuple(self.plots)
    
    def animate(self, i):
        stored_state = self.stored_states[i]
        for i in range(len(stored_state)):
            state = stored_state[i]
            car_plot = self.plots[2*i]
            dest_plot = self.plots[2*i + 1]
            car_plot.set_data([state[0]], [state[1]])
            dest_plot.set_data([state[2]], [state[3]])
        return tuple(self.plots)
            
class State:
    
    def __init__(self, uid, x, y, vel, deg, goal_x, goal_y, color):
        self.uid = uid
        self.x = x
        self.y = y
        self.vel = vel
        self.deg = deg
        self.goal_x = goal_x
        self.goal_y = goal_y
        # Stuff for statistics and output
        self.color = color
        self.dist_of_goals_reached = 0
        self.original_dist_to_next_goal = variables.distance(x, y, goal_x, goal_y)
        self.num_goals_reached = 0
        self.total_dist = 0
        # Crash info
        self.crashed = False
        self.num_of_crashes = 0
        self.time_of_last_crash = None
        # Reward info
        self.last_x = x
        self.last_y = y
        self.reached_goal = False
        
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
    if denominator != 0:
        ua = ((xb2 - xb1)*(ya1 - yb1) - (yb2 - yb1)*(xa1 - xb1)) / denominator
        ub = ((xa2 - xa1)*(ya1 - yb1) - (ya2 - ya1)*(xa1 - xb1)) / denominator
    else:
        return False
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
    
def random_color():
    r = random.random()
    g = random.random()
    b = random.random()
    return (r,g,b)
    