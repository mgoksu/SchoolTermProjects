'''
Created on Nov 21, 2016

@author: miracgoksuozturk
'''
import numpy
import random
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import agent
import settings


sttng = settings.sttng
#sttng = settings.setParam()
#global sttng

def createBoard():
    sttng.board = numpy.zeros((sttng.n,sttng.n)) + sttng.ground_color
    for _ in range(sttng.hp_count):
        x = int(sttng.rnd.random()*sttng.n)
        y = int(sttng.rnd.random()*sttng.n)
        for j in range(sttng.hp_size):
            for k in range(sttng.hp_size):
                x_ = (x+j)%sttng.n
                y_ = (y+k)%sttng.n
                settings.hp_list.append( (x_, y_) )
                dyeGrid(x_, y_)
    
def dyeGrid(x, y):
    if (x,y) in settings.trap_list:
        sttng.board[x,y] = sttng.trap_color
    elif (x,y) in settings.hp_list:
        sttng.board[x,y] = sttng.hp_color
    else:
        sttng.board[x,y] = sttng.ground_color
    
def createAgent(agentID, agent):
    settings.agents[agentID] = agent
        
    
def init():
    settings.hp_list = []
    settings.trap_list = []
    settings.agents = {}
    agent.init()
    createBoard()
    for i in range(0,sttng.K):
        agentID = i
        x = int(sttng.rnd.random()*sttng.n)
        y = int(sttng.rnd.random()*sttng.n) 
        if i<sttng.K/2:#rnd.random() < 0.5
            born(x, y, agentID, sttng.prey_color) # prey init
        else:
            born(x, y, agentID, sttng.pred_color) # pred init
    

def frame_gen():
    while True:
        yield sttng.board
        
def simulateTurn():
    for ID, ag in settings.agents.iteritems():
        dyeGrid(ag.x, ag.y)
        ag.move(settings.agents, sttng.freeID)
    for ID in numpy.unique(sttng.freeID):
        killAgent(ID)
    for ID, ag in settings.agents.iteritems():
        sttng.board[ag.x, ag.y] = ag.gNumber
    
    for ID in numpy.unique(sttng.freeID):
        breed_key = random.choice(settings.agents.keys())
        new_type = settings.agents[breed_key].gNumber
        new_x = settings.agents[breed_key].x
        new_y = settings.agents[breed_key].y
        born(new_x, new_y, ID, new_type)
    sttng.freeID = []   
    
    sttng.death_count += 1
    if(sttng.death_count == sttng.death_cycle):
        deathBornCycle()

def killAgent(ID):
    #global board, agents
    dyeGrid(settings.agents[ID].x, settings.agents[ID].y)
    del settings.agents[ID]
    for _, agn in settings.agents.iteritems():
        if(agn.gNumber == sttng.pred_color):
            if(agn.wantedAgent != None and agn.wantedAgent.ID == ID):
                agn.wantedAgent = None
        elif(agn.gNumber == sttng.prey_color):
            if(agn.predAgent != None and agn.predAgent.ID == ID):
                agn.predAgent = None
    
def born(x, y, born_key, new_type):
    #global board
    #x = int(rnd.random()*n)
    #y = int(rnd.random()*n)
    if(new_type == sttng.prey_color):
        ag = agent.Prey(x,y, sttng.v_prey, born_key, sttng.alpha, sttng.R, sttng.prey_color, sttng.s_prey) # prey init
    elif(new_type == sttng.pred_color):
        ag = agent.Pred(x,y, sttng.v_pred, born_key, sttng.alpha, sttng.R, sttng.pred_color, sttng.s_pred)  # pred init
    createAgent(born_key, ag)
    sttng.board[x,y] = ag.gNumber
    
def deathBornCycle():
    death_key = random.choice(settings.agents.keys())
    breed_key = random.choice(settings.agents.keys())
    
    new_type = settings.agents[breed_key].gNumber
    new_x = settings.agents[breed_key].x
    new_y = settings.agents[breed_key].y
    killAgent(death_key)
    #del agents[death_key]
    
    born(new_x, new_y, death_key, new_type)
    sttng.death_count = 0

def simulate():
    def update(data):
        simulateTurn()
        mat.set_data(data)
        return mat
    
    if(sttng.visual):
        fig, ax = plt.subplots(figsize=(15,8))
        mat = ax.matshow(sttng.board, cmap='gist_stern', aspect='auto')
        plt.colorbar(mat)
        ani = animation.FuncAnimation(fig=fig, func=update, frames=frame_gen, interval=1000,
                                      save_count=sttng.iteration_count)
        #plt.show()
        if(sttng.save_mp4):
            FFwriter = animation.FFMpegWriter()
            ani.save('ani.mp4', writer = FFwriter, fps=60, extra_args=['-vcodec', 'libx264'])
    else:
        for _ in range(sttng.iteration_count):
            frame_gen()
            simulateTurn()
    '''for _ in range(sttng.iteration_count):
        frame_gen()
        simulateTurn()'''    
        
if __name__ == "__main__":
    init()
    simulate()
    
    
    