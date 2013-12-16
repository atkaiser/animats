'''
Created on Dec 10, 2013

@author: akaiser
'''

from pybrain.rl.environments.environment import Environment
from environment import Env
from grids.grid import Grid

class CarEnvironment(Environment):
    
    def __init__(self):
        self.action = [0.0, 0.0]
        self.delay = False
        self.grid = Grid()
        self.env = Env(self.grid)
        self.reset()

    def step(self):
        # Simulate a step in the environment
        self.agent.brain.stored_action = self.action
        self.env.tick()
        self.env.calculate_moves()
        self.env.do_moves()
        self.env.print_env(self.env.tick_number)
    
    def reset(self):
        self.env.reset()
        self.agent = self.env.cars[0]
        # (x, y, vel, deg, goal_x, goal_y, dist_to_goal, dir_of_goal, direction_diff)
        self.sensors = self.agent.brain.get_state_tuple()
        self.distance_to_goal = self.agent.brain.distance_to_goal()
        
    def getSensors(self):
        # (x, y, vel, deg, goal_x, goal_y, dist_to_goal, dir_of_goal, direction_diff)
        return self.agent.brain.get_state_tuple()
    
    def getCarState(self):
        return self.agent.brain.get_state()
    
    def in_goal_state(self):
        return self.agent.brain.get_state().reached_goal
    
    def performAction(self, action):
        self.action = action
        self.step()
    
    def indim(self):
        return 2
    
    def outdim(self):
        return len(self.getSensors())