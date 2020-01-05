#import team3200
import wpilib
import commandbased

import team3200

class Robot(commandbased.CommandBasedRobot):
    
    def robotInit(self): 
        '''This is where the robot code starts.'''
        Robot = lambda x=0:self
        self.map = team3200.robotMap

