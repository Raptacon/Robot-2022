from components.driveTrain import DriveTrain
from magicbot import tunable, feedback, StateMachine, state
import logging as log
from wpilib import controller

import navx

class TurnToAngle(StateMachine):
    compatString = ["doof", "greenChassis"]

    navx = navx._navx.AHRS.create_spi()
    driveTrain: DriveTrain
    starting = False
    running = False
    nextOutput = 0
    initialHeading = 0
    nextHeading = 0
    heading = 0
    originalHeading = 0
    turnAngle = 20
    dumbSpeed = .5
    farMultiplier = tunable(.5)
    midMultiplier = tunable(.4)
    closeMultiplier = tunable(.25)
    tolerance = tunable(.5)
    change = 0
    setSpeed = True

    def setup(self):
        self.heading = self.navx.getFusedHeading()
        self.originalHeading = self.navx.getFusedHeading()
        self.initialHeading = self.navx.getFusedHeading()
    """
    def setAngle(self, angle):
        Sets the desired turn angle
        self.turnAngle = angle
    """
    def start(self):
        self.starting = True
        self.next_state("idling")

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
        self.next_state("turn")

    @state
    def turn(self):
        if self.running == True:
            if self.nextHeading > 360:
                self.nextHeading -= 360
            elif self.nextHeading < 0:
                self.nextHeading += 360


            self.change = self.nextHeading - self.heading
            if self.change > 180:
                self.change -= 360
            elif self.change < -180:
                self.change += 360

            if abs(self.change) > 90:
                self.speed = self.dumbSpeed * self.farMultiplier
            elif abs(self.change) <= 90 and abs(self.change) > 20:
                self.speed = self.dumbSpeed * self.midMultiplier
            elif abs(self.change) <= 20:
                self.speed = self.dumbSpeed * self.closeMultiplier

            if self.setSpeed == True:
                if self.change > 0:
                    self.driveTrain.setTank(-1 * self.speed, self.speed)
                else:
                    self.driveTrain.setTank(self.speed, -1 * self.speed)

            if (self.heading <= self.nextHeading + self.tolerance and self.heading >= self.nextHeading - self.tolerance):
                self.setSpeed = False
                self.nextOutput = self.PIDController.calculate(measurement = self.heading, setpoint = self.nextHeading)
                self.driveTrain.setTank(-1 * self.nextOutput, self.nextOutput)
                self.stop()
                self.next_state("idling")

    def stop(self):
        self.nextOutput = 0
        self.running = False
        self.starting = False
        self.initialHeading = self.heading
        self.setSpeed = True


    @feedback
    def outputDisplay(self):
        return self.nextOutput

    @feedback
    def nextHeadingDisplay(self):
        return self.nextHeading

    @feedback
    def setSpeedDisplay(self):
        return self.setSpeed

    def execute(self):
        self.heading = self.navx.getFusedHeading()
