from re import S
from magicbot import AutonomousStateMachine, state, timed_state, feedback
from components.driveTrain import DriveTrain
from components.colorSensor import ColorSensor
from components.intakeMotor import IntakeMotor
from components.hopperMotor import HopperMotor
from components.shooterMotors import ShooterMotors
from components.breakSensors import Sensors, State
import logging as log

class SmokeTest(AutonomousStateMachine):
    compatString = ["doof"]
    MODE_NAME = "Smoke Test"
    driveTrain: DriveTrain
    intakeMotor: IntakeMotor
    colorSensor: ColorSensor
    hopperMotor: HopperMotor
    shooterMotors: ShooterMotors
    breakSensors: Sensors

    #DEFAULT = True
    toDo = None

    @feedback
    def getToDo(self):
        return self.toDo

    @timed_state(first = True, time = 2)
    def drive(self):
        """Tests to see if the motors are working with an input from the driver"""
        self.toDo = "Motor should be driving forwards"
        self.driveTrain.setTank(.25, .25)

    @timed_state(time = 2)
    def runIntakeMotor(self):
        """Runs intake motor"""
        self.toDo = "The intake motor should be running"
        self.intakeMotor.intakeSpeed = .25
        self.intakeMotor.intake = True
        self.next_state("runHopperMotor")

    @timed_state(time = 2)
    def runHopperMotor(self):
        """Runs the hopper motor if there is a seperate motor for the hopper"""
        self.toDo = "The hopper motor should be running"
        self.intakeMotor.intake = False
        self.hopperMotor.hopperSpeed = .25
        self.hopperMotor.hopper = True
        self.next_state("runShooterMotor1")


    @timed_state(time = 2)
    def runShooterMotor1(self):
        self.toDo = "The upper/lower shooter motor should be running"
        self.hopperMotor.hopper = False
        self.shooterMotors.shooter = True
        self.shooterMotors.shooterSpeed1 = .25
        self.next_state("runShooterMotor2")

    @timed_state(time = 2)
    def runShooterMotor2(self):
        self.toDo = "The other shooter motor should be running"
        self.shooterMotors.shooterSpeed1 = 0
        self.shooterMotors.shooterSpeed2 = .25
        self.next_state("colorSensorCheck")
    
    @state
    def colorSensorCheck(self):
        self.toDo = "Put up a red ball to the color sensor"
        if self.colorSensor.colorMatched == "red":
            self.next_state("checkIntakeSensor")
        elif self.colorSensor.colorMatched == "blue":
            log.error("The ball is not red idiot")
            self.next_state("colorSensorCheck")
        else:
            log.error("There is no ball")
            self.next_state("colorSensorCheck")

    @state
    def checkIntakeSensor(self):
        """Checks to see if the intake break sensor is broken"""
        self.toDo = "Break the break sensor on the intake"
        if self.breakSensors.loadingSensor(State.kTripped):
            self.next_state("checkShooterSensor")
        else:
            log.error("Sensor not broken")
            self.next_state("checkIntakeSensor")

    @state
    def checkHopperSensor(self):
        """Checks to see if the hopper break sensor is broken"""
        pass

    @state
    def checkShooterSensor(self):
        """Checks to see if the shooter break sensor is broken"""
        self.toDo = "Break the break sensor on the shooter"
        if self.breakSensors.shootingSensor(State.kTripped):
            log.error("Done")
            self.done()
        else:
            self.next_state("checkShooterSensor")
