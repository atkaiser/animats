'''
Created on Nov 5, 2013

@author: akaiser
'''

from cars import car
from grids import grid
import environment
import variables

# Create the map
master_grid = grid.Grid()

# Create environment
env = environment.Environment(master_grid)

# Create objects
for i in range(variables.number_of_cars):
    env.add_car(car.Car(3, 5, 320, env))

# Run simulation
for i in range(variables.num_of_iterations):
    # Calculate what to do next
    env.calculate_moves()
    # Do it
    env.do_moves()
    # Print results
    env.print_env(i)
    
print "Finished"