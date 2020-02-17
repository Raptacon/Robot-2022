import ConfigMapper as mapper
import os
from wpilib import XboxController
from components.buttonManager import ButtonManager, ButtonEvent

class RobotMap():
    """
    Robot map gathers all the hard coded values needed to interface with
    hardware into a single location
    """
    def __init__(self):
        """intilize the robot map"""
        configFile = os.path.dirname(__file__) + os.path.sep + "config.yml" #Put filename for config here, should be in the same directory as robot.py
        config = mapper.ConfigMapper(configFile)
        self.motorsMap = CANMap(config)

class CANMap():
    """
    Holds the mappings to all the motors in the robot. Both CAN and PWM
    """
    def __init__(self, config):
        """
        Creates default mappings
        """
        driveMotors = config.getDicts()
        print("DRIVEMOTORS: {}".format(driveMotors['leftMotor']))
        self.driveMotors = driveMotors

class XboxMap():
    """
    Holds the mappings to TWO Xbox controllers, one for driving, one for mechanisms
    """
    def __init__(self, Xbox1: XboxController, Xbox2: XboxController):
        
        self.drive = Xbox1
        self.mech = Xbox2
        #Button mappings
        

    def controllerInput(self):
        """
        Collects all controller values and puts them in an easily readable format 
        (Should only be used for axes while buttonManager has no equal for axes)
        """
        #Drive Controller inputs
        self.driveLeft = self.drive.getRawAxis(1)
        self.driveRight = self.drive.getRawAxis(5)
        self.driveLeftHoriz = self.drive.getRawAxis(0)
        self.driveRightHoriz = self.drive.getRawAxis(4)
        self.driveRightTrig = self.drive.getRawAxis(3)
        self.driveLeftTrig = self.drive.getRawAxis(2)
        #Mechanism controller inputs
        self.mechLeft = self.mech.getRawAxis(1)
        self.mechRight = self.mech.getRawAxis(5)
        self.mechLeftHoriz = self.mech.getRawAxis(0)
        self.mechRightHoriz = self.mech.getRawAxis(4)
        self.mechRightTrig = self.mech.getRawAxis(3)
        self.mechLeftTrig = self.mech.getRawAxis(2)

    def getDriveLeft(self):
        return driveLeft

    def getDriveRight(self):
        return driveRight

    def getDriveLeftHoriz(self):
        return driveLeftHoriz

    def getDriveRightHoriz(self):
        return driveRightHoriz

    def getDriveRightTrig(self):
        return driveRightTrig

    def getDriveLeftTrig(self):
        return driveLeftTrig
    
    def getMechLeft(self):
        return mechLeft

    def getMechRight(self):
        return mechRight

    def getMechLeftHoriz(self):
        return mechLeftHoriz

    def getMechRightHoriz(self):
        return mechRightHoriz

    def getMechRightTrig(self):
        return mechRightTrig

    def getMechLeftTrig(self):
        return mechLeftTrig
