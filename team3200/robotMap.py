from team3200 import ConfigMapper as mapper

class RobotMap():
    """
    Robot map gathers all the hard coded values needed to interface with
    hardware into a single location
    """
    def __init__(self):
        """intilize the robot map"""
        config = mapper.ConfigMapper("team3200/config.yml")
        self.motorsMap = CANMap(config)


class CANMap():
    """
    holds the mappings to all the motors in the robot. Both CAN and PWM
    """
    def __init__(self, config):
        """
        Creates default mappings
        """
        pid = None
        rampRate = .2
        driveMotors = {}
        driveMotors['right'] = {'channel':2, 'inverted':False, 'type':'CANTalon', 'pid':pid, "rampRate":rampRate}
        driveMotors['left'] = {'channel':3, 'inverted':False, 'type':'CANTalon', 'pid':pid, "rampRate":rampRate}
        self.driveMotors = driveMotors