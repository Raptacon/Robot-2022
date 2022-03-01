from robotMap import XboxMap
from components.Actuators.LowLevel.shooterMotors import ShooterMotors
from components.Actuators.LowLevel.intakeMotor import IntakeMotor
from components.Actuators.HighLevel.hopperMotor import HopperMotor
from utils.DirectionEnums import Direction
from enum import Enum, auto
from magicbot import tunable
import logging as log

class Type(Enum):
    """Enumeration for the two types within the feeder."""
    kIntake = auto()
    kHopper = auto()

class FeederMap:
    """Simple map that holds the logic for running elements of the feeder."""

    compatString = ["doof", "teapot"]

    shooterMotors: ShooterMotors
    intakeMotor: IntakeMotor
    hopperMotor: HopperMotor
    xboxMap: XboxMap

    loaderMotorSpeed = tunable(.2)
    intakeMotorSpeed = tunable(.5)

    def on_enable(self):
        pass
        # log.setLevel(logging.DEBUG)

    def run(self, loaderFunc):
        """Called when execution of a feeder element is desired."""
        if loaderFunc == Type.kIntake:
            if self.xboxMap.getDriveLeftTrig() > 0 and self.xboxMap.getDriveRightTrig() == 0:
                self.intakeMotor.runIntake(self.intakeMotorSpeed, Direction.kForwards)
                log.debug("right trig intake", self.xboxMap.getMechRightTrig())

            elif self.xboxMap.getDriveRightTrig() > 0 and self.xboxMap.getDriveLeftTrig() == 0:
                self.intakeMotor.runIntake(self.intakeMotorSpeed, Direction.kBackwards)
                log.debug("left trig intake", self.xboxMap.getMechLeftTrig())

            else:
                self.intakeMotor.runIntake(0, Direction.kForwards)

        if loaderFunc == Type.kHopper:
            if self.xboxMap.getDriveLeftTrig() > 0 and self.xboxMap.getDriveRightTrig() == 0:
                self.hopperMotor.runHopperMotorForeside(self.loaderMotorSpeed, Direction.kForwards)
                self.hopperMotor.runHopperMotorBackside(self.loaderMotorSpeed, Direction.kForwards)
                log.debug("right trig manual", self.xboxMap.getMechRightTrig())

            elif self.xboxMap.getDriveRightTrig() > 0 and self.xboxMap.getDriveLeftTrig() == 0:
                self.hopperMotor.runHopperMotorForeside(self.loaderMotorSpeed, Direction.kBackwards)
                self.hopperMotor.runHopperMotorBackside(self.loaderMotorSpeed, Direction.kBackwards)
                log.debug("left trig manual", self.xboxMap.getMechLeftTrig())

            else:
                self.hopperMotor.stopHopperMotorBackside()
                self.hopperMotor.stopHopperMotorForeside()

    def execute(self):
        pass
