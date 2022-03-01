from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.Actuators.LowLevel.driveTrain import DriveTrain
from components.Actuators.HighLevel.shooterLogic import ShooterLogic
from components.Actuators.LowLevel.pneumatics import Pneumatics
from components.Actuators.AutonomousControl.turnToAngle import TurnToAngle
from components.Actuators.AutonomousControl.turretTurn import TurretTurn
from components.Actuators.HighLevel.turretCalibrate import CalibrateTurret, TurretThreshold

class Autonomous(AutonomousStateMachine):
    """Creates the autonomous code"""
    time = 1.4
    shootTime = 4
    DEFAULT = True
    MODE_NAME = "Basic Autonomous"
    driveTrain: DriveTrain
    shooter: ShooterLogic
    pneumatics: Pneumatics
    turnToAngle: TurnToAngle
    turretCalibrate: CalibrateTurret
    turretTurn: TurretTurn
    turretThreshold: TurretThreshold
    drive_speed = tunable(.25)

    @state(first = True)
    def engage_shooter(self):
        """Starts shooter and fires"""
        self.pneumatics.deployLoader()
        self.shooter.engage()
        self.shooter.startShooting()
        self.next_state('shooter_wait')

    @timed_state(duration = shootTime, next_state="calibrateTurret")
    def shooter_wait(self):
        """Waits for shooter to finish, then next state"""
        pass

    @state
    def turn(self):
        self.turnToAngle.setAngle(angle = -90)
        self.turnToAngle.engage()
        self.firstCall = True
        self.next_state("turnWait")

    @state
    def turnWait(self):
        self.turnToAngle.engage()
        if self.firstCall:
            self.firstCall = False
            self.next_state('turnWait')
        elif self.turnToAngle.running:
            self.next_state('turnWait')
        else:
            self.next_state("calibrateTurret")

    @state
    def calibrateTurret(self):
        """Calibrates the turret's deadzones and checks to see if the turret motor is working"""
        self.toDo = "Check to see if the turret is moving and that the deadzones are calibrated"
        self.turretCalibrate.engage()
        self.next_state("calibrateTurret")
        if self.turretThreshold.calibrated == True:
            self.turretTurn.done()
            self.turretThreshold.setTurretspeed(0)
            self.next_state("finishCalibration")

    @state
    def finishCalibration(self):
        self.turretThreshold.setTurretspeed(0)
        self.next_state("stop")

    @timed_state(duration = time, next_state = 'stop')
    def drive(self):
        """Drives the bot backwards for a time"""
        self.shooter.doneShooting()
        self.driveTrain.setTank(self.drive_speed, self.drive_speed)

    @state(must_finish = True)
    def stop(self):
        """Stops driving bot"""
        self.driveTrain.setTank(0, 0)
        self.done()
