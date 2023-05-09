import random
#=======================================================================================================
# For the code to run, it must be run in the code in the Pything console
# The commands to type are as follows:
#To run the Simulation type:
#   sim = Simulation(time_steps) (where time steps is the number of time steps you would like to simulate)
#   sim.run() (this will show you the simulation of the roads)
# 
# To get Data type:
#    sim.data (this will give you a 2D array were each array is a lane and 
#              shows you how many time steps it took for a car to make it to the end of the highway)
#
# To get how many cars made it to the end of the highway for each lane type:
#   sim.madeIt()

# To get the average time step for each lane type:
#   sim.averageTimeStep
#========================================================================================================


# Parameter definitions
#========================================================================================================
EMPTY = " " # signifies an empty slot in the road
#========================================================================================================

#========================================================================================================
#Speeds for vehicles
SELF_D = 4 # speed for the self-driven vehicles 100km/h to start may change later
SELF_D1 = 5 # speed for the self-driven vehicles 110km/h
SELF_D2 = 6 # speed for the self-driven vehicles 120km/h
HUMAN_D = 4 # speed for the human-ddriven vehicles 100km/h
#========================================================================================================

#========================================================================================================
# Safe follow distances for inbetween vehicles
SAFE_FOLLOW_S = 3 # the travel distance that Human driven vehicles must keep infront of them
SAFE_FOLLOW_H = 4 # the travel distance that Human driven vehicles must keep infront of them
#========================================================================================================

#========================================================================================================
# Integers representiing the lanes of the Highway
LEFT = 0 # Self-driven lane
MIDDILE = 1 # 1st human driven lane
RIGHT = 2 # 2nd human driven lane
EMERGENCY = 3 # emergency lane
#========================================================================================================

#========================================================================================================
# Probabilty of generating a vehicle for each type
SELF_PROBABILITY = 0.3 # used in the random spawing of self-driven vehicles going at normal speed
SELF_PROBABILITY1 = 0.2 # used in the random spawing of self-driven vehicles going faster speed
SELF_PROBABILITY2= 0.1 # used in the random spawing of self-driven vehicles going fastest speed 

HUMAN_PROBABILITY_M = 0.5 # used in the random spawing of Human-driven vehicles in the middle lane
HUMAN_PROBABILITY_R = 0.5 # used in the random spawing of Human-driven vehicles in the Right Lane
#========================================================================================================

#========================================================================================================
# Other Variables
HIGHWAY_LENGTH = 150 # length of the highway
PRINT_ROAD = True
#=======================================================================================================

# Function definitions
#========================================================================================================
class Driver:
    def __init__(self, type, speed, arrive_time):
        self.speed = speed
        self.type = type
        self.arrive_time = arrive_time
        if(type == "S"): # identification of car: is it a human or self-driven car
            self.safe_follow = SAFE_FOLLOW_S
        else:
            self.safe_follow = SAFE_FOLLOW_H
#========================================================================================================

#========================================================================================================
class Highway:
    def __init__(self, length):
        # initializing the road
        self.road = [[], [], [], []]
        self.length = length
        for i in range(length):
            self.road[0].append(EMPTY)
            self.road[1].append(EMPTY)
            self.road[2].append(EMPTY)
            self.road[3].append(EMPTY)
#========================================================================================================
    def getCar(self, lane, index):
        # returns what kind of car if any at a given lane and index
        return self.road[lane][index]
#========================================================================================================
    def setCar(self, lane, index, value):
        # sets the kind of car we want a given lane and index
        self.road[lane][index] = value
#========================================================================================================
    def safe_distance_within(self, lane, index, k):
        #Returns the distance until the next car, from index i within k; returns k if all spots are EMPTY
        x = 0
        for i in range(index + 1, index + k + 1):
            if i >= self.length:
                return k
            if self.road[lane][i] != EMPTY:
                return x
            x += 1
        return x
#=====================================================================================================================================
    def safe_left_lane_change_from_Right(self, index):
        # Returns true if the self driving vehicle may lane change from the Right into the Middle Lane
        # checks if the index beside it and 2 spaces infront of it are empty
        return self.road[LEFT][index-1] == EMPTY and self.road[MIDDILE][index] == EMPTY and self.road[MIDDILE][index+1] == EMPTY and self.road[MIDDILE][index+2] == EMPTY
#========================================================================================================    
    def safe_left_lane_change_from_Middle(self, index):
        # Returns true if the self driving vehicle may lane change from the middle into the left Lane(self-driving lane)
        # checks if the index beside it and 2 spaces infront of it are empty
        return self.road[LEFT][index-1] == EMPTY and self.road[LEFT][index] == EMPTY and self.road[LEFT][index+1] == EMPTY and self.road[LEFT][index+2] == EMPTY
#=====================================================================================================================================
    def print(self):
        # this prints out the road
        s = "\n"
        for i in range(self.length):
            if self.road[0][i] == EMPTY:
                s += "_"
            else:
                s += "S"
        s+="\n"
        for i in range(self.length):
            if self.road[1][i] == EMPTY:
                s += "_"
            else:
                s += "C"
        s+="\n"
        for i in range(self.length):
            if self.road[2][i] == EMPTY:
                s += "_"
            else:
                s += "C"
        s+="\n"
        for i in range(self.length):
            if self.road[3][i] == EMPTY:
                s += "_"
            else:
                s += "C"
        print(s)
#========================================================================================================       

#========================================================================================================
class Simulation:
    def __init__(self, time_steps):
        self.road = Highway(HIGHWAY_LENGTH)
        self.time_steps = time_steps
        self.current_step = 0
        self.data = [[],[],[],[]]
