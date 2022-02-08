from networktables import NetworkTables as networktable
from components.SoftwareControl.speedSections import SpeedSections
from components.Actuators.LowLevel.driveTrain import DriveTrain
from components.Input.ballCounter import BallCounter
from magicbot import StateMachine, state
import logging as log

class BallCollect(StateMachine):
    compatString = ["teapot"]

    speedSections: SpeedSections
    driveTrain: DriveTrain
    ballCounter: BallCounter

    # In degrees
    angleTolerance = .25
    # In feet
    distTolerance = 1

    def startRunning(self):
        self.start = True

    @state
    def idling(self):
        if self.start:
            self.start = False
            self.forwardTurnSpeed = 0
            self.next_state("align")

    @state
    def align(self):
        # Placeholder, we aren't planning to use limelight
        self.DeviationX = self.limeTable.getNumber("tx", -50)
        if self.DeviationX != -50 or self.DeviationX != 0:
            # "-50" is the default value, so if that is returned,
            # nothing should be done because there is no connection.

            self.AbsoluteX = abs(self.DeviationX)
            if self.AbsoluteX < self.angleTolerance:
                self.speed = 0
                self.initTravel()
                self.next_state("travel")
            else:
                self.speed = self.speedSections.getSpeed(self.AbsoluteX, "AutoAlign")
                if self.DeviationX < 0:
                    self.speed *= -1
                self.next_state("align")
            self.driveTrain.setArcade(self.forwardTurnSpeed, self.speed)

        else:
            log.error("Limelight: No Valid Targets")
            self.next_state("idling")

    def initTravel(self):
        self.initBallCount = self.ballCounter.getBallCount()
        self.initDist = self.driveTrain.getEstTotalDistTraveled()
        # Placeholder, will need to get data from camera
        self.dist = 9
        self.maxDist = self.dist + self.distTolerance + self.initDist

    @state
    def travel(self):
        """
        Takes input from ballCounter to determine
        if we have picked up a ball or not.
        If a ball collection hasn't happened after a few feet,
        disengage.
        """
        # Placeholder, we need a visible ball check
        ballVisible = True

        self.next_state("travel")
        offset = self.maxDist - self.driveTrain.getEstTotalDistTraveled()
        self.speed = self.speedSections.getSpeed(offset, "GoToDist")

        if not ballVisible:
            self.forwardTurnSpeed = .1
            self.speed = 0
            self.next_state("align")

        if self.ballCounter.getBallCount() != self.initBallCount:
            self.speed = 0
            self.next_state("idling")
        if self.driveTrain.getEstTotalDistTraveled() > self.maxDist:
            log.error("Missed the ball")
            self.speed = 0
            self.next_state("idling")

        self.driveTrain.setArcade(self.speed, 0)
