'''
Created on Nov 5, 2013

@author: akaiser
'''
import simulation.variables as variables

class Grid(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def get_accel_with_friction(self, x, y, vel, accel):
        # different friction based on if your braking or accelerating
        # TODO!
        if abs(accel) > 0:
            return accel - (vel**3)*variables.coeffient_of_drag
        else:
            return (1 * accel) - (vel**3)*variables.coeffient_of_drag