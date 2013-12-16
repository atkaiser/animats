'''
Created on Nov 9, 2013

@author: akaiser
'''

class Engine:
    '''
    classdocs
    '''


    def __init__(self, hp):
        '''
        Constructor
        '''
        self.hp = hp
        
    def max_accel(self):
        return self.hp / 3