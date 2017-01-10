'''
Created on Dec 20, 2016

@author: miracgoksuozturk
'''
import numpy
import random


global hp_list, trap_list, agents, sttng
hp_list = []
trap_list = []
agents = {}


    
def removeCoord(coord):
    global trap_list
    trap_list = [c for c in trap_list if c != coord]

class setParam:
    
    def __init__(self):
        #initGlobals()
        
        self.visual = True
        self.iteration_count = 200
        
        self.save_mp4 = True
        
        self.ground_color = 0.5
        
        # hiding point
        self.hp_color = 0.9
        self.hp_count = 1
        self.hp_size = 4
        
        self.pred_color = 0.0
        self.prey_color = 1.0
        self.freeID = []
        
        self.canTrap = False
        self.trap_perc = 0.9
        self.trap_color = 0.1
        
        
        # general parameters
        self.n = 500
        self.R = 20
        #R_h = 8
        self.alpha = numpy.pi/3
        self.K = 50
        
        self.death_count = 0
        self.death_cycle = 100
        
        # predator parameters
        # id
        #i_pred = 1
        # speed
        self.v_pred = 2
        # stamina
        self.s_pred = 1000
        # fitness
        self.f_pred = 1
        # hunger endurance
        #self.e_pred = 8
        
        
        # prey parameters
        # id
        #i_prey = 2
        # speed
        self.v_prey = 2
        # stamina
        self.s_prey = 1000
        # fitness
        self.f_prey = 1
        
        # warning distance
        self.w_prey = 20
        self.canWarn = True
        self.board = None
        self.rnd = random.Random()

        
sttng = setParam()
