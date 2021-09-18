from robotMap import XboxMap
from components.shooterMotors import ShooterMotorCreation, Direction
from enum import Enum, auto
from magicbot import tunable
import logging as log

class Type(Enum):
    """Enumeration for the two types within the feeder."""
    kIntake = auto()
    kLoader = auto()

class FeederMap:
    """Simple map that holds the logic for running elements of the feeder."""

    compatString = ["doof"]

    shooterMotors: ShooterMotorCreation
    xboxMap: XboxMap

    loaderMotorSpeed = tunable(.4)
    intakeMotorSpeed = tunable(.7)

    def on_enable(self):
        pass
        # log.setLevel(logging.DEBUG)

    def run(self, loaderFunc):
        """Called when execution of a feeder element is desired."""
        if loaderFunc == Type.kIntake:
            if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
                self.shooterMotors.runIntake(self.intakeMotorSpeed, Direction.kForwards)
                log.debug("right trig intake", self.xboxMap.getMechRightTrig())

            elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
                self.shooterMotors.runIntake(self.intakeMotorSpeed, Direction.kBackwards)
                log.debug("left trig intake", self.xboxMap.getMechLeftTrig())

            else:
                self.shooterMotors.runIntake(0, Direction.kForwards)

        if loaderFunc == Type.kLoader:
            if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
                self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kForwards)
                log.debug("right trig manual", self.xboxMap.getMechRightTrig())

            elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
                self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kBackwards)
                log.debug("left trig manual", self.xboxMap.getMechLeftTrig())

            else:
                self.shooterMotors.runLoader(0, Direction.kForwards)


    def execute(self):
        pass
