from magicbot import StateMachine, feedback, state, tunable
from components.Actuators.LowLevel.driveTrain import DriveTrain
from components.Actuators.HighLevel.driveTrainHandler import DriveTrainHandler
from components.SoftwareControl.speedSections import SpeedSections
import logging as log

# This will likely all become far less useful upon implementation of odometry - already it relies on features from a tank-only drivetrain
# So it's basically functionless right now

class GoToDist(StateMachine):

    compatString = ["teapot"]

    driveTrainHandler:DriveTrainHandler
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
        # Convert to XYR
        # self.driveTrainHandler.setDriveTrain(self, ControlMode.kTankDrive, 0, 0)
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
        self.initDist = 0
        self.targetDist = self.initDist + self.targetDist
        self.next_state("goToDist")

    @state
    def goToDist(self):
        """
        Feedback loop using the
        drivetrain in order to travel
        a certain distance.
        """
        # Replaced outdated method
        self.dist = 0

        self.nextSpeed = 0
        totalOffset = self.targetDist - self.dist
        absTotalOffset = abs(totalOffset)

        self.nextSpeed = self.speedSections.getSpeed(totalOffset, "GoToDist")

        if absTotalOffset < self.tolerance:
            self.stop()
            self.next_state("idling")
        else:
            self.adjust_drive()

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
        # Convert to XYR
        # self.driveTrainHandler.setDriveTrain(self, ControlMode.kArcadeDrive, -1*self.nextSpeed, 0)
