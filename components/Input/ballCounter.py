import logging as log
from components.Input.breakSensors import Sensors, State
from components.Input.colorSensor import ColorSensor
from components.Actuators.HighLevel.shooterLogic import ShooterLogic
from networktables import NetworkTables

class Ball:
    """
    Has position and color information
    """
    def __init__(self, color:str="None", pos=None):
        self.color = color
        self.pos = pos

    def setColor(self, color:str):
        """
        Red or Blue
        """
        self.color = color
    def setPosition(self, pos):
        """
        Either 1 or 2
        """
        self.pos = pos

    def getColor(self):
        return self.color
    def getPosition(self):
        return self.pos

class BallCounter:
    """Class meant to keep track of the number of balls currently in the hopper"""
    compatString = ["doof", "teapot"]
    sensors: Sensors
    colorSensor: ColorSensor
    shooter: ShooterLogic

    def setup(self):
        self.SmartTable = NetworkTables.getTable("SmartDashboard")
        self.hopperTable = NetworkTables.getTable("components").getSubTable("hopperMotor")
        readableArr = ["No Ball", "No Ball"]
        self.SmartTable.putStringArray("BallCount", readableArr)

    def on_enable(self):
        self.prevLoadingSensorTripped = False
        self.prevMiddleSensorTripped = False
        self.prevOutputSensorTripped = False
        self.ballArr = [None, None]

    def addBall(self, pos, color:str):
        """
        Add ball at position pos (1 or 2, where 1 is the forward position)
        """
        ball = Ball(color, pos)
        pos -= 1
        if self.ballArr[pos] == None:
            self.ballArr[pos] = ball
        else:
            log.error("Too many balls added")

    def subtractBall(self, pos):
        """
        Subtract ball at position pos (1 or 2, where 1 is the forward position)
        """
        pos -= 1
        if type(self.ballArr[pos]) == Ball:
            self.ballArr[pos] = None
        else:
            log.error("Too many balls subtracted")

    def moveBall(self, initPos, finPos):
        """
        Moves ball from initPos to finPos
        if there is a ball in initPos
        """
        if self.ballArr[initPos-1] != None:
            self.ballArr[finPos-1] = self.ballArr[initPos-1]
            self.ballArr[finPos-1].setPosition(finPos)
            self.subtractBall(initPos)

    def resetBallCount(self):
        """
        Resets all positions to 0 balls
        """
        self.ballArr = [None, None]

    def getBallCount(self):
        """
        Returns array of balls in the format
        [pos1, pos2]
        where pos1 and pos2 are
        Ball class if there is a ball
        None if there is not
        """
        return self.ballArr

    def execute(self):

        self.currentLoadingSensorTripped = self.sensors.loadingSensor(State.kTripped)
        self.currentMiddleSensorTripped = self.sensors.hopperSensor(State.kTripped)
        self.currentOutputSensorTripped = self.sensors.shootingSensor(State.kTripped)

        # If the state of a loading sensor has changed AND it is unbroken,
        # we assume a ball has entered/left and passed a break sensor
        # and so a ball is added/subtracted
        if(self.currentLoadingSensorTripped != self.prevLoadingSensorTripped
        and self.currentLoadingSensorTripped == False
        and self.hopperTable.getEntry("isLoading")):
            color = self.colorSensor.displayColor()
            self.addBall(1, color)

        if(self.currentMiddleSensorTripped != self.prevMiddleSensorTripped
        and self.currentMiddleSensorTripped == False):
            self.moveBall(1, 2)

        if(self.currentOutputSensorTripped != self.prevOutputSensorTripped
        and self.currentOutputSensorTripped == False):
            self.subtractBall(2)

        self.prevLoadingSensorTripped = self.currentLoadingSensorTripped
        self.prevMiddleSensorTripped = self.currentMiddleSensorTripped
        self.prevOutputSensorTripped = self.currentOutputSensorTripped

        # Generate readable array
        readableArr = []
        for ball in self.ballArr:
            if ball == None:
                readableArr.append("No Ball")
            elif type(ball) == Ball:
                if ball.getColor() == "none":
                    readableArr.append("Unknown Color")
                else:
                    readableArr.append(ball.getColor())
            else:
                readableArr.append("???")

        self.SmartTable.putStringArray("BallCount", readableArr)
        pass
