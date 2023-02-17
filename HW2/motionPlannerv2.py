#python
import random


# Constants
min_x = -3 # meters
max_x = 3 # meters
min_y = -2.5 # meters
max_y = 2.5 # meters


def sysCall_thread():
    

    obj_handle = sim.getObject("/target")
    sim.setObjectPosition(obj_handle,-1,[0,0,1])
   
    while True:
        p = sim.getObjectPosition(obj_handle,-1)
        
        current_x=p[0]
        current_y =p[1]
        
        next_x = random.uniform(min_x, max_x)
        next_y = random.uniform(min_y, max_y)
    
        distance_x = next_x - current_x
        distance_y = next_y - current_y
        
        speed = random.uniform(0.01, 0.03)
            
        p[0]=p[0] + speed*distance_x
        p[1]=p[1] + speed*distance_y
        
        sim.setObjectPosition(obj_handle, -1, p)
            
        
        sim.wait(0.01) 
    
    
    pass

