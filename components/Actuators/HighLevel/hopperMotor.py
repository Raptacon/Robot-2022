import logging as log

from magicbot import feedback, tunable
from utils.DirectionEnums import Direction
from components.Input.breakSensors import Sensors, State

class HopperMotor:
    """
    Allows you to run motors in the hopper
    """
    compatString = ["teapot"]

    motors_hopper: dict
    sensors: Sensors
    intakeSpeed = tunable(.3)
    movingSpeed = tunable(.3)

    def setup(self):
        """
        Sets up hopper motors
        """
        self.hopperSpeed1 = 0
        self.hopper1 = False
        self.hopperSpeed2 = 0
        self.hopper2 = False

    def on_enable(self):
        """
        Creates hopper motors
        """
        self.hopperMotor1 = self.motors_hopper["hopperMotor1"]
        self.hopperMotor2 = self.motors_hopper["hopperMotor2"]

        log.info("Hopper Motor Component Created")

    @feedback
    def getSpeed1(self):
        return self.hopperSpeed1
    @feedback
    def getSpeed2(self):
        return self.hopperSpeed2

    @feedback
    def isLoading(self):
        if self.hopperSpeed1 >= 0:
            return True
        return False

    def runHopperMotor1(self, lSpeed, direction):
        """
        Sets the hopper motor to speed lSpeed in direction
        :param lSpeed: double/float 0 to 1, where 0 is nothing and 1 is full speed
        :param direction: Enum Direction from utils.DirectionEnums (forwards or backwards)
        """
        if direction == Direction.kForwards: # Forwards
            self.hopperSpeed1 = lSpeed
        elif direction == Direction.kBackwards: # Backwards
            self.hopperSpeed1 = -lSpeed

        self.hopper1 = True

    def runHopperMotor2(self, lSpeed, direction):
        """
        Sets the hopper motor to speed lSpeed in direction
        :param lSpeed: double/float 0 to 1, where 0 is nothing and 1 is full speed
        :param direction: Enum Direction from utils.DirectionEnums (forwards or backwards)
        """
        if direction == Direction.kForwards: # Forwards
            self.hopperSpeed2 = lSpeed
        elif direction == Direction.kBackwards: # Backwards
            self.hopperSpeed2 = -lSpeed
        self.hopper2 = True

    def stopHopperMotor1(self):
        """
        Turns the hopper off
        """
        self.hopper1 = False

    def stopHopperMotor2(self):
        """
        Turns the hopper off
        """
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

    def checkSensors(self):
        """
        If either of the break sensors is broken,
        set its corresponding motor speed
        Only changes motor speeds if they are 0
        """
        if self.hopperSpeed1 == 0 and self.sensors.loadingSensor(State.kTripped):
            self.runHopperMotor1(self.intakeSpeed, Direction.kForwards)
        if self.hopperSpeed2 == 0 and self.sensors.middleSensor(State.kTripped):
            self.runHopperMotor2(self.movingSpeed, Direction.kForwards)

    def execute(self):
        if self.hopper1:
            self.hopperMotor1.set(self.hopperSpeed1)
        elif self.hopper1 == False:
            self.hopperMotor1.set(0)
        if self.hopper2:
            self.hopperMotor2.set(self.hopperSpeed2)
        elif self.hopper2 == False:
            self.hopperMotor2.set(0)

        # Reset speeds to give checkSensors() a chance
        # and to avoid motors running without input
        self.hopperSpeed1 = 0
        self.hopperSpeed2 = 0
        self.checkSensors()
