#python
import math
from sys import maxsize
import numpy as np
import itertools 
class State:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.state = "."
        self.t = "new"  # tag for state
        self.h = 0
        self.k = 0

    def cost(self, state):
        if self.state == "#" or state.state == "#":
            return maxsize

        return math.sqrt(math.pow((self.x - state.x), 2) +
                         math.pow((self.y - state.y), 2))

    def set_state(self, state):
        """
        .: new
        #: obstacle
        e: oparent of current state
        *: closed state
        s: current state
        """
        if state not in ["s", ".", "#", "e", "*"]:
            return
        self.state = state


class Map:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.map = self.init_map()

    def init_map(self):
        map_list = []
        for i in range(self.row):
            tmp = []
            for j in range(self.col):
                tmp.append(State(i, j))
            map_list.append(tmp)
        return map_list

    def get_neighbors(self, state):
        state_list = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                if state.x + i < 0 or state.x + i >= self.row:
                    continue
                if state.y + j < 0 or state.y + j >= self.col:
                    continue
                state_list.append(self.map[state.x + i][state.y + j])
        return state_list

    def set_obstacle(self, point_list):
        for x, y in point_list:
            if x < 0 or x >= self.row or y < 0 or y >= self.col:
                continue

            self.map[x][y].set_state("#")


class Dstar:
    def __init__(self, maps):
        self.map = maps
        self.open_list = set()

    def process_state(self):
        x = self.min_state()

        if x is None:
            return -1

        k_old = self.get_kmin()
        self.remove(x)

        if k_old < x.h:
            for y in self.map.get_neighbors(x):
                if y.h <= k_old and x.h > y.h + x.cost(y):
                    x.parent = y
                    x.h = y.h + x.cost(y)
        elif k_old == x.h:
            for y in self.map.get_neighbors(x):
                if y.t == "new" or y.parent == x and y.h != x.h + x.cost(y) \
                        or y.parent != x and y.h > x.h + x.cost(y):
                    y.parent = x
                    self.insert(y, x.h + x.cost(y))
        else:
            for y in self.map.get_neighbors(x):
                if y.t == "new" or y.parent == x and y.h != x.h + x.cost(y):
                    y.parent = x
                    self.insert(y, x.h + x.cost(y))
                else:
                    if y.parent != x and y.h > x.h + x.cost(y):
                        self.insert(y, x.h)
                    else:
                        if y.parent != x and x.h > y.h + x.cost(y) \
                                and y.t == "close" and y.h > k_old:
                            self.insert(y, y.h)
        return self.get_kmin()

    def min_state(self):
        if not self.open_list:
            return None
        min_state = min(self.open_list, key=lambda x: x.k)
        return min_state

    def get_kmin(self):
        if not self.open_list:
            return -1
        k_min = min([x.k for x in self.open_list])
        return k_min

    def insert(self, state, h_new):
        if state.t == "new":
            state.k = h_new
        elif state.t == "open":
            state.k = min(state.k, h_new)
        elif state.t == "close":
            state.k = min(state.h, h_new)
        state.h = h_new
        state.t = "open"
        self.open_list.add(state)

    def remove(self, state):
        if state.t == "open":
            state.t = "close"
        self.open_list.remove(state)

    def modify_cost(self, x):
        if x.t == "close":
            self.insert(x, x.parent.h + x.cost(x.parent))

    def run(self, start, end):

        rx = []
        ry = []

        self.insert(end, 0.0)

        while True:
            self.process_state()
            if start.t == "close":
                break

        start.set_state("s")
        s = start
        s = s.parent
        s.set_state("e")
        tmp = start

        while tmp != end:
            tmp.set_state("*")
            rx.append(tmp.x)
            ry.append(tmp.y)
            if tmp.parent.state == "#":
                self.modify(tmp)
                continue
            tmp = tmp.parent
        tmp.set_state("e")

        return rx, ry

    def modify(self, state):
        self.modify_cost(state)
        while True:
            k_min = self.process_state()
            if k_min >= state.h:
                break


 

    
