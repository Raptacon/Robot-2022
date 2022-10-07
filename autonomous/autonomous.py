from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.Input.ballCounter import BallCounter
from components.Actuators.LowLevel.driveTrain import DriveTrain
from components.Actuators.LowLevel.intakeMotor import IntakeMotor
from components.Actuators.LowLevel.limelight import Limelight
from components.Actuators.HighLevel.shooterLogic import ShooterLogic
from components.Actuators.HighLevel.loaderLogic import LoaderLogic
from components.Actuators.HighLevel.driveTrainHandler import DriveTrainHandler, ControlMode
from components.Actuators.HighLevel.turretScan import TurretScan
from components.Actuators.LowLevel.pneumatics import Pneumatics
from components.Actuators.AutonomousControl.turnToAngle import TurnToAngle
from components.Actuators.AutonomousControl.turretTurn import TurretTurn
from components.Actuators.AutonomousControl.driveTrainGoToDist import GoToDist
from components.Actuators.HighLevel.turretCalibrate import CalibrateTurret, TurretThreshold
from components.Actuators.LowLevel.winch import Winch
from utils.DirectionEnums import Direction

import logging as log

class Autonomous(AutonomousStateMachine):
    """Creates the autonomous code"""
    shootTime = 4
    DEFAULT = True
    MODE_NAME = "Big Brain Autonomous"
    turretScan: TurretScan
    driveTrain: DriveTrain
    goToDist: GoToDist
    shooter: ShooterLogic
    pneumatics: Pneumatics
    driveTrain: DriveTrain
    turnToAngle: TurnToAngle
    turretCalibrate: CalibrateTurret
    turretTurn: TurretTurn
    turretThreshold: TurretThreshold
    ballCounter: BallCounter
    intakeMotor: IntakeMotor
    loader: LoaderLogic
    winch:Winch
    limelight: Limelight
    driveTrainHandler: DriveTrainHandler
    drive_speed = tunable(.1)

    allianceColor: str

    afterShootState = "moveBack"

    moveComplete = False
    currentMove = 0
    robotPosition = tunable(1)
    turnToAnglePrevRunning = False
    goToDistPrevRunning = False
    turretTurnPrev = True

    # In degrees and feet
    # Positions are left to right 1,2,3 for the spots with balls

    moveSequences = [[["drive", 46],
                    ["turn", 180]],

                    [["turn", 59.993],
                    ["drive", 5.62733*12]],

                    [["turn", -59.993],
                    ["drive", 5.62733*12]]]

    @state(first=True)
    def init(self):
        self.ballCounter.addBall(2, self.allianceColor.lower())
        self.loader.setIsAutonomous(True)
        self.shooter.autonomousEnabled()
        self.driveTrain.resetDistTraveled()
        self.pneumatics.deployLoader()
        self.assessPosition()
        self.next_state("winchUp")

    @timed_state(duration=.1, next_state="calibrateTurret_move")
    def winchUp(self):
        self.winch.setLower()

    def assessPosition(self):
        """
        Pick a movement sequence based on the tunable robotPosition.
        If it has not been changed, do the default sequence. If it has,
        pick the correct set of movements
        """
        self.moveSequence = []
        if int(self.robotPosition) == 0:
            log.error("You forgot to choose")
            self.moveSequence = [["turn", 90]]
        else:
            self.moveSequence = self.moveSequences[int(self.robotPosition) - 1]

    @state
    def engage_shooter(self):
        """Starts shooter and fires"""
        self.shooter.engage()
        self.shooter.startShooting()
        self.next_state('shooter_wait')

    @timed_state(duration = shootTime, next_state= "engage_Shooter2")
    def shooter_wait(self):
        """Waits for shooter to finish, then next state"""
        pass

    @state
    def calibrateTurret_move(self):
        """
        Calibrates the turret's deadzones
        while moving
        """
        self.winch.stop()
        self.assessPosition()
        self.shooter.shooterMotors.stopShooter()
        self.driveTrain.setBraking(True)
        if not self.moveComplete:
            move = self.moveSequence[self.currentMove]
            if move[0] == "turn":
                self.intakeMotor.runIntake(0, Direction.kForwards)
                log.error("Turning")
                if (not self.turnToAngle.running) and self.turnToAnglePrevRunning:
                    log.error("Moving to drive")
                    self.currentMove += 1
                elif not self.turnToAngle.running:
                    self.turnToAngle.setRelAngle(move[1])
                self.turnToAngle.engage()
            elif move[0] == "drive":
                if not self.goToDist.running:
                    self.goToDist.setTargetDist(move[1])
                if (((not self.goToDist.running) and self.goToDistPrevRunning)
                or self.ballCounter.getBallCount()[0] != None):
                    log.error("Finishing")
                    self.currentMove += 1
                self.intakeMotor.runIntake(.4, Direction.kForwards)
                self.intakeMotor.execute()
                self.goToDist.engage()

            if self.currentMove == len(self.moveSequence):
                self.moveComplete = True

        self.turnToAnglePrevRunning = self.turnToAngle.running
        self.goToDistPrevRunning = self.goToDist.running

        self.turretCalibrate.setUseMotor(True)
        self.turretCalibrate.engage()
        self.next_state("calibrateTurret_move")
        if self.turretThreshold.calibrated == True:
            self.turretTurn.done()
            self.turretThreshold.setTurretspeed(0)

        if self.turretThreshold.calibrated == True and self.moveComplete:
            self.next_state("finishCalibration")

    @state
    def turn_turret_rough(self):
        self.turretTurn.setEncoderControl()
        self.turretTurn.setAngle(self.turretThreshold.rightLim - 103)
        self.turretTurn.engage()
        self.next_state("turn_turret_rough")
        if self.turretTurn.withinTolerance() and not self.turretTurnPrev:
            self.next_state("turn_turret_smart")
        self.turretTurnPrev = self.turretTurn.withinTolerance()

    @state
    def turn_turret_smart(self):
        '''
        self.limelight.LEDOn()
        self.turretTurn.setLimeLightControl()
        self.turretTurn.engage()
        self.next_state("turn_turret_smart")
        if self.turretScan.hasTarget() and self.turretTurn.withinTolerance():
            self.next_state("engage_shooter")
        elif not self.turretScan.hasTarget():
            self.turretScan.engage()
        '''
        self.next_state("engage_Shooter2")

    @state
    def finishCalibration(self):
        self.turretThreshold.setTurretspeed(0)
        self.next_state("turn_turret_rough")

    @state
    def engage_Shooter2(self):
        '''Shoots the  ball'''
        ball1 = self.ballCounter.getBallCount()[0]
        self.afterShootState = "stop"

        if ball1 != None:
            self.shooter.engage()
            self.shooter.startShooting()
            self.next_state('shooter_wait')
        elif ball1 != None:
            self.shooter.autoShootingSpeed1 = 1000
            self.shooter.autoShootingSpeed2 = 500
            self.shooter.engage()
            self.shooter.startShooting()
            self.next_state('shooter_wait')
        else:
            self.next_state("moveBack")


    @timed_state(duration=3, next_state="stop")
    def moveBack(self):
        self.driveTrainHandler.setDriveTrain(self, ControlMode.kTankDrive, self.drive_speed, self.drive_speed)

    @state(must_finish = True)
    def stop(self):
        """Stops driving bot"""
        self.driveTrain.setTank(0, 0)
        self.turnToAngle.done()
        self.goToDist.done()
        self.turretTurn.done()
        self.done()