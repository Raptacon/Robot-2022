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
        self.hopperSpeedFore = 0
        self.hopperFore = False
        self.hopperSpeedBack = 0
        self.hopperBack = False

    def on_enable(self):
        """
        Creates hopper motors
        """
        self.hopperMotorForeward = self.motors_hopper["hopperMotorForeward"]
        self.hopperMotorBackward = self.motors_hopper["hopperMotorBackward"]

        log.info("Hopper Motor Component Created")

    @feedback
    def getSpeedFore(self):
        return self.hopperSpeedFore
    @feedback
    def getSpeedBack(self):
        return self.hopperSpeedBack

    @feedback
    def isLoading(self):
        """
        Returns true if the forward hopper motor is
        moving forward (bringing a ball in)
        false otherwise
        """
        if self.hopperSpeedFore >= 0:
            return True
        return False

    def runHopperMotorForeward(self, lSpeed, direction):
        """
        Sets the hopper motor to speed lSpeed in direction
        :param lSpeed: double/float 0 to 1, where 0 is nothing and 1 is full speed
        :param direction: Enum Direction from utils.DirectionEnums (forwards or backwards)
        """
        if direction == Direction.kForwards: # Forwards
            self.hopperSpeedFore = lSpeed
        elif direction == Direction.kBackwards: # Backwards
            self.hopperSpeedFore = -lSpeed

        self.hopperFore = True

    def runHopperMotorBackward(self, lSpeed, direction):
        """
        Sets the hopper motor to speed lSpeed in direction
        :param lSpeed: double/float 0 to 1, where 0 is nothing and 1 is full speed
        :param direction: Enum Direction from utils.DirectionEnums (forwards or backwards)
        """
        if direction == Direction.kForwards: # Forwards
            self.hopperSpeedBack = lSpeed
        elif direction == Direction.kBackwards: # Backwards
            self.hopperSpeedBack = -lSpeed
        self.hopperBack = True

    def stopHopperMotorForeward(self):
        """
        Turns the hopper off
        """
        self.hopperFore = False

    def stopHopperMotorBackward(self):
        """
        Turns the hopper off
        """
        self.hopperBack = False

    def isHopperForewardRunning(self):
        """
        Returns True if the hopper is running.
        """
        return self.hopperFore

    def isHopperBackwardRunning(self):
        """
        Returns True if the hopper is running.
        """
        return self.hopperBack

    def checkSensors(self):
        """
        If either of the break sensors is broken,
        set its corresponding motor speed
        Only changes motor speeds if they are 0
        """
        if self.hopperSpeedFore == 0 and self.sensors.loadingSensor(State.kTripped):
            self.runHopperMotorForeward(self.intakeSpeed, Direction.kForwards)
        if self.hopperSpeedBack == 0 and self.sensors.middleSensor(State.kTripped):
            self.runHopperMotorBackward(self.movingSpeed, Direction.kForwards)

    def execute(self):
        if self.hopperFore:
            self.hopperMotorForeward.set(self.hopperSpeedFore)
        elif self.hopperFore == False:
            self.hopperMotorForeward.set(0)
        if self.hopperBack:
            self.hopperMotorBackward.set(self.hopperSpeedBack)
        elif self.hopperBack == False:
            self.hopperMotorBackward.set(0)

        # Reset speeds to give checkSensors() a chance
        # and to avoid motors running without input
        self.hopperSpeedFore = 0
        self.hopperSpeedBack = 0
        self.checkSensors()
