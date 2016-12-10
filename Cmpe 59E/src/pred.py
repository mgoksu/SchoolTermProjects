'''
Created on Nov 21, 2016

@author: miracgoksuozturk
'''
from agent import Agent


class Pred(Agent):
    
    def __init__(self, x, y, speed, ID, alpha, R, gNumber):
        Agent.__init__(self, x, y, speed, ID, alpha, R)
        self.gNumber = gNumber
        self.onChase = False
        self.wantedAgent = None
        
    def chase(self, ag):
        self.x, self.y = self.moveTowards(ag.x, ag.y)
        
    def move(self):
        if self.onChase:
            self.chase(self.wantedAgent)
        else:
            self.moveRandom()