from magicbot import StateMachine, feedback, state, tunable
from components.Actuators.LowLevel.driveTrain import ControlMode, DriveTrain
from components.Actuators.HighLevel.driveTrainHandler import DriveTrainHandler
from components.SoftwareControl.speedSections import SpeedSections
import logging as log

class GoToDist(StateMachine):

    compatString = ["teapot"]

    driveTrainHandler: DriveTrainHandler
    driveTrain: DriveTrain
    speedSections: SpeedSections
    tolerance = tunable(.25)
    starting = False
    running = False
    targetDist = 0
    nextSpeed = 0

    def on_enable(self):
        self.starting = False
        self.running = False
        self.targetDist = 0
        self.nextSpeed = 0

    def setTargetDist(self, distance):
        """
        Call this to set the target distance
        in inches, and start
        does not change target dist if currently running
        """
        if not self.running:
            log.error("SET TARGET")
            self.targetDist = distance
            self.start(self.targetDist)

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
        self.targetDist = 0
        self.driveTrainHandler.setDriveTrain(self, ControlMode.kTankDrive, 0, 0)
        self.next_state("idling")

    @state(first=True)
    def idling(self):
        """
        Base state, kicks into
        statemachine if starting.
        """
        self.running = False
        self.initDist = 0
        if self.starting:
            log.error("Starting GoToDist")
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

        self.nextSpeed = 0
        totalOffset = self.targetDist - self.dist
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
                self.next_state("goToDist")
                self.adjust_drive()
                break

        # This might be triggered if something is wrong with the
        # values array.
        if self.nextSpeed == 0:
            log.error("Something went wrong with GoToDist!")

        if absTotalOffset < self.tolerance:
            self.stop()
            self.next_state("idling")

    @feedback
    def getSpeed(self):
        return self.nextSpeed

    @feedback
    def getTarget(self):
        return self.targetDist

    def adjust_drive(self):
        """
        This state takes the speed set by the goToDist
        state and sets the driveTrain to go forwards/
        backwards at that speed. It then goes back to
        goToDist.
        """
        self.driveTrainHandler.setDriveTrain(self, ControlMode.kArcadeDrive, -1*self.nextSpeed, 0)
