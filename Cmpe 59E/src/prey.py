'''
Created on Nov 21, 2016

@author: miracgoksuozturk
'''
from agent import Agent

class Prey(Agent):
    
    def __init__(self, x, y, speed, ID, alpha, R, gNumber):
        Agent.__init__(self, x, y, speed, ID, alpha, R)
        self.gNumber = gNumber
        self.onRun = False
        self.predAgent = None
        
    def runAway(self, ag):
        self.x, self.y = self.moveAway(ag.x, ag.y)
        
    def move(self):
        if self.onRun:
            self.runAway(self.predAgent)
        else:
            self.moveRandom()