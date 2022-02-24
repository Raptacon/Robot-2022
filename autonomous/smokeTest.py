from magicbot import AutonomousStateMachine, state, feedback, timed_state
from components.Actuators.LowLevel.driveTrain import DriveTrain
from components.Input.colorSensor import ColorSensor
from components.Actuators.LowLevel.intakeMotor import IntakeMotor
from components.Actuators.LowLevel.hopperMotor import HopperMotor
from components.Actuators.LowLevel.shooterMotors import ShooterMotors
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from components.Actuators.AutonomousControl.turretTurn import TurretTurn
from components.Actuators.HighLevel.turretCalibrate import CalibrateTurret
from components.Input.breakSensors import Sensors, State
from components.Input.navx import Navx
from components.Actuators.AutonomousControl.turnToAngle import TurnToAngle
import logging as log

from utils.DirectionEnums import Direction

class SmokeTest(AutonomousStateMachine):
    compatString = ["teapot"]
    MODE_NAME = "Smoke Test"
    DEFAULT = False
    driveTrain: DriveTrain
    intakeMotor: IntakeMotor
    colorSensor: ColorSensor
    hopperMotor: HopperMotor
    shooterMotors: ShooterMotors
    turretCalibrate: CalibrateTurret
    turretThreshold: TurretThreshold
    turretTurn: TurretTurn
    sensors: Sensors
    navx: Navx
    turnToAngle: TurnToAngle
    dumbSpeed = .25
    dumbRPMs = 3000
    time = 2
    toDo = None

    @feedback
    def getToDo(self):
        return self.toDo

    @state(first=True)
    def driveSetup(self):
        self.driveTrain.setup()
        self.driveTrain.resetDistTraveled()
        self.next_state("drive")

    @state
    def drive(self):
        """Tests to see if the motors are working with an input from the driver"""
        self.toDo = "Drives robot forwards until it reaches a certain distance"
        self.driveTrain.setTank(-self.dumbSpeed, -self.dumbSpeed)
        if int(self.driveTrain.getEstTotalDistTraveled()) >= 100 and int(self.driveTrain.getEstTotalDistTraveled()) <=115:
            self.driveTrain.setTank(0, 0)
            log.error("Drove forwards about 100 inches")
            self.next_state("runIntakeMotor")
        else:
            log.error("Driving")
            self.next_state("drive")

    @state
    def delpoyIntake(self):
        """Deploys the intake"""
        self.toDo = "Check to see if intake is deployed"
        pass

    @timed_state(duration = time, next_state = "runShooterMotors")
    def runIntakeMotor(self):
        """Runs the intake motor for 2 seconds"""
        self.toDo = "Check to see if the intake motor is running"
        self.intakeMotor.runIntake(iSpeed = self.dumbSpeed, direction = Direction.kForwards)
        log.error("Running intake motor")

    @timed_state(duration = time, next_state = "runHopperMotor2")
    def runHopperMotor1(self):
        """Runs the first hopper motor for 2 seconds"""
        self.toDo = "Check to see if the front hopper motor is running"
        self.intakeMotor.stopIntake()
        #self.hopperMotor.runHopperMotor1(lSpeed = self.dumbSpeed, direction = Direction.kForwards)
        log.error("Running hopper motor 1")
        pass

    @timed_state(duration = time, next_state = "runShooterMotors")
    def runHopperMotor2(self):
        """Stops the first hopper motor adn runs the second motor for 2 seconds"""
        self.toDo = "Check to see if the back hopper motor is running"
        #self.hopperMotor.stopHopperMotor1()
        #self.hopperMotor.runHopperMotor2(lSpeed = self.dumbSpeed, direction = Direction.kForwards)
        log.error("Running hopper motor 2")
        pass

    @timed_state(duration = time, next_state = "calibrateTurret")
    def runShooterMotors(self):
        """Stops the second hopper motor and runs both shooter motors for 2 seconds"""
        self.toDo = "Check to see if the shooter motors are running"
        #self.hopperMotor.stopHopperMotor2
        self.intakeMotor.stopIntake()
        self.shooterMotors.runShooter(sSpeed1 = self.dumbRPMs, sSpeed2 = self.dumbRPMs)
        self.shooterMotors.execute()
        log.error("Running both shooter motors")

    @state
    def calibrateTurret(self):
        """Calibrates the turret's deadzones and checks to see if the turret motor is working"""
        self.toDo = "Check to see if the turret is moving and that the deadzones are calibrated"
        self.shooterMotors.stopShooter()
        self.turretCalibrate.engage()
        self.turretTurn.engage()
        self.turretThreshold.execute()
        self.next_state("calibrateTurret")
        if self.turretThreshold.calibrated == True:
            self.next_state("colorSensorCheck")

    @state
    def colorSensorCheck(self):
        """Has the user put up a red ball to the color sensor. Will not move on until the ball is red."""
        self.toDo = "Put up a red ball to the color sensor"
        self.colorSensor.execute()
        if self.colorSensor.colorMatched == "red":
            log.error("The ball is red")
            self.next_state("checkIntakeSensor")
        elif self.colorSensor.colorMatched == "blue":
            log.error("The ball is not red")
            self.next_state("colorSensorCheck")
        else:
            log.error("There is no ball")
            self.next_state("colorSensorCheck")

    @state
    def checkNavx(self):
        """Has user turn the robot until it gets to a certain angle. Once angle is reached, it moves to the next state. This state uses turnToAngle"""
        self.toDo = "Turn the bot to the right about 45 degrees"
        self.turnToAngle.setAngle(angle = 45)
        if self.turnToAngle.running:
            log.error("Keep turning")
        else:
            log.error("Done turning")
            self.next_state = "checkIntakeSensor"

    @state
    def checkIntakeSensor(self):
        """Checks to see if the intake break sensor is broken"""
        self.toDo = "Break the break sensor on the intake"
        if self.sensors.loadingSensor(State.kTripped):
            log.error("Tripped")
            self.next_state("checkHopperSensor")
        else:
            log.error("Intake sensor not broken")
            self.next_state("checkIntakeSensor")

    @state
    def checkHopperSensor(self):
        """Checks to see if the hopper break sensor is broken"""
        self.toDo = "Break the break sensor on the hopper"
        if self.sensors.hopperSensor(State.kTripped):
            log.error("Tripped")
            self.next_state("checkShooterSensor")
        else:
            log.error("Hopper sensor not broken")
            self.next_state("checkHopperSensor")

    @state
    def checkShooterSensor(self):
        """Checks to see if the shooter break sensor is broken"""
        self.toDo = "Break the break sensor on the shooter"
        if self.sensors.shootingSensor(State.kTripped):
            log.error("Tripped")
            log.error("Done")
            self.done()
        else:
            log.error("Shooting sensor not broken")
            self.next_state("checkShooterSensor")
