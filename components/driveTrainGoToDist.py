from magicbot import StateMachine, state, tunable
from components.driveTrain import DriveTrain
import logging as log

class GoToDist(StateMachine):

    compatString = ["doof"]

    driveTrain: DriveTrain
    dumbTolerance = tunable(.25)
    tolerance = tunable(.25)
    starting = False
    running = False
    targetDist = 0
    values = [
             [5, .15],
             [8, .2],
             [12, .25],
             [36, .3]
             ["End", .4]
             ]

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
        self.driveTrain.setArcade(0, 0)
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

        self.speed = 0
        absTotalOffset = abs(totalOffset)
        for dist, speed in self.values:
            if (dist == "End"
                or absTotalOffset < dist):
                # We don't have this implemented for goToDist yet
                # if speed == "PID":
                #     self.speed = self.calc_PID(self.DeviationX)
                self.nextSpeed = speed
                self.next_state("adjust_drive")
                break

    @state
    def adjust_drive(self):
        self.driveTrain.setArcade(self.nextSpeed, 0)
