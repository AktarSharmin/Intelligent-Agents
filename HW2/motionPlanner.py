#python
import random


# target area boundary
min_x = -3 # meters
max_x = 3 # meters
min_y = -2.5 # meters
max_y = 2.5 # meters




def sysCall_thread():
    
    
    obj_handle = sim.getObject("/target")
    sim.setObjectPosition(obj_handle,-1,[0,0,0.5])#starts from [0,0]
    speed = random.uniform(0.01, 0.03) # speed controller
    while True:
        
        p=sim.getObjectPosition(obj_handle,-1)
        
        next_x = random.uniform(min_x, max_x)
        next_y = random.uniform(min_y, max_y)
    
        
        p[1] = p[1] + speed*next_y
        p[0] = p[0] + speed*next_x
        #print(p[0])
        #print(p[1])
        if p[0] > max_x:
            p[0] = max_x - random.uniform(min_x,max_x)#if next x co-ord exceeds max_x decrease to some random point 
        elif p[0] < min_x:
            p[0] = min_x +  random.uniform(min_x,max_x)#if next x co-ord falls below min_x increase to some random point 

        if p[1] > max_y:
            p[1] = max_y - random.uniform(min_y, max_y)#if next y co-ord exceeds max_y decrease to some random point 
        elif p[1] < min_y:
            p[1] = min_y +  random.uniform(min_y, max_y)#if next y co-ord falls below exceeds min_y decrease to some random point 

        
        sim.setObjectPosition(obj_handle,-1,p)
        
        sim.wait(0.01) 
    
    
    pass


