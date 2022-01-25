import logging as log
from networktables import NetworkTables
from components.driveTrain import DriveTrain, ControlMode

from magicbot import tunable, feedback
class DriveTrain():
    compatString = ["doof","scorpion", "greenChassis"]
    # Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    driveTrain: DriveTrain

    def setup(self):
        pass

    def requestControl(self, requestSource):
        self.currentSource = requestSource
        return True

    def setDriveTrain(self, requestSource, controlMode: ControlMode, input1, input2):
        """
        Sets drivetrain values and returns true IF the requestSource
        is the current source of input. If not, returns false.
        If you would like control, call requestControl().
        """
        if self.currentSource == requestSource:
            self.input1 = input1
            self.input2 = input2
            self.controlMode = controlMode
            return True
        else:
            return False

    def execute(self):
        if self.controlMode == ControlMode.kArcadeDrive:
            self.driveTrain.setArcade(self.input1, self.input2)
        elif self.controlMode == ControlMode.kTankDrive:
            self.driveTrain.setTank(self.input1, self.input2)
        elif self.controlMode == ControlMode.kDisabled:
            self.driveTrain.setTank(0, 0)
        else:
            log.error("Unknown control mode")
            self.driveTrain.setTank(0, 0)