# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
#from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5 

# For Python 3.6:
#from ps2_verify_movement36 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6

#For Python 3.8 (my version) testing:
from ps2_verify_movement38 import testRobotMovement

# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
# Note: raise NotImplementedError can be deleted once function is implemented
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.tiles = {} #set tiles as a dictionary
        #Set the initial tiles that has key(i,j) as dirty 
        for i in range(width+1):
            for j in range(height+1): 
                self.tiles[(i,j)] = False # Initial state for dirty, clean will be True
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        # Use math.floor to mark the tile with integer (x,y) pair as clean
        self.tiles[(math.floor(pos.getX()),math.floor(pos.getY()))] = True

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        assert self.width > m
        assert self.height > n
        if self.tiles[(m,n)] == True:
            return True
        else:
            return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        cleanedTiles = 0
        listAllTiles = [(i,j) for i in range(0,self.width) for j in range(self.height)]
        for tile in listAllTiles:
            if self.tiles[tile] == True:
                cleanedTiles += 1
        return cleanedTiles

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        widthOfRoom = self.width
        heightOfRoom = self.height
        # The value generated will be random and will not include widthOfRoom or heightOfRoom,
        # but 0 will be included
        randomPosition = Position(random.randrange(0,widthOfRoom),random.randrange(0,heightOfRoom))
        return randomPosition

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        #Note: (0,0) tile is in the room, but (width,height) tile is not in the room
        if 0 <= pos.getX() < self.width and 0 <= pos.getY() < self.height:
            return True
        elif pos.getX() < 0 or pos.getY() < 0:
            return False
        else:
            return False


# === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        random.seed() # for testing leave seed = 9
        randomDirection = random.randrange(0,360)
        x_position = random.randrange(0, room.width)
        y_position = random.randrange(0, room.height)
        randomPosition = Position(x_position, y_position)
        self.room = room
        self.speed = speed
        self.direction = randomDirection
        self.position = randomPosition
        room.cleanTileAtPosition(randomPosition)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # Since speed is constant, each time-step the robot can move a distance
        # equal to speed s
        # Move first and then clean is the correct strategy according to Richard
        nextPosition = self.getRobotPosition().getNewPosition(self.direction, self.speed)
        # Check to make sure that the next position is inbound before moving
        if self.room.width > nextPosition.getX() >= 0 and self.room.height > nextPosition.getY() >= 0:
            #Move to a new position
            self.position = self.getRobotPosition().getNewPosition(self.direction, self.speed)
            #Clean the new position
            self.room.cleanTileAtPosition(self.position)
        # If the next position is out of bound in any of these 4 cases
        elif nextPosition.getX() < 0 or nextPosition.getY() < 0 or \
             nextPosition.getX() > self.room.width or nextPosition.getY() > self.room.height: 
            #Create a new direction and give this direction to the robot
            self.direction = random.randrange(0,360)
            nextPosition = self.getRobotPosition().getNewPosition(self.direction, self.speed)
            #Retest the next position again to make sure that it's inbound
            if self.room.width > nextPosition.getX() >= 0 and self.room.height > nextPosition.getY() >= 0:
                #Move and then clean
                self.position = self.getRobotPosition().getNewPosition(self.direction, self.speed) 
                self.room.cleanTileAtPosition(self.position)

        
        #This code below failed 1 test, at 8/10
        #The reason why this is failing the test is because the newDirection value only 
        # happens in the case where it goes out of bound. In other words, the direction of the 
        # robot is not updated once it goes out of bounds
        # nextPosition = self.getRobotPosition().getNewPosition(self.direction, self.speed)
        # # Check to make sure that the next position is inbound before moving
        # if self.room.width > nextPosition.getX() >= 0 and self.room.height > nextPosition.getY() >= 0:
        #     #Move to a new position
        #     self.position = self.getRobotPosition().getNewPosition(self.direction, self.speed)
        #     #Clean the new position
        #     self.room.cleanTileAtPosition(self.position)
        # elif nextPosition.getX() < 0 or nextPosition.getY() < 0: 
        #     newDirection = random.randrange(0,360)
        #     nextPosition = self.getRobotPosition().getNewPosition(newDirection, self.speed)
        #     if self.room.width > nextPosition.getX() >= 0 and self.room.height > nextPosition.getY() >= 0:
        #         self.position = self.getRobotPosition().getNewPosition(newDirection, self.speed) 
        #         self.room.cleanTileAtPosition(self.position)
        # elif nextPosition.getX() > self.room.width or nextPosition.getY() > self.room.height: 
        #     newDirection = random.randrange(0,360)
        #     nextPosition = self.getRobotPosition().getNewPosition(newDirection, self.speed)
        #     if self.room.width > nextPosition.getX() >= 0 and self.room.height > nextPosition.getY() >= 0:
        #         self.position = self.getRobotPosition().getNewPosition(newDirection, self.speed) 
        #         self.room.cleanTileAtPosition(self.position)        
            
