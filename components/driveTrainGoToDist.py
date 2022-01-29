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
    # This array determines what speed the robot will use
    # at different distances.
    values = [
             [5, .15], # The first value is the limit, so it will
             [8, .2],  # use the included speed if the distance is
             [12, .25],# under this value and above the last.
             [36, .3],
             ["End", .4],
             ]  # The array must end with "End" - this will be the value used
    # if the target is really far away.

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
        """
        This is guaranteed to end whatever
        GoToDist is doing.
        """
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
        if self.starting:
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
        Sets the target variables for the loop
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

        self.nextSpeed = 0
        absTotalOffset = abs(totalOffset)

        # Loops through our speed limits in order to find the correct speed.
        # We aren't using PID, though that would be a good idea for maximum accuracy.
        for dist, speed in self.values:
            if (dist == "End"
                or absTotalOffset < dist):
                # We don't have this implemented for goToDist yet
                # if speed == "PID":
                #     self.nextSpeed = self.calc_PID(self.DeviationX)
                self.nextSpeed = speed
                self.next_state("adjust_drive")
                break

        # This might be triggered if something is wrong with the
        # values array.
        if self.nextSpeed == 0:
            log.error("Something went wrong with GoToDist!")

        if absTotalOffset < self.tolerance:
            self.stop()
            self.next_state("idling")

    @state
    def adjust_drive(self):
        """
        This state takes the speed set by the goToDist
        state and sets the driveTrain to go forwards/
        backwards at that speed. It then goes back to
        goToDist.
        """
        self.driveTrain.setArcade(self.nextSpeed, 0)
        self.next_state("goToDist")
