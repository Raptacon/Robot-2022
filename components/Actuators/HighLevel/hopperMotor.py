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
    intakeSpeed = tunable(.15)
    movingSpeed = tunable(.11)

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
        self.hopperMotorForeside = self.motors_hopper["hopperMotorForeside"]
        self.hopperMotorBackside = self.motors_hopper["hopperMotorBackside"]

        log.info("Hopper Motor Component Created")

    @feedback
    def getSpeedFore(self):
        """
        Gets the speed of the foreside hopper motor
        """
        return self.hopperSpeedFore
    @feedback
    def getSpeedBack(self):
        """
        Gets the speed of the backside hopper motor
        """
        return self.hopperSpeedBack

    @feedback
    def isLoading(self):
        """
        Returns true if the foreside hopper motor is
        moving forward (bringing a ball in)
        false otherwise
        """
        if self.hopperSpeedFore >= 0:
            return True
        return False

    def runHopperMotorForeside(self, lSpeed, direction):
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

    def runHopperMotorBackside(self, lSpeed, direction):
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

    def stopHopperMotorForeside(self):
        """
        Turns the hopper off
        """
        self.hopperFore = False

    def stopHopperMotorBackside(self):
        """
        Turns the hopper off
        """
        self.hopperBack = False

    def isHopperForesideRunning(self):
        """
        Returns True if the hopper is running.
        """
        return self.hopperFore

    def isHopperBacksideRunning(self):
        """
        Returns True if the hopper is running.
        """
        return self.hopperBack

    def checkSensors(self):
        """
        If either of the break sensors is broken,
        set its corresponding motor speed
        """
        if self.sensors.loadingSensor(State.kTripped):
            self.runHopperMotorForeside(self.intakeSpeed, Direction.kForwards)
        else:
            self.stopHopperMotorForeside()

        if self.sensors.hopperSensor(State.kTripped):
            self.runHopperMotorBackside(self.movingSpeed, Direction.kForwards)
        else:
            self.stopHopperMotorBackside()

    def execute(self):
        """
        Runs motors with set values, checks sensors
        """
        if self.hopperFore:
            self.hopperMotorForeside.set(self.hopperSpeedFore)
        elif self.hopperFore == False:
            self.hopperMotorForeside.set(0)
        if self.hopperBack:
            self.hopperMotorBackside.set(self.hopperSpeedBack)
        elif self.hopperBack == False:
            self.hopperMotorBackside.set(0)

        self.checkSensors()
