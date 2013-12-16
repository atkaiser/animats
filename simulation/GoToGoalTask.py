'''
Created on Dec 10, 2013

@author: akaiser
'''

from pybrain.rl.environments import EpisodicTask
import CarEnvironment
import variables

class GoToGoalTask(EpisodicTask):

    def __init__(self, env = None, maxsteps = 1000):
        if env == None:
            env = CarEnvironment()
        EpisodicTask.__init__(self, env)
        self.N = maxsteps
        self.t = 0
        # (vel, deg, dist_to_goal, dir_of_goal, direction_diff)
        self.sensor_limits = [(-30.0, 100.0),
                              (0.0, 360.0),
                              (0.0, variables.grid_size*2),
                              (-180.0, 180.0),
                              (-180.0, 180.0)]
        self.actor_limits = [(-1.0, +4.5), (-90.0, +90.0)]
        self.rewardscale = 100.0 / env.distance_to_goal
        self.total_reward = 0.0
        
    def reset(self):
        EpisodicTask.reset(self)
        self.t = 0
        self.rewardscale = 100.0 / self.env.distance_to_goal
        print self.total_reward
        self.total_reward = 0.0
        
    def performAction(self, action):
        self.t += 1
        EpisodicTask.performAction(self, action)
        
    def isFinished(self):
        if self.t >= self.N:
            return True
        if self.env.in_goal_state():
            return True
        return False
    
    def getReward(self):
        state = self.env.getCarState()
        if state.reached_goal:
            self.total_reward += 1000
            return 1000
        old_dist_to_goal = variables.distance(state.last_x, state.last_y, state.goal_x, state.goal_y)
        new_dist_to_goal = variables.distance(state.x, state.y, state.goal_x, state.goal_y)
        direction_diff = abs(self.env.agent.brain.direction_diff(self.env.agent.brain.get_state()))
        if direction_diff <= 15:
            dir_reward = 1
        elif direction_diff <= 145:
            dir_reward = (-1.0/65.0) * direction_diff + 1.23
        else:
            dir_reward = -1
        self.total_reward += (old_dist_to_goal - new_dist_to_goal) * self.rewardscale * 4 + dir_reward
        return (old_dist_to_goal - new_dist_to_goal) * self.rewardscale * 4 + dir_reward
        
    def setMaxLength(self, n):
        self.N = n