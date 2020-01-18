#import team3200
import commandbased
import wpilib
import ctre
import logging

log = logging.getLogger("console")
log.setLevel(logging.DEBUG)

class Robot(commandbased.CommandBasedRobot):

    def robotInit(self):
        '''This is where the robot code starts.'''
        self.controller = wpilib.Joystick(0)
        self.motor = ctre.WPI_TalonSRX(0)
        self.pwMotor = wpilib.PWMSpeedController(0)
        log.info("robot initialized")

    def operatorControl(self):
        log.info("operator control")
        while self.isOperatorControl and self.isEnabled:
            log.debug("joystick is %f y %f x", self.controller.getY(), self.controller.getX())
            wpilib.Timer.delay(.1)
            self.motor.set(self.controller.getY())
            self.pwMotor.set(self.controller.getX())
