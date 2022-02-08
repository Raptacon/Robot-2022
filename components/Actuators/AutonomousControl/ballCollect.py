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
    travelFirstCall = False

    def startRunning(self):
        self.start = True

    def getBallDist(self):
        # Placeholder, figure this out later.
        return 5

    @state(first=True)
    def idling(self):
        """
        Starts the statemachine if requested.
        Otherwise stays here.
        """
        self.next_state("idling")
        if self.start:
            self.start = False
            self.forwardTurnSpeed = 0
            self.next_state("align")

    @state
    def align(self):
        """
        Turns the drive base towards a detected ball
        and then starts driving towards it.
        """
        # Placeholder, we need to get angle offset
        self.next_state("align")
        self.DeviationX = 90
        if self.DeviationX != 0:
            self.AbsoluteX = abs(self.DeviationX)
            self.travelFirstCall = False
            self.forwardTurnSpeed = 0
            offset = self.maxDist - self.driveTrain.getEstTotalDistTraveled()
            self.forwardTurnSpeed = self.speedSections.getSpeed(offset, "GoToDist")

            if self.ballCounter.getBallCount() != self.initBallCount:
                self.forwardTurnSpeed = 0
                self.next_state("idling")
            if self.driveTrain.getEstTotalDistTraveled() > self.maxDist:
                log.error("Missed the ball")
                self.forwardTurnSpeed = 0
                self.next_state("idling")

            if not self.DeviationX < self.angleTolerance:
                self.turnSpeed = self.speedSections.getSpeed(self.AbsoluteX, "AutoAlign")
                if self.DeviationX < 0:
                    self.turnSpeed *= -1
            self.driveTrain.setArcade(self.forwardTurnSpeed, self.turnSpeed)

        else:
            log.error("Limelight: No Valid Targets")
            self.next_state("idling")

    def initTravel(self):
        """
        Sets initial values for forward movement
        """
        self.initBallCount = self.ballCounter.getBallCount()
        self.initDist = self.driveTrain.getEstTotalDistTraveled()
        # Placeholder, will need to get data from camera
        self.dist = self.getBallDist()
        self.maxDist = self.dist + self.distTolerance + self.initDist
