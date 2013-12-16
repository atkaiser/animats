'''
Created on Dec 5, 2013

@author: akaiser
'''

import variables

def calculate_stats(states):
    total_time = variables.time_per_iteration * variables.num_of_iterations
    avg_speed = []
    avg_speed_to_target = []
    total_num_of_crashes = 0
    for car in states.keys():
        state = states[car]
        avg_speed.append( state.total_dist / (total_time - (variables.crash_time * state.num_of_crashes)) )
        avg_speed_to_target.append( ( state.dist_of_goals_reached + (state.original_dist_to_next_goal - variables.distance(state.x, state.y, state.goal_x, state.goal_y))) / total_time )
        total_num_of_crashes += state.num_of_crashes
    total_num_of_crashes = total_num_of_crashes / 2
    print "Number of crashes: " + str(total_num_of_crashes)
    print "Average speed to destination: " + str(sum(avg_speed_to_target) / float(len(avg_speed_to_target)))
    print "Average speed: " + str(sum(avg_speed) / float(len(avg_speed)))
    print "Efficiency: " + str((sum(avg_speed_to_target) / float(len(avg_speed_to_target))) / (sum(avg_speed) / float(len(avg_speed))))