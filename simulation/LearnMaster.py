'''
Created on Dec 11, 2013

@author: akaiser
'''

from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.customxml.networkreader import NetworkReader

from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners.directsearch.enac import ENAC
from pybrain.rl.experiments.episodic import EpisodicExperiment
from pybrain.rl.agents import OptimizationAgent
from pybrain.structure.modules.tanhlayer import TanhLayer
from pybrain.optimization import PGPE

from pybrain.tools.shortcuts import buildNetwork

from pybrain.rl.agents import OptimizationAgent

from scipy import mean
import datetime

from CarEnvironment import CarEnvironment
from GoToGoalTask import GoToGoalTask
import variables

def print_connections(n):
    for mod in n.modules:
        for conn in n.connections[mod]:
            print conn
            for cc in range(len(conn.params)):
                print conn.whichBuffers(cc), conn.params[cc]

for i in [5]:
    # create task
    env = CarEnvironment()
    maxsteps = variables.num_of_iterations
    task = GoToGoalTask(env = env, maxsteps = maxsteps)
    
    if i == 0:
        net = buildNetwork(task.outdim(), task.indim(), outclass=TanhLayer)
    else:
        net = buildNetwork(task.outdim(), i+1 ,task.indim(), outclass=TanhLayer)
    
    # create agent
#    learner = ENAC()
##    learner.gd.rprop = False
#    # only relevant for RP
##    learner.gd.deltamin = 0.0001
#    # only relevant for BP
#    learner.gd.alpha = 0.3
#    learner.gd.momentum = 0.0
    
#    agent = LearningAgent(net, learner)
    #agent.actaspg = False
    
    agent = OptimizationAgent(net, PGPE(learningRate = 0.3,
                                    sigmaLearningRate = 0.15,
                                    momentum = 0.0,
                                    epsilon = 2.0,
                                    rprop = False,
                                    storeAllEvaluations = True))
    
    # create experiment
    experiment = EpisodicExperiment(task, agent)
    
    # print weights at beginning
    print agent.module.params
    
    # episodic version
    x = 0
    batch = 1 #number of samples per gradient estimate (was: 20; more here due to stochastic setting)
    while x < 400:
        experiment.doEpisodes(batch)
        x += batch
        if x > 350:
            pass
#        reward = mean(agent.history.getSumOverSequences('reward'))
#        if (x % 100 == 0):
#            print agent.module.params
#        agent.learn()
#        agent.reset()
    
#    folder = 'networks'
#    current_time = str(datetime.datetime.now())
#    filename = folder + '/' + str(reward) + 'dim' + str(task.outdim()) + 't' + current_time + '.xml'
#    NetworkWriter.writeToFile(net, filename)
    
    folder = 'networks'
    current_time = str(datetime.datetime.now())
    filename = folder + '/' + 'dim' + str(task.outdim()) + 't' + current_time + '.xml'
    NetworkWriter.writeToFile(net, filename)

