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
        self.hopperSpeed1 = 0
        self.hopper1 = False
        self.hopperSpeed2 = 0
        self.hopper2 = False

        self.hopperMotor1 = self.motors_loader["hopperMotor1"]
        self.hopperMotor2 = self.motors_loader["hopperMotor2"]

        log.info("Hopper Motor Component Created")

    def runHopper(self, lSpeed, direction):
        """
        Sets the hopper motor to speed lSpeed in direction
        :param lSpeed: double/float 0 to 1, where 0 is nothing and 1 is full speed
        :param direction: Enum Direction from utils.DirectionEnums (forwards or backwards)
        """
        if direction == Direction.kForwards: # Forwards
            self.hopperSpeed1 = lSpeed
        elif direction == Direction.kBackwards: # Backwards
            self.hopperSpeed1 = -lSpeed

        if direction == Direction.kForwards: # Forwards
            self.hopperSpeed2 = lSpeed
        elif direction == Direction.kBackwards: # Backwards
            self.hopperSpeed2 = -lSpeed

        self.hopper1 = True
        self.hopper2 = True

    def stopHopper(self):
        """
        Turns the hopper off
        """
        self.hopper1 = False
        self.hopper2 = False

    def isHopper1Running(self):
        """
        Returns True if the hopper is running.
        """
        return self.hopper1

    def isHopper2Running(self):
        """
        Returns True if the hopper is running.
        """
        return self.hopper2


    def execute(self):
        if self.hopper1:
            self.hopperMotor1.set(self.hopperSpeed)
        elif self.hopper1 == False:
            self.hopperMotor1.set(0)
        if self.hopper2:
            self.hopperMotor2.set(self.hopperSpeed)
        elif self.hopper2 == False:
            self.hopperMotor2.set(0)

