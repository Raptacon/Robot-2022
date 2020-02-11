import ConfigMapper as mapper
import platform

class RobotMap():
    """
    Robot map gathers all the hard coded values needed to interface with
    hardware into a single location
    """
    def __init__(self):
        """intilize the robot map"""
        configFileName = "config.yml" #Put filename for config here, should be in the same directory as robotMap.py


        if platform.system() == "Linux": # added to accomodate the bot - It doesn't run with just "config.yml". I imagine that there's a better way to do this, either finding if you're on the roborio or just working around it
            config = mapper.ConfigMapper("/home/lvuser/py/" + configFileName)
        else:
            config = mapper.ConfigMapper(configFileName)

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
