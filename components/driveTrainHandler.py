import logging as log
from bcrypt import re
from magicbot import MagicRobot
from networktables import NetworkTables
from components.driveTrain import DriveTrain, ControlMode

class DriveTrainHandler():
    """
    This class is how we're going to control the drivetrain
    during teleop. It gives priority to drivers.
    We shouldn't be calling the drivetrain's control methods directly now.
    """
    compatString = ["doof","scorpion", "greenChassis"]
    # Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    driveTrain: DriveTrain

    currentSource = None
    prevSource = None

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

    def setDriveTrain(self, requestSource, controlMode: ControlMode, input1, input2):
        """
        If you do not have control, this will request it for you.
        Sets drivetrain values and returns true if your control is valid.
        If not, returns false. You must request control (through this method) every frame.
        (Yes this is wide open to abuse, but I trust you)
        """

        # If the requestSource isn't in control, check if it should be.
        if self.currentSource != requestSource:
            self.requestControl(requestSource)

        if self.currentSource == requestSource:
            self.input1 = input1
            self.input2 = input2
            self.controlMode = controlMode
            return True
        else:
            return False

    def setArcade(self, requestSource, speed, rotation):
        """
        Sets the drivetrain in arcade mode (if you deserve control)

        If you do not have control, this will request it for you.
        Sets drivetrain values and returns true if your control is valid.
        If not, returns false. You must request control (through this method) every frame.
        (Yes this is wide open to abuse, but I trust you)
        """
        self.setDriveTrain(self, requestSource, ControlMode.kArcadeDrive, speed, rotation)

    def setTank(self, requestSource, leftSpeed, rightSpeed):
        """
        Sets the drivetrain in tank mode (if you deserve control)

        If you do not have control, this will request it for you.
        Sets drivetrain values and returns true if your control is valid.
        If not, returns false. You must request control (through this method) every frame.
        (Yes this is wide open to abuse, but I trust you)
        """
        self.setDriveTrain(self, requestSource, ControlMode.kTankDrive, leftSpeed, rightSpeed)

    def execute(self):
        # Pass through inputs to drivetrain
        if self.controlMode == ControlMode.kArcadeDrive:
            self.driveTrain.setArcade(self.input1, self.input2)
        elif self.controlMode == ControlMode.kTankDrive:
            self.driveTrain.setTank(self.input1, self.input2)
        elif self.controlMode == ControlMode.kDisabled:
            self.driveTrain.setTank(0, 0)
        else:
            log.error("Unknown control mode")
            self.driveTrain.setTank(0, 0)

        # You must request control every frame.
        self.prevSource == self.currentSource
        self.currentSource == None
