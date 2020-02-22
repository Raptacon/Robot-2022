import ConfigMapper as mapper
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
        self.driveMotors = driveMotors
