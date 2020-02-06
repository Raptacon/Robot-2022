import ConfigMapper as mapper

class RobotMap():
    """
    Robot map gathers all the hard coded values needed to interface with
    hardware into a single location
    """
    def __init__(self):
        """intilize the robot map"""
        config = mapper.ConfigMapper("config.yml") #Put filename for config here, should be in the same directory as robotMap.py
        self.motorsMap = CANMap(config)


class CANMap():
    """
    holds the mappings to all the motors in the robot. Both CAN and PWM
    """
    def __init__(self, config):
        """
        Creates default mappings
        """
        driveMotors = config.getDicts()
        print("DRIVEMOTORS: {}".format(driveMotors['leftMotor']))
        self.driveMotors = driveMotors