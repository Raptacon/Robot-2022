from components.Actuators.HighLevel.driveTrainHandler import DriveTrainHandler
from components.Actuators.LowLevel.driveTrain import ControlMode
from magicbot import tunable, feedback, StateMachine, state

import navx

class TurnToAngle(StateMachine):
    compatString = ["doof", "greenChassis", "teapot"]

    navx = navx._navx.AHRS.create_spi()
    driveTrainHandler: DriveTrainHandler
    starting = False
    running = False
    initialHeading = 0
    nextHeading = 0
    heading = 0
    originalHeading = 0
    turnAngle = 0
    dumbSpeed = tunable(.25)
    farMultiplier = tunable(1)
    midMultiplier = tunable(.75)
    closeMultiplier = tunable(.6)
    tolerance = tunable(.5)
    change = 0

    def setup(self):
        self.originalHeading = self.navx.getFusedHeading()

    def setAngle(self, angle):
        """Sets the desired turn angle"""
        self.turnAngle = angle

    @state(first = True)
    def idling(self):
        """Stays in this state until started"""
        if self.turnAngle != 0:
            self.initialHeading = self.navx.getFusedHeading()
            self.next_state("turn")
        else:
            self.next_state("idling")


    def calcHeading(self):
        """Calculates how far away from the desired angle the bot is"""
        self.running = True
        self.starting = False
        self.nextHeading = self.initialHeading + self.turnAngle

        if self.nextHeading > 360:
            self.nextHeading -= 360
        elif self.nextHeading < 0:
            self.nextHeading += 360

        self.change = self.nextHeading - self.navx.getFusedHeading()
        if self.change > 180:
            self.change -= 360
        elif self.change < -180:
            self.change += 360

    def setSpeedFunc(self):
        """Determines the speed based off of the distance from the desired angle"""
        self.calcHeading()
        if abs(self.change) > 90:
            self.speed = self.dumbSpeed * self.farMultiplier
        elif abs(self.change) <= 90 and abs(self.change) > 20:
            self.speed = self.dumbSpeed * self.midMultiplier
        else:
            self.speed = self.dumbSpeed * self.closeMultiplier

    @state
    def turn(self):
        """Turns the robot based off of the speed determined in setSpeedFunc"""
        self.setSpeedFunc()
        if self.change > 0:
            self.driveTrainHandler.setDriveTrain(self, ControlMode.kTankDrive, -1 * self.speed, self.speed)
        else:
            self.driveTrainHandler.setDriveTrain(self, ControlMode.kTankDrive, self.speed, -1 * self.speed)
        self.next_state("turn")

        """Stops the automatic turning if the bot is within the tolerance of the desired angle"""
        if abs(self.navx.getFusedHeading() - self.nextHeading) < self.tolerance:
            self.driveTrain.setTank(0, 0)
            self.turnAngle = 0
            self.next_state("idling")
            self.stop()

    def stop(self):
        self.running = False
        self.starting = False

    @feedback
    def nextHeadingDisplay(self):
        return self.navx.getFusedHeading()
