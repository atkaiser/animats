'''
Created on Nov 5, 2013

@author: akaiser
'''

from cars import car
from grids import grid
import environment
import variables
import simulation.stats as stats

from pybrain.tools.customxml.networkreader import NetworkReader

# Create the map
master_grid = grid.Grid()

# Create environment
env = environment.Env(master_grid)

# Load NN
net = NetworkReader.readFrom('../networks/178.32309862dim5t2013-12-12 11:29:12.948622.xml')
net = None

# Create objects
env.add_cars(nn=net)

# Run simulation
for i in range(variables.num_of_iterations):
    env.tick()
    # Calculate what to do next
    env.calculate_moves()
    # Do it
    env.do_moves()
    # Print results
    env.print_env(i)
    print i
    
# Print statistics
#stats.calculate_stats(env.states)
    
# Find way to show animation
env.show_animation()
    
print "Finished"