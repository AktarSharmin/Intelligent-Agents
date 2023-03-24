#python
import numpy as np
def sysCall_thread():
    sim.setThreadAutomaticSwitch(True)

    quad_handle = sim.getObject('/target')
    
    while True:
        trajectory_handle = sim.getInt32Signal("trajectory")
        dt = sim.getSimulationTimeStep()
        if(trajectory_handle):
            
                sim.clearInt32Signal("trajectory")
                
                trajectory_path = sim.unpackDoubleTable(sim.readCustomDataBlock(trajectory_handle, "PATH"))
                
    
                trajectory_path = np.array(trajectory_path).reshape(len(trajectory_path)//7,7)
                #print(len(trajectory_path))
                
                for i in range(len(trajectory_path)):
                    pose = trajectory_path[i]
                    sim.setObjectPosition(quad_handle, -1, pose[:3].tolist())
                    sim.setObjectQuaternion(quad_handle, -1, pose[3:].tolist())
                    sim.wait(dt)
    pass