def create_source():
    size = [0.1, 0.1, 0.1]  # Set the size of the source object
    source_handle = sim.createPrimitiveShape(sim.primitiveshape_cuboid, size)
    sim.setObjectAlias(source_handle, "source")
    sim.setObjectPosition(source_handle,-1,[-1.5,-0.8,0])
    sim.setObjectColor(source_handle,0,0, [0, 0, 1])
    source=sim.getObjectPosition(source_handle,-1)
    return source


def create_destination():
    size = [0.1, 0.1, 0.1]  # Set the size of the destination object
    destination_handle = sim.createPrimitiveShape(sim.primitiveshape_cuboid, size)
    sim.setObjectAlias(destination_handle, "destination")
    sim.setObjectPosition(destination_handle,-1,[1.5,1,0])
    sim.setObjectColor(destination_handle,0,0, [0, 1, 0])
    destination=sim.getObjectPosition(destination_handle,-1)
    return destination
    
def create_source_sphere():
    size = [0.1, 0.1, 0.1]
    sphere_handle = sim.createPrimitiveShape(sim.primitiveshape_spheroid, size)
    sim.setObjectAlias(sphere_handle, "source_sphere")
    source_pioneer = sim.getObject('/PioneerP3DX[0]')
    source_pioneer_pos = sim.getObjectPosition(source_pioneer,-1)
    #print(source_pioneer_pos)
    dis = 0
    sim.setObjectPosition(sphere_handle,-1,[ source_pioneer_pos[0]+dis,source_pioneer_pos[1]+dis,source_pioneer_pos[2]+dis ])
    #sim.setObjectPosition(sphere_handle,-1,[-1.3,-0.8,0])
    #sim.setObjectColor(sphere_handle,0,0, [0.11, 0.1, 0])
    sphere_pos=sim.getObjectPosition(sphere_handle,-1)
    return sphere_handle,sphere_pos

def create_destination_sphere():
    size = [0.1, 0.1, 0.1]
    sphere_handle = sim.createPrimitiveShape(sim.primitiveshape_spheroid, size)
    sim.setObjectAlias(sphere_handle, "destination_sphere")
    dis = 0
    destination_pioneer = sim.getObject('/PioneerP3DX[1]')
    destination_pioneer_pos = sim.getObjectPosition(destination_pioneer,-1)
    sim.setObjectPosition(sphere_handle,-1,[ destination_pioneer_pos[0]+dis,destination_pioneer_pos[1]+dis,destination_pioneer_pos[2]+dis ])

    #sim.setObjectPosition(sphere_handle,-1,[1.5,0.8,0])
    sphere_pos=sim.getObjectPosition(sphere_handle,-1)
    return sphere_handle,sphere_pos
    
def create_obstacles_boundary(obstacles):
    size = [0.1, 0.1, 0.2] 
    obstacle_handles = []
    for obstacle in obstacles:
        obstacle_handle = sim.createPrimitiveShape(sim.primitiveshape_cuboid, size)
        sim.setObjectPosition(obstacle_handle, -1, [obstacle[0], obstacle[1], 0.2])
        #sim.setObjectColor(obstacle_handle,0,0, [1, 1, 0])
        obstacle_handles.append(obstacle_handle)
    obstacles_group = sim.groupShapes(obstacle_handles)
    sim.setObjectAlias(obstacles_group, 'obstacles')
    
def euler_to_quaternion():
    from scipy.spatial.transform import Rotation as R
    import numpy as np

    # Create a Rotation instance from the Euler angle
    r = R.from_euler('xyz', [0.1, 0.1, 0.1])

    # Convert the Rotation instance to a quaternion
    q = r.as_quat()

    return q


