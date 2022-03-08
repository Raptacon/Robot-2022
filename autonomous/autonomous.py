from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.Input.ballCounter import BallCounter
from components.Actuators.LowLevel.driveTrain import DriveTrain
from components.Actuators.LowLevel.intakeMotor import IntakeMotor, Direction
from components.Actuators.HighLevel.shooterLogic import ShooterLogic
from components.Actuators.LowLevel.pneumatics import Pneumatics
from components.Actuators.LowLevel.driveTrain import DriveTrain
from components.Actuators.AutonomousControl.turnToAngle import TurnToAngle
from components.Actuators.AutonomousControl.turretTurn import TurretTurn
from components.Actuators.AutonomousControl.driveTrainGoToDist import GoToDist
from components.Actuators.HighLevel.turretCalibrate import CalibrateTurret, TurretThreshold

import logging as log

class Autonomous(AutonomousStateMachine):
    """Creates the autonomous code"""
    time = 1.4
    shootTime = 4
    DEFAULT = True
    MODE_NAME = "Big Brain Autonomous"
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
    drive_speed = tunable(.25)

    allianceColor: str

    afterShootState = "calibrateTurret_move"

    moveComplete = False
    currentMove = 0
    robotPosition = tunable(2)
    turnToAnglePrevRunning = False
    goToDistPrevRunning = False

    # In degrees and feet
    # Positions are left to right 1,2,3 for the spots with balls

    moveSequences = [[["drive", -24],
                    ["turn", 180]],

                    [["turn", 59.993],
                    ["drive", 5.62733*12]],

                    [["turn", -59.993],
                    ["drive", 5.62733*12]]]

    @state(first=True)
    def init(self):
        self.assessPosition()
        self.next_state("calibrateTurret_move")

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
        self.pneumatics.deployLoader()
        self.shooter.engage()
        self.shooter.startShooting()
        self.next_state('shooter_wait')

    @timed_state(duration = shootTime, next_state=afterShootState)
    def shooter_wait(self):
        """Waits for shooter to finish, then next state"""
        pass

    @state(first = True)
    def calibrateTurret_move(self):
        """
        Calibrates the turret's deadzones
        while moving
        """
        self.assessPosition()
        self.shooter.shooterMotors.stopShooter()
        self.driveTrain.setBraking(True)
        if not self.moveComplete:
            move = self.moveSequence[self.currentMove]
            if move[0] == "turn":
                if not self.turnToAngle.running:
                    self.turnToAngle.setRelAngle(move[1])
                log.error("Turing")
                self.turnToAngle.engage()
                if (not self.turnToAngle.running) and self.turnToAnglePrevRunning:
                    log.error("Moving to drive")
                    self.currentMove += 1
            elif move[0] == "drive":
                if (((not self.goToDist.running) and self.goToDistPrevRunning)
                or self.ballCounter.getBallCount()[0] != None):
                    log.error("Finishing")
                    self.currentMove += 1
                else:
                    self.goToDist.setTargetDist(move[1])
                    self.goToDist.engage()

            if self.currentMove == len(self.moveSequence):
                self.moveComplete = True

        self.turnToAnglePrevRunning = self.turnToAngle.running
        self.goToDistPrevRunning = self.goToDist.running

    @state
    def calibrateTurret(self):
        """Calibrates the turret's deadzones and checks to see if the turret motor is working"""
        self.toDo = "Check to see if the turret is moving and that the deadzones are calibrated"
        self.turretCalibrate.setUseMotor(True)
        self.turretCalibrate.engage()
        self.next_state("calibrateTurret_move")
        if self.turretThreshold.calibrated == True:
            self.turretTurn.done()
            self.turretThreshold.setTurretspeed(0)

        if self.turretThreshold.calibrated == True and self.moveComplete:
            self.next_state("finishCalibration")

    @state
    def finishCalibration(self):
        self.turretThreshold.setTurretspeed(0)
        self.next_state("engage_shooter")

    @state
    def engage_Shooter2(self):
        ball1 = self.ballCounter.getBallCount()[0]
        self.afterShootState = "stop"

        # We don't need the second condition, but it sounds fun
        if ball1 != None and ball1.getColor() == self.allianceColor:
            self.shooter.engage()
            self.shooter.startShooting()
            self.next_state('shooter_wait')
        elif ball1 != None and ball1.getColor() != self.allianceColor:
            self.shooter.autoShootingSpeed1 = 1000
            self.shooter.autoShootingSpeed2 = 500
            self.shooter.engage()
            self.shooter.startShooting()
            self.next_state('shooter_wait')
        else:
            self.next_state("stop")


    @state(must_finish = True)
    def stop(self):
        """Stops driving bot"""
        self.driveTrain.setTank(0, 0)
        self.turnToAngle.done()
        self.goToDist.done()
        self.turretTurn.done()
        self.done()
