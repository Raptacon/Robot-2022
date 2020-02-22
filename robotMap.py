import ConfigMapper as mapper
from wpilib import XboxController
import motorHelper
import os
import logging
from pathlib import Path

class RobotMap():
    """
    Robot map gathers all the hard coded values needed to interface with
    hardware into a single location
    """
    def __init__(self):
        """intilize the robot map"""
        configFile = self.findConfig()
        #configFile = os.path.dirname(__file__) + os.path.sep + "config.yml" #Put filename for config here, should be in the same directory as robot.py
        config = mapper.ConfigMapper(configFile)
        self.motorsMap = CANMap(config)

    def findConfig(self):
        """
        Will determine the correct yml file for the robot.
        Please run 'echo (robotCfg.yml) > robotConfig' on the robot.
        This will tell the robot to use robotCfg file remove the () and use file name file.
        Files should be configs dir
        """
        configPath = os.path.dirname(__file__) + os.path.sep + "configs" + os.path.sep
        home = str(Path.home()) + os.path.sep
        defaultConfig = configPath + "doof.yml"
        robotConfigFile = home + "robotConfig"
        

        if not os.path.isfile(robotConfigFile):
            logging.error("Could not find %s. Using default", robotConfigFile)
            robotConfigFile = configPath + "default"
        try:
            file = open(robotConfigFile)
            configFileName = file.readline().strip()
            file.close()
            configFile = configPath + configFileName
            
            if os.path.isfile(configFile):
                logging.info("Using %s config file", configFile)
                return configFile
            logging.error("No config? Can't find %s", configFile)
            logging.error("Using default %s", defaultConfig)
        except Exception as e:
            logging.error("Could not find %s", robotConfigFile)
            logging.error(e)
            logging.error("Please run `echo <robotcfg.yml> > ~/robotConcig` on the robot")
            logging.error("Using default %s", defaultConfig)

        return defaultConfig



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
        self.motors = {}

        for motorDescKey in driveMotors:
            currentMotor = driveMotors[motorDescKey]
            print("{}".format(currentMotor))
            self.motors[motorDescKey] = motorHelper.createMotor(currentMotor)
        self.driveMotors = self.motors

class XboxMap():
    """
    Holds the mappings to TWO Xbox controllers, one for driving, one for mechanisms
    """
    def __init__(self, Xbox1: XboxController, Xbox2: XboxController):
        self.drive = Xbox1
        self.mech = Xbox2
        #Button mappings
        self.controllerInput()

    def controllerInput(self):
        """
        Collects all controller values and puts them in an easily readable format
        (Should only be used for axes while buttonManager has no equal for axes)
        """
        #Drive Controller inputs
        self.driveLeft = self.drive.getRawAxis(XboxController.Axis.kLeftY)
        self.driveRight = self.drive.getRawAxis(XboxController.Axis.kRightY)
        self.driveLeftHoriz = self.drive.getRawAxis(XboxController.Axis.kLeftX)
        self.driveRightHoriz = self.drive.getRawAxis(XboxController.Axis.kRightX)
        self.driveRightTrig = self.drive.getRawAxis(XboxController.Axis.kRightTrigger)
        self.driveLeftTrig = self.drive.getRawAxis(XboxController.Axis.kLeftTrigger)
        #Mechanism controller inputs
        self.mechLeft = self.mech.getRawAxis(XboxController.Axis.kLeftY)
        self.mechRight = self.mech.getRawAxis(XboxController.Axis.kRightY)
        self.mechLeftHoriz = self.mech.getRawAxis(XboxController.Axis.kLeftX)
        self.mechRightHoriz = self.mech.getRawAxis(XboxController.Axis.kRightX)
        self.mechRightTrig = self.mech.getRawAxis(XboxController.Axis.kRightTrigger)
        self.mechLeftTrig = self.mech.getRawAxis(XboxController.Axis.kLeftTrigger)

    def getDriveController(self):
        return self.drive

    def getMechController(self):
        return self.mech

    def getDriveLeft(self):
        return self.driveLeft

    def getDriveRight(self):
        return self.driveRight

    def getDriveLeftHoriz(self):
        return self.driveLeftHoriz

    def getDriveRightHoriz(self):
        return self.driveRightHoriz

    def getDriveRightTrig(self):
        return self.driveRightTrig

    def getDriveLeftTrig(self):
        return self.driveLeftTrig

    def getMechLeft(self):
        return self.mechLeft

    def getMechRight(self):
        return self.mechRight

    def getMechLeftHoriz(self):
        return self.mechLeftHoriz

    def getMechRightHoriz(self):
        return self.mechRightHoriz

    def getMechRightTrig(self):
        return self.mechRightTrig

    def getMechLeftTrig(self):
        return self.mechLeftTrig
