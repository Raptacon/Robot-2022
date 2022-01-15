import logging as log
from utils.DirectionEnums import Direction

class HopperMotor:
    """
    Allows you to run motors in the hopper
    """
    compatString = ["doof"]

    motors_loader: dict

    def on_enable(self):
        """
        Sets up hopper motors
        """
        self.hopperSpeed = 0
        self.hopper = False

        self.hopperMotor1 = self.motors_hopper["hopperMotor1"]

        log.info("Hopper Motor Component Created")

    def runHopper(self, lSpeed, direction):
        """
        Sets the hopper motor to speed lSpeed
        """
        if direction == Direction.kForwards: # Forwards
            self.hopperSpeed = lSpeed
        elif direction == Direction.kBackwards: # Backwards
            self.hopperSpeed = -lSpeed

        self.hopper = True

    def stopHopper(self):
        """
        Turns the hopper off
        """
        self.hopper = False

    def isHopperRunning(self):
        return self.hopper

    def execute(self):
        if self.hopper:
            self.hopperMotor1.set(self.hopperSpeed)
        elif self.hopper == False:
            self.hopperMotor1.set(0)
