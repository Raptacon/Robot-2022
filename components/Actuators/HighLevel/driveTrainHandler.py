import logging as log
from magicbot import AutonomousStateMachine, MagicRobot
from components.Actuators.LowLevel.driveTrain import DriveTrain

class DriveTrainHandler():
    """
    This class is how we're going to control the drivetrain
    during teleop. It gives priority to drivers.
    We shouldn't be calling the drivetrain's control methods directly now.
    """
    compatString = ["doof","teapot", "greenChassis"]
    # Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    driveTrain: DriveTrain
    Motorspeeds = {}

    currentSource = None
    prevSource = None
    controlMode = None

    def requestControl(self, requestSource):
        """
        (The preferred way to gain control is to call the set method,
        which will request control through this method anyway.)
        This method will request control of the drivetrain. If
        your request is approved (True is returned),
        then you can call the set method to
        get the DriveTrain to move.
        Only call when you want to access drivetrain.

        Priority Tree:

        High Priority:
        Driver input

        Low Priority:
        Everything Else
        (Priority is given to components who held control on previous frame)
        (Therefor, control is given to components who request control first immediately after
        driver control is relinquished. Play nice, I guess.)
        """
        # If the request comes from a descendant of MagicRobot
        # (If the request comes from robot.py)
        # give it control
        if issubclass(type(requestSource), MagicRobot):
            self.currentSource = requestSource
            return True
        if issubclass(type(requestSource), AutonomousStateMachine):
            self.currentSource = requestSource
            return True

        # I think this works.
        elif self.currentSource == None:
            if self.prevSource == None:
                self.currentSource = requestSource
                return True
            elif self.prevSource == requestSource:
                self.currentSource = requestSource
                return True
            else:
                return False

        else:
            return False

    def setDriveTrain(self, requestSource, Motorspeeds):
        """
        If you do not have control, this will request it for you.
        Sets drivetrain values and returns true if your control is valid.

        pass in self as requestSource

        If not, returns false. You must request control (through this method) every frame.
        (Yes this is wide open to abuse, but I trust you)
        """

        # If the requestSource isn't in control, check if it should be.
        if self.currentSource != requestSource:
            self.requestControl(requestSource)

        if self.currentSource == requestSource:
            self.Motorspeeds = Motorspeeds
            return True
        else:
            return False

    def execute(self):
        self.driveTrain.setMotors(self.Motorspeeds)

        self.Motorspeeds = {}

        # You must request control every frame.
        self.prevSource = self.currentSource
        self.currentSource = None
