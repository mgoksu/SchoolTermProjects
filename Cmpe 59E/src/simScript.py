'''
Created on Jan 1, 2017

@author: miracgoksuozturk
'''

import dynamics
import settings
import sys

settings.sttng.visual = False

n_list = [100, 200, 500]
v_pry_prd_list = [(1,2), (2,3), (3,4), (4,5)]
s_pry_prd_list = [(5,8), (10,13), (15,18), (20, 23), (30, 33), (50, 53)]
hp_size_list = [0.0,0.1,0.15,0.20,0.25]
canWarn_list = [False, True]
canTrap_list = [False, True]
trap_perc_list = [0.2, 0.4, 0.6, 0.8]


def getStat():
    pry_count = 0.0
    prd_count = 0.0
    for _, ag in settings.agents.iteritems():
        if ag.gNumber == settings.sttng.pred_color:
            prd_count += 1
        elif ag.gNumber == settings.sttng.prey_color:
            pry_count += 1

    return '%f %f\n'%(pry_count/settings.sttng.K, prd_count/settings.sttng.K)



f = open('results.txt', 'w')

i=0
for n in n_list:
    settings.sttng.n = n
    for v_pry, v_prd in v_pry_prd_list:
        settings.sttng.v_prey = v_pry
        settings.sttng.v_pred = v_prd
        for s_pry, s_prd in s_pry_prd_list:
            settings.sttng.s_prey = s_pry
            settings.sttng.s_pred = s_prd
            for hp_size in hp_size_list:
                settings.sttng.hp_size = int(hp_size*n)
                for canWarn in canTrap_list:
                    settings.sttng.canWarn = canWarn
                    for canTrap in canTrap_list:
                        settings.sttng.canTrap = canTrap
                        for trap_perc in trap_perc_list:
                            settings.sttng.trap_perc = trap_perc
                             
                            i += 1
                            
                            dynamics.init()
                            dynamics.simulate()
                            par = '%s %s %s %s %s %s %s'%(n, str(v_pry)+','+str(v_prd), str(s_pry)+','+str(s_prd), hp_size, canWarn, canTrap, trap_perc)
                            f.write(par+' '+getStat())
                            print i
                            #print par,getStat()    
                            
f.close()