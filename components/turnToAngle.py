from components.driveTrain import DriveTrain
from magicbot import tunable, feedback, StateMachine, state
import logging as log

import navx

class TurnToAngle(StateMachine):
    compatString = ["doof", "greenChassis"]

    navx = navx._navx.AHRS.create_spi()
    driveTrain: DriveTrain
    starting = False
    running = False
    initialHeading = 0
    nextHeading = 0
    heading = 0
    originalHeading = 0
    turnAngle = 0
    dumbSpeed = .25
    farMultiplier = tunable(1)
    midMultiplier = tunable(.75)
    closeMultiplier = tunable(.5)
    tolerance = tunable(.5)
    change = 0

    def setup(self):
        self.originalHeading = self.navx.getFusedHeading()
        self.initialHeading = self.navx.getFusedHeading()

    def setAngle(self, angle):
        """Sets the desired turn angle"""
        self.turnAngle = angle

    def start(self):
        self.starting = True

    @state(first = True)
    def idling(self):
        """Stays in this state until started"""
        if self.turnAngle != 0:
            self.next_state("turn")
        else:
            log.error("Must have an angle to turn to")
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
        elif abs(self.change) <= 20:
            self.speed = self.dumbSpeed * self.closeMultiplier

    @state
    def turn(self):
        """Turns the robot based off of the speed determined in setSpeedFunc"""
        self.setSpeedFunc()
        if self.change > 0:
            self.driveTrain.setTank(-1 * self.speed, self.speed)
        else:
            self.driveTrain.setTank(self.speed, -1 * self.speed)
        self.next_state("turn")

        """Stops the automatic turning if the bot is within the tolerance of the desired angle"""
        if self.navx.getFusedHeading() <= self.nextHeading + self.tolerance and self.navx.getFusedHeading() >= self.nextHeading - self.tolerance:
            self.driveTrain.setTank(0, 0)
            self.stop()

    def stop(self):
        self.running = False
        self.starting = False
        self.initialHeading = self.navx.getFusedHeading()
        self.done()

    @feedback
    def nextHeadingDisplay(self):
        return self.navx.getFusedHeading()
