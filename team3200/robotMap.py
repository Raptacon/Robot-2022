
class RobotMap():
    """
    Robot map gathers all the hard coded values needed to interface with
    hardware into a single location
    """
    def __init__(self):
        """intilize the robot map"""
        self.motorsMap = CANMap()


class CANMap():
    """
    holds the mappins to all the motors in the robot. Both CAN and PWM
    """
    def __init__(self):
        """
        Creates default mappings
        """
        pid = None
        rampRate = .2
        driveMotors = {}
        driveMotors['right'] = {'channel':0, 'inverted':False, 'type':'CANTalon', 'pid':pid, "rampRate":rampRate}
        driveMotors['left'] = {'channel':1, 'inverted':False, 'type':'CANTalon', 'pid':pid, "rampRate":rampRate}
        self.driveMotors = driveMotors

