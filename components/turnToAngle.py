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
    turnAngle = 20
    dumbSpeed = .25
    """
    farMultiplier = tunable(.5)
    midMultiplier = tunable(.4)
    closeMultiplier = tunable(.25)
    """
    tolerance = tunable(.5)
    change = 0
    setSpeed = True

    def setup(self):
        self.originalHeading = self.navx.getFusedHeading()
        self.initialHeading = self.navx.getFusedHeading()
    """
    def setAngle(self, angle):
        Sets the desired turn angle
        self.turnAngle = angle
    """
    def start(self):
        self.starting = True

    @state(first = True)
    def idling(self):
        if self.starting and not self.running:
            if self.turnAngle != 0:
                self.next_state("calcHeading")
            else:
                log.error("Must have an angle to turn to")
                self.next_state("idling")
        else:
            self.next_state("idling")


    @state
    def calcHeading(self):
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
        self.next_state_now("setSpeedFunc")

    @state
    def setSpeedFunc(self):
        if abs(self.change) > 90:
            self.speed = self.dumbSpeed
        elif abs(self.change) <= 90 and abs(self.change) > 20:
            self.speed = self.dumbSpeed
        elif abs(self.change) <= 20:
            self.speed = self.dumbSpeed
        self.next_state("turn")

    @state
    def turn(self):
        if self.setSpeed == True:
            if self.change > 0:
                self.driveTrain.setTank(-1 * self.speed, self.speed)
            else:
                self.driveTrain.setTank(self.speed, -1 * self.speed)

        if (self.heading <= self.nextHeading + self.tolerance and self.heading >= self.nextHeading - self.tolerance):
            self.setSpeed = False
            self.driveTrain.setTank(0, 0)
            self.stop()
        else:
            self.next_state("calcHeading")


    def stop(self):
        self.running = False
        self.starting = False
        self.initialHeading = self.navx.getFusedHeading()
        self.setSpeed = True
        self.done()

    @feedback
    def nextHeadingDisplay(self):
        return self.navx.getFusedHeading()

    # def execute(self):
    #     self.heading = self.navx.getFusedHeading()
