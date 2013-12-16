'''
Created on Dec 4, 2013

@author: akaiser
'''

import math

class Brain():

    def __init__(self, car, nn=None):
        self.car = car
        self.stored_action = None
        self.nn = nn
        
    def calculate_move(self):
        if self.stored_action:
            return self.stored_action
        elif self.nn:
            nn_response = self.nn.activate(self.get_state_tuple())
            accel = nn_response[0]
            direction_difference = nn_response[1]
        else:
            state = self.get_state()
            direction_difference = self.direction_diff(state)
            if direction_difference > 90:
                direction_difference = 90
            elif direction_difference < -90:
                direction_difference = -90
            if direction_difference > 0:
                direction_difference += .5
            elif direction_difference < 0:
                direction_difference -= .5
            if abs(direction_difference > 10):
                if state.vel > 1:
                    accel = 0
                else:
                    accel = .5
            else:
                accel = 5
        return accel, direction_difference
        
    def direction_of_goal(self):
        state = self.get_state()
        delta_x = state.x - state.goal_x
        delta_y = state.y - state.goal_y
        return math.atan2(delta_y, delta_x) * (180 / math.pi)
    
    def distance_to_goal(self):
        state = self.get_state()
        delta_x = state.x - state.goal_x
        delta_y = state.y - state.goal_y
        return math.sqrt(delta_x**2 + delta_y**2)
    
    def direction_diff(self, state):
        direction_difference = state.deg - self.direction_of_goal()
        if direction_difference < -180:
            direction_difference = direction_difference + 360
        elif direction_difference > 180:
            direction_difference = direction_difference - 360
        return direction_difference
    
    def get_state(self):
        return self.car.env.states[self.car]
    
    def get_state_tuple(self):
        # (vel, deg, dist_to_goal, dir_of_goal, direction_diff)
        state = self.get_state()
        return (state.vel,
                state.deg,
                self.distance_to_goal(),
                self.direction_of_goal(),
                self.direction_diff(state))
        
        