#========================================================================================================
    def run(self):
        while (self.current_step < self.time_steps):
            self.execute_time_step()
            self.current_step += 1
            if PRINT_ROAD:
                self.road.print()
#========================================================================================================
    def execute_time_step(self):
        for i in range (self.road.length -1,-1,-1):

            if self.road.getCar(LEFT,i) != EMPTY:
                self.sim_self_driven_lane(i)

            if self.road.getCar(MIDDILE,i) != EMPTY:
                self.sim_human_driven_lane1(i)

            if self.road.getCar(RIGHT,i) != EMPTY:
                self.sim_human_driven_lane2(i)
        self.gen_Cars()
#========================================================================================================
    def sim_self_driven_lane(self, i):
        driver = self.road.getCar(LEFT,i)
        
        # Remove the car if we make it to the end of the highway
        if driver.speed + i >= self.road.length - 1:
            self.road.setCar(LEFT, i, EMPTY)
            self.data[0].append(self.current_step - driver.arrive_time)
            return

        self.sim_cruise(LEFT, i)
#========================================================================================================
    def sim_human_driven_lane1(self, i):
        driver = self.road.getCar(MIDDILE,i)
        
        # Remove the car if we make it to the end of the highway
        if driver.speed + i >= self.road.length - 1:
            self.road.setCar(MIDDILE, i, EMPTY)
            self.data[1].append(self.current_step - driver.arrive_time)
            return

        if driver.type == "S":
            if self.road.safe_left_lane_change_from_Middle(i):
                self.road.setCar(LEFT, i, driver)
                self.road.setCar(MIDDILE, i, EMPTY)
                self.sim_cruise(LEFT, i)
            else:
                self.sim_cruise(MIDDILE, i)
        else:
            self.sim_cruise(MIDDILE, i)
#========================================================================================================
    def sim_human_driven_lane2(self, i):
        driver = self.road.getCar(RIGHT,i)
        
        if driver.speed + i >= self.road.length - 1:
            self.road.setCar(RIGHT, i, EMPTY)
            self.data[2].append(self.current_step - driver.arrive_time)
            return

        if driver.type == "S":
            if self.road.safe_left_lane_change_from_Right(i):
                self.road.setCar(MIDDILE, i, driver)
                self.road.setCar(RIGHT, i, EMPTY)
                self.sim_cruise(MIDDILE, i)
            else:
                self.sim_cruise(RIGHT, i)
        else:
            self.sim_cruise(RIGHT, i)
#========================================================================================================
    def sim_cruise(self, lane, index):
        driver = self.road.getCar(lane, index)

        x = self.road.safe_distance_within(lane, index,driver.speed+driver.safe_follow)

        if x == driver.speed + driver.safe_follow:
            self.road.setCar(lane, index + driver.speed, driver) #Car moves forward by full speed
        elif x > driver.safe_follow:
            self.road.setCar(lane, index + x - driver.safe_follow, driver) #Car moves forward just enough to maintain safe_distance
        else:
            self.road.setCar(lane, index + 1, driver) #Car moves forward by just 1 spot
        self.road.setCar(lane, index, EMPTY)
#========================================================================================================
    def gen_Cars(self):
        #Self-Driven Lane: The probably of geerating a self-driving car in the left lane
        r = random.random()

        if r < SELF_PROBABILITY:
            r = random.random()

            if r < SELF_PROBABILITY1 and r > SELF_PROBABILITY2 : # this is to generate different speed self driven vehicles
                self.road.setCar(LEFT, 0, Driver("S", SELF_D1, self.current_step))
            elif r < SELF_PROBABILITY2:
                self.road.setCar(LEFT, 0, Driver("S", SELF_D2, self.current_step))
            else:
                self.road.setCar(LEFT, 0, Driver("S", SELF_D, self.current_step))
        #========================================================================================================
        #Middle Lane: The probably of geerating a human-driving car in the middle lane
        r = random.random()

        if r < HUMAN_PROBABILITY_M:
            r = random.random()
            if r < SELF_PROBABILITY: # may generate a selfdriven vehicle which has to lane change to the left lane
                self.road.setCar(MIDDILE, 0, Driver("S", SELF_D, self.current_step))
            else:
                self.road.setCar(MIDDILE, 0, Driver("H", HUMAN_D, self.current_step))
        #========================================================================================================
        #Right Lane: The probably of geerating a human-driving car in the right lane
        r = random.random()

        if r < HUMAN_PROBABILITY_R:
            r = random.random()
            if r < SELF_PROBABILITY:# may generate a selfdriven vehicle which has to lane change to the left lane
                self.road.setCar(RIGHT, 0, Driver("S", SELF_D, self.current_step))
            else:
                self.road.setCar(RIGHT, 0, Driver("H", HUMAN_D, self.current_step))
#========================================================================================================
    def averageTimeStep(self):
        # returns a a list where each index represents the number of cars passed per Lane
        #[ [self-driving lane]   [human driving lane 1]   [human driving lane 2]   [emergency lane] ]
        return [round(sum(self.data[0])/len(self.data[0]),2),round(sum(self.data[1])/len(self.data[1]),2), round(sum(self.data[2])/len(self.data[2]),2), 0]
#========================================================================================================
    def madeIt(self):
        # returns a a list where each index represents the number of cars passed per Lane
        #[ [self-driving lane]   [human driving lane 1]   [human driving lane 2]   [emergency lane] ]
        return [len(self.data[0]), len(self.data[1]), len(self.data[2]), len(self.data[3])]
#========================================================================================================
    def average_time(self):
        return sum(self.data)/len(self.data)
#========================================================================================================