def create_trajectory(path):
    

    control_points = []
    
    for p in path:
      position = [p[0], p[1], 0]
      quaternion = euler_to_quaternion()
      control_points.extend(position+quaternion.tolist())
    

    #print(control_points)

    path_lengths,total_length=sim.getPathLengths(control_points,7)
    dt = sim.getSimulationTimeStep()*0.5
    
    trajectory_handle = sim.createPath(control_points, 16,total_length  // dt, 1)
    sim.setInt32Signal("trajectory", trajectory_handle)


    
    return trajectory_handle


'''
def follow_path():
    path_handle = sim.getObjectHandle("/path")
    quad_handle = sim.getObject("/target")
    sim.followPath(quad_handle, path_handle, 1, 0, 0.17,15)'''
    

def rescale_range(data, input_min, input_max, output_min, output_max):
    data = np.array(data)
    standardized = (data - input_min) / (input_max - input_min)
    scaled = standardized * (output_max - output_min) + output_min
    return scaled
    

    
def sysCall_init():
    
    
    
    #set the obstacle boundary with safety measure
    
    m = Map(100, 100)
    ox, oy = [], []
    for i in range(-10, 60):
        ox.append(i)
        oy.append(-10)
    for i in range(-10, 60):
        ox.append(60)
        oy.append(i)
    for i in range(-10, 61):
        ox.append(i)
        oy.append(60)
    for i in range(-10, 61):
        ox.append(-10)
        oy.append(i)
    for i in range(-10, 40):
        ox.append(20)
        oy.append(i)
    for i in range(0, 40):
        ox.append(40)
        oy.append(60 - i)
    m.set_obstacle([(i, j) for i, j in zip(ox, oy)])

    #add safety boundary
    #safety param
    safety_param = 5
    
    m.set_obstacle([(i+safety_param, j) for i, j in zip(ox, oy)])
    m.set_obstacle([(i-safety_param, j) for i, j in zip(ox, oy)])
    m.set_obstacle([(i, j+safety_param) for i, j in zip(ox, oy)])
    m.set_obstacle([(i, j-safety_param) for i, j in zip(ox, oy)])
    
    
    coppeliasim_min=-2.5
    coppeliasim_max=2.5
    obstacle_min=-10
    obstacle_max=60
    
    #scale obstacles to coppeliasim config
    scaled_ox= rescale_range(ox, obstacle_min, obstacle_max, coppeliasim_min, coppeliasim_max)
    scaled_oy= rescale_range(oy, obstacle_min, obstacle_max, coppeliasim_min, coppeliasim_max)
    
    
    #create the obstacles boundary 
    create_obstacles_boundary(np.transpose([scaled_ox, scaled_oy]))
    
    
    #create the source and destination object
    source = create_source()
    destination = create_destination()
    
    source_sphere_handle,source_sphere_pos = create_source_sphere()
    destination_sphere_handle,destination_sphere_pos = create_destination_sphere()
    # scale source and destination to the obstacle range [-10,60]
    
    source = rescale_range(source, coppeliasim_min, coppeliasim_max, obstacle_min, obstacle_max ).astype(int)
    destination = rescale_range(destination, coppeliasim_min, coppeliasim_max, obstacle_min, obstacle_max ).astype(int)
    
    
    
    #run D* algo
    source = m.map[source[0]][source[1]]
    destination = m.map[destination[0]][destination[1]]
    dstar = Dstar(m)
    rx, ry = dstar.run(source, destination)
    
    
    #scale path coord to coppeliasim config
    scaled_rx= rescale_range(rx, obstacle_min, obstacle_max, coppeliasim_min, coppeliasim_max)
    scaled_ry= rescale_range(ry, obstacle_min, obstacle_max, coppeliasim_min, coppeliasim_max)
    
    path = np.stack([scaled_rx, scaled_ry],axis=1)

    #create the trajectory
    trajectory_handle = create_trajectory(np.stack([scaled_rx, scaled_ry],axis=1))
    
    
    
    
   
    
    
    
    
    
    
