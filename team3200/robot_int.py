import ctre
from wpilib import XboxController
import wpilib


class Team3200Robot(wpilib.IterativeRobot):

    def robotInit(self):
        '''This is where the robot code starts.'''
        pass

    def testInit(self):
        """
        Function called when testInit is called. Crashes on 2nd call right now
        """
        self.left = ctre.WPI_TalonFX(30)
        self.left.setInverted(True)
        self.leftf = ctre.WPI_TalonFX(31)
        self.leftf.setInverted(True)
        self.leftf.set(ctre.ControlMode.Follower, 30)
        self.right = ctre.WPI_TalonFX(40)
        self.rightF = ctre.WPI_TalonFX(41)
        self.rightF.set(ctre.ControlMode.Follower, 40)        
        self.stick = XboxController(0)
        print("Stick %s, left %s, right %s", self.stick, self.left, self.right)

    def testPeriodic(self):
        """
        Called during test mode alot
        """
        left = self.stick.getRawAxis(1)
        right = self.stick.getRawAxis(5)
        #self.logger.info("Left %f Right %f", left, right)
        self.left.set(left)
        #self.leftf.set(left)
        self.right.set(right)
        #self.rightf.set(right)
