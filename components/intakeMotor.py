import logging as log
from utils.DirectionEnums import Direction

class IntakeMotor:
    """
    Allows you to run motors in the intake
    """
    compatString = ["doof"]

    def on_enable(self):
        """
        Sets up shooter motors
        """
        self.intakeSpeed = 0
        self.intake = False

        self.intakeMotor = self.motors_loader["intakeMotor"]

        log.info("Intake Motor Component Created")

    motors_loader: dict

    def runIntake(self, iSpeed, direction):
        """
        Sets the intake to speed iSpeed in direction
        iSpeed: double/float 0 to 1, where 0 is nothing and 1 is full speed
        direction: Enum Direction from utils.DirectionEnums (forwards or backwards)
        """
        if direction == Direction.kForwards:  # Forwards
            self.intakeSpeed = iSpeed
        elif direction == Direction.kBackwards: # Backwards
            self.intakeSpeed = -iSpeed
        elif direction == Direction.kDisabled:
            self.intakeSpeed = 0

        self.intake = True

    def stopIntake(self):
        """
        Turns the intake off
        """
        self.intake = False

    def isIntakeRunning(self):
        """
        Returns True if the intake is running.
        """
        return self.intake

    def execute(self):
        if self.intake:
            self.intakeMotor.set(self.intakeSpeed)
        elif self.intake == False:
            self.intakeMotor.set(0)