# Uncomment this line to see your implementation of StandardRobot in action!
# testRobotMovement(StandardRobot, RectangularRoom)

# === Problem 4
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    allTrialRecords = []
    for t in range(num_trials): 
        allTrialRecords.append(oneTrialSimulation(num_robots,speed,width,height,min_coverage,robot_type))
    meanTimeNeeded = sum(allTrialRecords) / len(allTrialRecords)
    return meanTimeNeeded

def oneTrialSimulation(num_robots, speed, width, height, min_coverage, robot_type):
    """
    Parameters
    ----------
    num_robots : int > 0
        Number of robots in the room
    speed : float > 0
        speed of each robot
    width : int > 0
        width of the room
    height : int > 0
        height of the room
    min_coverage : 0 <= float <= 1 
        the coverage of the room necessary to
    robot : class of robot

    Returns
    -------
    The time steps it takes to clean the minimum coverage of the room
    Int > 0, each time step can be thought of as when a robot (or group of 
    robots) updates its position and cleans a tide
    """
    # To create animation, the higher the delay number (the last number), the slower
    # the animation will move. The default is 0.2 (that is, 5 frames per second). 
    # anim = ps2_visualize.RobotVisualization(num_robots, width, height, 0.1)
    room = RectangularRoom(width, height)
    totalTileNumber = room.getNumTiles()
    # Calculate the number of tiles that need to be cleaned
    numberTilesRequired = totalTileNumber * min_coverage
    timeSteps = 0 
    # Code to create all the robots, mapping to a list
    instanceRobot = []
    for i in range(num_robots): 
        instanceRobot.append(robot_type(room, speed))
    # The code below is how to pass in the abstract class, so any class of robot can be used
    # This code was used to create just 1 robot
    # instanceRobot = robot_type(room, speed)
    #Keep cleaning while the number of clean tiles is still smaller than number of tiles required
    while room.getNumCleanedTiles() < numberTilesRequired:
        #Update the position of all the robots and make them clean
        for i in range(num_robots):
            # anim.update(room, instanceRobot) # to update the animation before robots update their pos
            instanceRobot[i].updatePositionAndClean()
        timeSteps += 1 #only increase by 1 after all robots have been updated
    # anim.done() #to conclude the animation
    return timeSteps
    
# Make sure to delete the seed number in Robot class to get different random results
# Uncomment this line to see how much your simulation takes on average
# avg = runSimulation(10, 1.0, 15, 20, 0.8, 30, StandardRobot)
# print(runSimulation(2, 1.0, 10, 10, 0.75, 30, StandardRobot))


# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # Move first and then clean is the correct strategy according to Richard
        nextPosition = self.getRobotPosition().getNewPosition(self.direction, self.speed)
        # Check to make sure that the next position is inbound before moving
        if self.room.width > nextPosition.getX() >= 0 and self.room.height > nextPosition.getY() >= 0:
            #Move to a new position
            self.position = self.getRobotPosition().getNewPosition(self.direction, self.speed)
            #Clean the new position
            self.room.cleanTileAtPosition(self.position)
            # After finished cleaning, change the direction of the robot
            self.direction = random.randrange(0,360)
        # If the next position is out of bound in any of these 4 cases
        elif nextPosition.getX() < 0 or nextPosition.getY() < 0 or \
             nextPosition.getX() > self.room.width or nextPosition.getY() > self.room.height: 
            #Create a new direction and give this direction to the robot
            self.direction = random.randrange(0,360)
            nextPosition = self.getRobotPosition().getNewPosition(self.direction, self.speed)
            #Retest the next position again to make sure that it's inbound
            if self.room.width > nextPosition.getX() >= 0 and self.room.height > nextPosition.getY() >= 0:
                #Move and then clean
                self.position = self.getRobotPosition().getNewPosition(self.direction, self.speed) 
                self.room.cleanTileAtPosition(self.position)

#Use this for testing
# testRobotMovement(RandomWalkRobot, RectangularRoom)

def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11) # from 1 to 10
    times1 = [] #Standard Robot
    times2 = [] #Random Walk Robot
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = [] # Standard Robot
    times2 = [] # Random Walk Robot
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

# Something like below along with the needed code would allow you to run the code
#  w/o commenting/uncommenting lines
# runSimulation(num_robots, speed, width, height, min_coverage, num_trials, 
#               robot_type, Visualize = False)

# === Problem 6
# NOTE: If you are running the simulation, you will have to close it 
# before the plot will show up.

#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
# showPlot1("Time it takes 1-10 robots to clean 80% of a room", "Number \
# of robots", "Time steps needed")
#

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
# showPlot2("Time it takes 2 robots to clean 80% of variously shaped rooms", "Room width/height",\
#           "Time steps needed")
#
