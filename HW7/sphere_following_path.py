#python
import numpy as np

    
    
def sysCall_thread():
    sim.setThreadAutomaticSwitch(True)

    source_sphere = sim.getObject('/source_sphere')
    destination_sphere = sim.getObject('/destination_sphere')
    
    source_pioneer = sim.getObject('/PioneerP3DX[0]')
    destination_pioneer = sim.getObject('/PioneerP3DX[1]')
    
   
    
    
    while True:
        trajectory_handle = sim.getInt32Signal("trajectory")
        
        if(trajectory_handle):
                
                sim.clearInt32Signal("trajectory")
                
                trajectory_path = sim.unpackDoubleTable(sim.readCustomDataBlock(trajectory_handle, "PATH"))
                trajectory_path = np.array(trajectory_path).reshape(len(trajectory_path)//7,7)
                
                i = 0
                while i < len(trajectory_path):
                    front_path = trajectory_path[i]
                    rev_path = trajectory_path[-i-1]
                    #print(rev_path)
                    source_result, source_distance, _ = sim.checkDistance(source_sphere, source_pioneer)
                    destination_result, destination_distance, _ = sim.checkDistance(destination_sphere, destination_pioneer)
                    #print("src")
                    #print(source_distance[6])
                    #if source_distance[6] > 0.2 or destination_distance[6] > 0.2:
                        #print("far")

                    if source_distance[6] <= 0.2 or destination_distance[6] <= 0.2:
                        sim.setObjectPosition(source_sphere, -1, front_path[:3].tolist())
                        sim.setObjectQuaternion(source_sphere, -1, front_path[3:].tolist())

                        sim.setObjectPosition(destination_sphere, -1, rev_path[:3].tolist())
                        sim.setObjectQuaternion(destination_sphere, -1, rev_path[3:].tolist())

                        i += 1
                    sim.wait(0.1)
    pass


