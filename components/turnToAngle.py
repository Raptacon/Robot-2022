from components.driveTrain import DriveTrain
from magicbot import tunable, feedback
from wpilib import controller

import navx

class TurnToAngle():

    #PID
    P = tunable(0.01)
    I = tunable(0.01)
    D = tunable(0)
    time = 0.01
    PIDController = None

    navx = navx._navx.AHRS.create_spi()
    driveTrain: DriveTrain
    isRunning = False
    nextOutput = 0
    initialHeading = 0
    nextHeading = 0
    heading = 0
    originalHeading = 0
    turnAngle = tunable(10)
    speed = 0
    tolerance = tunable(.5)
    change = 0
    setSpeed = True

    def setup(self):
        self.heading = self.navx.getFusedHeading()
        self.originalHeading = self.navx.getFusedHeading()
        self.initialHeading = self.navx.getFusedHeading()
        self.PIDController = controller.PIDController(Kp= self.P, Ki= self.I, Kd= self.D, period = self.time)

    def setIsRunning(self):
        self.isRunning = True
        self.nextHeading = self.initialHeading + self.turnAngle
        #self.PIDController = controller.PIDController(Kp= self.P, Ki= self.I, Kd= self.D, period = self.time)

    def output(self):
        if self.isRunning == True:

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
                self.speed = .25
            elif abs(self.change) <= 90 and abs(self.change) > 20:
                self.speed = .2
            elif abs(self.change) <= 20:
                self.speed = .15

            if self.setSpeed == True:
                if self.change > 0:
                    self.driveTrain.setTank(-1 * self.speed, self.speed)
                else:
                    self.driveTrain.setTank(self.speed, -1 * self.speed)

            if (self.heading <= self.nextHeading + self.tolerance and self.heading >= self.nextHeading - self.tolerance):
                self.setSpeed = False
                self.nextOutput = self.PIDController.calculate(measurement = self.heading, setpoint = self.nextHeading)
                self.driveTrain.setTank(-1 * self.nextOutput, self.nextOutput)

    @feedback
    def outputDisplay(self):
        return self.nextOutput

    @feedback
    def nextHeadingDisplay(self):
        return self.nextHeading

    @feedback
    def setSpeedDisplay(self):
        return self.setSpeed

    @feedback
    def getIsRunning(self):
        return self.isRunning

    def stop(self):
        self.nextOutput = 0
        self.PIDController.reset()

        if self.nextHeading > 360:
            self.nextHeading -= 360

        self.isRunning = False
        self.initialHeading = self.heading
        self.setSpeed = True


    def execute(self):
        self.output()
        self.PIDController = controller.PIDController(Kp= self.P, Ki= self.I, Kd= self.D, period = self.time)
        self.heading = self.navx.getFusedHeading()
