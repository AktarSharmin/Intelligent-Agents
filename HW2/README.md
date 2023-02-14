
In this repo, the whole scene file has been uploaded. 
Below is the description of child script ( python ) named 'motionPlanner' which is responsible for copter controlling:

- given a 6m x 5m target area, I have set x axis boundary as [-3,3] and y-axis as [-2.5,2.5] 
- to create a motion planning algorithm so that a quadrotor UAV can patrol the target area without revealing its strategy to intruders, I have used random fraction generator using "random.uniform" function to generate next position. 
First, I have setup the copters position at [0,0,0]. Then, for both x,y axis random fraction has been generated and using that random number, next position is generated. To control the speed of the copter I have also used a paramter called 'speed' and also choose it's value randomly so that intruder can't detect it's speed as well. 
Now when the new position reaches it's corresponding boundary value, in that case again a randomness has been used to avoid exceeding the target area. 


