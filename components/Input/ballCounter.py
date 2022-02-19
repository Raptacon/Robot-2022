import logging as log
from components.Input.breakSensors import Sensors, State
from components.Actuators.HighLevel.shooterLogic import ShooterLogic
from networktables import NetworkTables

class BallCounter:
    """Class meant to keep track of the number of balls currently in the hopper"""
    compatString = ["doof", "teapot"]
    sensors: Sensors
    shooter: ShooterLogic

    def on_enable(self):
        self.prevLoadingSensorTripped = State.kNotTripped
        self.prevMiddleSensorTripped = State.kNotTripped
        self.prevOutputSensorTripped = State.kNotTripped
        self.SmartTable = NetworkTables.getTable("SmartDashboard")
        self.hopperTable = NetworkTables.getTable("components").getSubTable("hopperMotor")
        self.SmartTable.putNumberArray("BallCount", [0, 0])
        self.ballArr = [0, 0]

    def addBall(self, pos):
        """
        Add ball at position pos (1 or 2, where 1 is the forward position)
        """
        pos -= 1
        if self.ballArr[pos] == 0:
            self.ballArr[pos] = 1
        else:
            log.error("Too many balls added")

    def subtractBall(self, pos):
        """
        Subtract ball at position pos (1 or 2, where 1 is the forward position)
        """
        pos -= 1
        if self.ballArr[pos] == 1:
            self.ballArr[pos] = 0
        else:
            log.error("Too many balls subtracted")

    def resetBallCount(self):
        """
        Resets all positions to 0 balls
        """
        self.ballArr = [0, 0]

    def getBallCount(self):
        """
        Returns array of balls in the format
        [pos1, pos2]
        where pos1 and pos2 are 0 or 1,
        1 if there is a ball
        0 if there is not
        """
        return self.ballArr

    def execute(self):

        self.currentLoadingSensorTripped = self.sensors.loadingSensor(State.kTripped)
        self.currentMiddleSensorTripped = self.sensors.middleSensor(State.kTripped)
        self.currentOutputSensorTripped = self.sensors.postShootingSensor(State.kTripped)

        # If the state of a loading sensor has changed AND it is unbroken,
        # we assume a ball has entered/left and passed a break sensor
        # and so a ball is added/subtracted
        if(self.currentLoadingSensorTripped != self.prevLoadingSensorTripped
        and self.currentLoadingSensorTripped == False
        and self.hopperTable.getEntry("isLoading")):
            self.addBall(1)

        if(self.currentMiddleSensorTripped != self.prevMiddleSensorTripped
        and self.currentMiddleSensorTripped == False):
            self.subtractBall(1)
            self.addBall(2)

        if(self.currentOutputSensorTripped != self.prevOutputSensorTripped
        and self.currentOutputSensorTripped == False):
            self.subtractBall(2)

        self.prevLoadingSensorTripped = self.currentLoadingSensorTripped
        self.prevMiddleSensorTripped = self.currentMiddleSensorTripped
        self.prevOutputSensorTripped = self.currentOutputSensorTripped
        self.SmartTable.putNumberArray("BallCount", self.ballArr)
        pass
