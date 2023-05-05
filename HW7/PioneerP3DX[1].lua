function sysCall_init() 
    local robot=sim.getObject('.')
    local obstacles=sim.createCollection(0)
    sim.addItemToCollection(obstacles,sim.handle_all,-1,0)
    sim.addItemToCollection(obstacles,sim.handle_tree,robot,1)
    usensors={}
    for i=1,16,1 do
        usensors[i]=sim.getObject("./ultrasonicSensor",{index=i-1})
        sim.setObjectInt32Param(usensors[i],sim.proxintparam_entity_to_detect,obstacles)
    end
    
    motorLeft=sim.getObject("./leftMotor")
    motorRight=sim.getObject("./rightMotor")
    noDetectionDist=0.5
    maxDetectionDist=0.2
    detect={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
    braitenbergL={-0.2,-0.4,-0.6,-0.8,-1,-1.2,-1.4,-1.6, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0}
    braitenbergR={-1.6,-1.4,-1.2,-1,-0.8,-0.6,-0.4,-0.2, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0}
    v0=2
end
-- This is a very simple EXAMPLE navigation program, which avoids obstacles using the Braitenberg algorithm


function sysCall_cleanup() 
 
end 

function uni_to_diff(v, w)
	vR = (2 * v + w * L) / ( 2 * R)
	vL = (2 * v - w * L) / ( 2 * R)
	return vR, vL
end 
function sysCall_actuation() 
    L = 0.381
    R = 0.195 / 2
    
    Kp = .25
	Kalpha = .35
    
    for i=1,16,1 do
        res,dist=sim.readProximitySensor(usensors[i])
        if (res>0) and (dist<noDetectionDist) then
            if (dist<maxDetectionDist) then
                dist=maxDetectionDist
            end
            detect[i]=1-((dist-maxDetectionDist)/(noDetectionDist-maxDetectionDist))
        else
            detect[i]=0
        end
    end
    
    
    destination_sphere = sim.getObject('/destination_sphere')
    destination_pioneer = sim.getObject('/PioneerP3DX[1]')
    
    pos = sim.getObjectPosition(destination_sphere,destination_pioneer)
    err = math.sqrt(pos[1]^2 + pos[2]^2 + pos[3]^2)
    --pos = np.array(pos)
    --err = np.linalg.norm(pos)
    
    x = pos[1]
    y = pos[2]
    

    vR, vL = 0, 0

    vR, vL = uni_to_diff( x, y)
	--vR = (2 * x + y * L) / ( 2 * R)
	--vL = (2 * x - y * L) / ( 2 * R)
    

	--vR = (2 * x + y * L) / ( 2 * R)
	--vL = (2 * x - y * L) / ( 2 * R)
    
        
    vLeft=vL
    vRight=vR
    
    for i=1,16,1 do
        vLeft=vLeft+braitenbergL[i]*detect[i]
        vRight=vRight+braitenbergR[i]*detect[i]
    end
    
    sim.setJointTargetVelocity(motorLeft,vLeft)
    sim.setJointTargetVelocity(motorRight,vRight)
end 
