from magicbot import StateMachine, state, tunable
from components.driveTrain import ControlMode
from components.driveTrainHandler import DriveTrainHandler
import logging as log

class GoToDist(StateMachine):

    compatString = ["doof"]

    driveTrainHandler: DriveTrainHandler
    dumbTolerance = tunable(.25)
    tolerance = tunable(.25)
    starting = False
    running = False
    targetDist = 0
    dumbSpeeds = [.3, .25, .2, .15]
    dumbSpeedLimits = [36, 12, 8, 5]

    def setTargetDist(self, distance):
        """
        Call this to set the target distance
        """
        self.targetDist = distance

    def start(self, distance=0):
        """
        Call this to start the process
        distance: optional argument, include
        in order to set the target distance.
        """
        if distance != 0:
            self.targetDist = distance
        self.starting = True

    def stop(self):
        self.running = False
        self.driveTrainHandler.setDriveTrain(self, ControlMode.kTankDrive, 0, 0)
        self.next_state("idling")

    @state(first=True)
    def idling(self):
        """
        Base state, kicks into
        statemachine if starting.
        """
        self.initDist = 0
        if self.starting and not self.running:
            if self.targetDist != 0:
                self.next_state("recordInitDist")
            else:
                log.error("Must set target dist before calling start")
                self.next_state("idling")
        else:
            self.next_state("idling")

    @state
    def recordInitDist(self):
        """
        First active state.
        """
        self.running = True
        self.starting = False
        self.initDist = self.driveTrain.getEstTotalDistTraveled()
        self.targetDist = self.initDist + self.targetDist
        self.next_state("goToDist")

    @state
    def goToDist(self):
        """
        Feedback loop using the
        drivetrain in order to travel
        a certain distance.
        """
        self.dist = self.driveTrain.getEstTotalDistTraveled()
        self.dumbSpeed = 0

        self.nextSpeed = 0
        totalOffset = self.targetDist - self.dist
        for i, limit in enumerate(self.dumbSpeedLimits):
            if abs(totalOffset) > limit:
                self.dumbSpeed = self.dumbSpeeds[i]
                break

        if self.dumbSpeed == 0:
            self.dumbSpeed = self.dumbSpeeds[-1]

        if self.dist < self.targetDist - self.dumbTolerance:
            self.nextSpeed = -1 * self.dumbSpeed
            self.next_state("goToDist")
        elif self.dist > self.targetDist + self.dumbTolerance:
            self.nextSpeed = self.dumbSpeed
            self.next_state("goToDist")
        if self.dist > self.targetDist - self.tolerance and self.dist < self.targetDist - self.tolerance:
            self.nextSpeed = 0
            self.stop()
            self.next_state("idling")

        self.driveTrainHandler.setDriveTrain(self, ControlMode.kArcadeDrive, self.nextSpeed, 0)
