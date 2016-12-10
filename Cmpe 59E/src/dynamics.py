'''
Created on Nov 21, 2016

@author: miracgoksuozturk
'''
import numpy
import random
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import agent

white = 0.5
red = 1.0
blue = 0.0
agents = {}
freeID = []

# general parameters
n = 50
R = 45
#R_h = 8
alpha = numpy.pi/3
K = 2

# predator parameters
# id
i_pred = 1
# speed
v_pred = 2
# stamina
s_pred = 5000
# fitness
f_pred = 1
# hunger endurance
e_pred = 8


# prey parameters
# id
i_prey = 2
# speed
v_prey = 2
# stamina
s_prey = 5000
# fitness
f_prey = 1
board = None
rnd = random.Random()


def createBoard():
    board = numpy.zeros((n,n)) + white
    return board
    
def createAgent(agentID, agent):
    agents[agentID] = agent
        
    
def init():
    global board, rnd
    board = createBoard()
    for i in range(0,K):
        agentID = i
        #x = int(rnd.random()*n)
        #y = int(rnd.random()*n)
        x = 5*(i+1)
        y = 5*(i+1)   
        if i<K/2:#rnd.random() < 0.5
            ag = agent.Prey(x,y,v_prey,agentID,alpha,R,blue, s_prey) # prey init
        else:
            ag = agent.Pred(x,y,v_pred,agentID,alpha,R,red, s_pred)  # pred init
        createAgent(agentID, ag)
        board[x,y] = ag.gNumber
    return board

def frame_gen():
    while True:
        yield board
        
def simulateTurn():
    ids = agents.keys()
    global freeID
    for ID, ag in agents.iteritems():
        board[ag.x, ag.y] = white
        ag.move(agents, freeID)
    for ID in numpy.unique(freeID):
        board[agents[ID].x, agents[ID].y] = white
        del agents[ID]
        for agnID, agn in agents.iteritems():
            if(agn.gNumber == red):
                if(agn.wantedAgent != None and agn.wantedAgent.ID == ID):
                    agn.wantedAgent = None
            elif(agn.gNumber == blue):
                if(agn.predAgent != None and agn.predAgent.ID == ID):
                    agn.predAgent = None
    for ID, ag in agents.iteritems():
        board[ag.x, ag.y] = ag.gNumber
    freeID = []
    '''
    for ID, ag in agents.iteritems():
        board[ag.x, ag.y] = white
        ag.move(agents, freeID)
        board[ag.x, ag.y] = ag.gNumber
    '''    
def update(data):
    simulateTurn()
    mat.set_data(data)
    return mat 
        
if __name__ == "__main__":
    init()
    fig, ax = plt.subplots(figsize=(15,8))
    mat = ax.matshow(board, cmap='seismic', aspect='auto')
    plt.colorbar(mat)
    ani = animation.FuncAnimation(fig=fig, func=update, frames=frame_gen, interval=1500,
                                  save_count=50)
    plt.show()
    
    