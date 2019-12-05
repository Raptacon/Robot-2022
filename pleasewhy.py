#import team3200
import wpilib
import commandbased
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
        '''
        holds mappings to all the motors in the robot
        '''
        pid = None
        rampRate = .2
        driveMotors = {}
        driveMotors['rightFollower'] = {'channel':2, 'inverted':False, 'type':'CANTalon', 'pid':pid, "rampRate":rampRate}
        self.driveMotors = driveMotors
class MyRobot(commandbased.CommandBasedRobot):
    
    def robotInit(self): 
        '''This is where the robot code starts.'''
        Robot = lambda x=0:self
        self.map = RobotMap()
if __name__ == '__main__':
    try:
        #patch no exit error if not running on robot
        try:
            print(wpilib._impl.main.exit)
        except:
            wpilib._impl.main.exit = exit
            
        #fixes simulation rerun errors.
        #todo verify this causes no issues on robot
        wpilib.DriverStation._reset()

        #patch simulation
        #we update the simluation files to ours. If we update WPIlib these may break
        import sim
        import pyfrc.sim
        import pyfrc.sim.pygame_joysticks
        pyfrc.sim.SimUI = sim.ui.SimUI
        pyfrc.sim.pygame_joysticks.UsbJoysticks = sim.pygame_joysticks.UsbJoysticks
    except Exception as err:
            print("Failed to patch runtime. Error", err)
    
    wpilib.run(MyRobot,physics_enabled=True)