#python
import numpy as np


def sysCall_init():
    
    sphereHandle = sim.getObject('/Sphere')
   
    # Generate random points on the surface of the sphere
    n = 300
    vector = np.random.randn(3, n)
    vector /= np.linalg.norm(vector, axis=0)
    
    points = 0.5 * vector.T #transposing since it returns (3,n)
    
    for i in range(n):
        
        x, y, z = points[i]

        u1 = np.random.uniform(0, 1)
        u2 = np.random.uniform(0, 1)
        u3 = np.random.uniform(0, 1)
  
        
        a = np.sqrt(1 - u1) * np.sin(2 * np.pi * u2)
        b = np.sqrt(1 - u1) * np.cos(2 * np.pi * u2)
        c = np.sqrt(u1) * np.sin(2 * np.pi * u3)
        d = np.sqrt(u1) * np.cos(2 * np.pi * u3)
        
        coneHandle = sim.createPrimitiveShape(sim.primitiveshape_cone, [0.06, 0.06, 0.06])
        
        
        sim.setObjectPosition(coneHandle, sphereHandle, [ x, y, z])
        sim.setObjectQuaternion(coneHandle, sphereHandle,[a,b,c,d])
    
        
    pass
