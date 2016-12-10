'''
Created on Nov 21, 2016

@author: miracgoksuozturk
'''
import math
import random
import numpy
import dynamics
from abc import ABCMeta
from _pyio import __metaclass__

rnd = random.Random()

n = dynamics.n

class Agent:
    __metaclass__ = ABCMeta
    
    def __init__(self, x, y, speed, ID, alpha, R):
        self.alpha = alpha
        self.R = R
        self.ID = ID
        self.speed = speed
        self.x = x
        self.y = y
    
    def moveTowards(self, x2, y2):
        x1 = self.x
        y1 = self.y
        speed = self.speed
        if x1 == x2 and y1 == y2:
            return x1, y1
        dirX = self.shortestPath(x1, x2)
        dirY = self.shortestPath(y1, y2)
        
        hyp = math.sqrt(dirX**2 + dirY**2) 
        dirX /= hyp
        dirY /= hyp
            
        x = x1 + dirX*speed
        y = y1 + dirY*speed
        x = int(round(x))
        y = int(round(y))
        
        if x >= n:
            x = x % n
        elif x < 0:
            x = n+x
        
        if y >= n:
            y = y % n
        elif y < 0:
            y = n+y
        
        return (x, y)
    
    def moveRandom(self):
        global rnd
        rand = rnd.random()
        if rand < 0.25:
            self.x += 1
        elif rand < 0.5:
            self.x -= 1
        elif rand < 0.75:
            self.y += 1
        elif rand < 1.:
            self.y -= 1
            
        if self.x >= n:
            self.x = self.x % n
        elif self.x < 0:
            self.x = self.x + n
        
        if self.y >= n:
            self.y = self.y % n
        elif self.y < 0:
            self.y = self.y + n
        
    def moveAway(self, x2, y2):
        global n
        x1 = self.x
        y1 = self.y
        speed = self.speed
        if x1 == x2 and y1 == y2:
            rnd = random.Random()
            if rnd.random() < 0.5:
                x1 = x1 - speed
            else:
                y1 = y1 - speed
            return x1, y1
        dirX = self.shortestPath(x1, x2)
        dirY = self.shortestPath(y1, y2)
        
        hyp = math.sqrt(dirX**2 + dirY**2) 
        dirX /= hyp
        dirY /= hyp
            
        x = x1 - dirX*speed
        y = y1 - dirY*speed
        x = int(round(x))
        y = int(round(y))
        
        if x >= n:
            x = x % n
        elif x < 0:
            x = x + n
        
        if y >= n:
            y = y % n
        elif y < 0:
            y = y + n
        
        return (x, y)
    
    def shortestPath(self, c1, c2):
        dc1 = (c2 - c1)
        if c2 > c1:
            dc2 = (c2 - c1 - n)
        else:
            dc2 = (c2 - c1 + n)
        if abs(dc1) <= abs(dc2):
            return dc1
        else:
            return dc2
    
    def distance(self, x1, y1, x2, y2):
        dx = self.shortestPath(x1, x2)**2
        dy = self.shortestPath(y1, y2)**2
        return math.sqrt(dx + dy)# (y2 - y1)**2 - (x2 - x1)**2
    
    def isInCircle(self, x2, y2, r):
        x1 = self.x
        y1 = self.y
        return self.distance(x1, y1, x2, y2) < r
    
    def hasVision(self, ag):
        if not self.isInCircle(ag.x, ag.y, self.R):
            return False
        global rnd
        rand = rnd.random()
        if rand < self.alpha/(2*numpy.pi):
            return True
        else:
            return False
    
    def hasAgentNearBy(self, agents, gNumber):
        for ID, ag in agents.iteritems():
            if(ag.gNumber == gNumber and self.hasVision(ag)):
                return ag
        return None
        
    def printCoord(self):
        print 'x: %f, y: %f' %(self.x, self.y)
        
class Prey(Agent):
    
    def __init__(self, x, y, speed, ID, alpha, R, gNumber, stamina):
        Agent.__init__(self, x, y, speed, ID, alpha, R)
        self.gNumber = gNumber
        self.predAgent = None
        self.fullStamina = stamina
        self.currentStamina = stamina
        
    def runAway(self, ag):
        self.x, self.y = self.moveAway(ag.x, ag.y)
        self.currentStamina -= 1
        
    def move(self, agents, freeID):
        if self.predAgent != None:
            if not self.isInCircle(self.predAgent.x, self.predAgent.y, self.R):
                self.predAgent = None
            else:
                if self.currentStamina != 0:
                    self.runAway(self.predAgent)
                else:
                    self.moveRandom()
                    if self.currentStamina != self.fullStamina:
                        self.currentStamina += 1
        else:
            prd = self.hasAgentNearBy(agents, dynamics.red)
            if prd != None:
                self.predAgent = prd
                if self.currentStamina != 0:
                    self.runAway(self.predAgent)
                else:
                    self.moveRandom()
                    if self.currentStamina != self.fullStamina:
                        self.currentStamina += 1
            else:    
                self.moveRandom()
                if self.currentStamina != self.fullStamina:
                    self.currentStamina += 1
            
class Pred(Agent):
    
    def __init__(self, x, y, speed, ID, alpha, R, gNumber, stamina):
        Agent.__init__(self, x, y, speed, ID, alpha, R)
        self.gNumber = gNumber
        self.wantedAgent = None
        self.fullStamina = stamina
        self.currentStamina = stamina
        self.onRest = False
        
    def chase(self, agents, ag, freeID):
        if(self.distance(self.x, self.y, ag.x, ag.y) < self.speed):
            self.x, self.y = ag.x, ag.y
        else:
            self.x, self.y = self.moveTowards(ag.x, ag.y)
        if self.x == ag.x and self.y == ag.y:
            self.killAgent(agents, ag, freeID)
        self.currentStamina -= 1
       
    def killAgent(self, agents, ag, freeID):
        freeID.append(ag.ID)
     
    def move(self, agents, freeID):
        if self.onRest:
            self.moveRandom()
            if self.currentStamina != self.fullStamina:
                    self.currentStamina += 1
            if self.currentStamina == self.fullStamina:
                self.onRest = False
        elif self.wantedAgent != None:
            if not self.isInCircle(self.wantedAgent.x, self.wantedAgent.y, self.R):
                self.wantedAgent = None
            else:
                self.chase(agents, self.wantedAgent, freeID)
                if self.currentStamina == 0:
                    self.onRest = True
        else:
            pry = self.hasAgentNearBy(agents, dynamics.blue)
            if pry != None:
                self.wantedAgent = pry
                self.chase(agents, pry, freeID)
                if self.currentStamina == 0:
                    self.onRest = True
            else:    
                self.moveRandom()
                if self.currentStamina != self.fullStamina:
                    self.currentStamina += 1