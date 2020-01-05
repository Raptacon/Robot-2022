
class RobotMap():
    """
    Robot map gathers all the hard coded values needed to interface with
    hardware into a single location
    """
    def __init__(self):
        """intilize the robot map"""
        self.motorsMap = CANMap()


class CANMap():
    def __init__(self): 
        """ 
        holds mappings to all the motors in the robot 
        """
        pid = None 
        rampRate = .2
        driveMotors = {}
        driveMotors['rightFollower'] = {'channel':2, 'inverted':False, 'type':'CANTalon', 'pid':pid, "rampRate":rampRate}
        self.driveMotor = driveMotors

