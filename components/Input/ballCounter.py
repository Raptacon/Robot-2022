import logging as log
from components.Input.breakSensors import Sensors, State
from components.Actuators.HighLevel.shooterLogic import ShooterLogic
from networktables import NetworkTables

class BallCounter:
    """Class meant to keep track of the number of balls currently in the hopper"""

    SmartTable = NetworkTables.getTable("SmartDashboard")
    compatString = ["doof"]
    sensors: Sensors
    shooter: ShooterLogic
    maxBalls = 4

    def on_enable(self):
        self.prevLoadingSensorTripped = State.kNotTripped
        self.prevShootngSensorTripped = State.kNotTripped
        self.ballCount = None

    def addBall(self):
        if self.ballCount <= self.maxBalls:
            self.ballCount += 1
        else:
            log.error("Too many balls added")

    def subtractBall(self):
        if self.ballCount == 0:
            log.error("Too many balls subtracted")
        else:
            self.ballCount -= 1

    def resetBallCount(self):
        """
        Reset the variable ballCount to 0
        """
        self.ballCount = 0

    def getBallCount(self):
        return self.ballCount

    def setBallCount(self, balls):
        self.ballCount = balls

    def execute(self):

        # If the variable hasn't been initialized, assume there are no balls.
        if self.ballCount == None:
            self.ballCount = 0

        self.currentLoadingSensorTripped = self.sensors.loadingSensor(State.kTripped)
        self.currentShootngSensorTripped = self.sensors.shootingSensor(State.kTripped)

        # If the state of a loading sensor has changed AND it is unbroken,
        # we assume a ball has entered/left and passed a break sensor
        # and so a ball is added/subtracted
        if(self.currentLoadingSensorTripped != self.prevLoadingSensorTripped
        and self.currentLoadingSensorTripped == False):
            self.addBall()

        # We add an extra shooting condition so that backing the balls out of the shooter
        # doesn't trip this subtraction.
        if(self.currentShootngSensorTripped != self.prevShootngSensorTripped
        and self.currentShootngSensorTripped == False and self.shooter.shooting):
            self.subtractBall()

        self.prevLoadingSensorTripped = self.currentLoadingSensorTripped
        self.prevShootngSensorTripped = self.currentShootngSensorTripped
        self.SmartTable.putNumber("BallCount", self.ballCount)
        pass
