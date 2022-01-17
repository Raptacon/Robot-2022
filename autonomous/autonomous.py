from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.driveTrain import DriveTrain
from components.driveTrainGoToDist import GoToDist
from components.shooterLogic import ShooterLogic
from components.shooterMotors import ShooterMotorCreation
from components.autoAlign import AutoAlign
from components.autoShoot import AutoShoot
from components.pneumatics import Pneumatics

class Autonomous(AutonomousStateMachine):
    """Creates the autonomous code"""
    time = 1.4
    shootTime = 4
    MODE_NAME = "Basic Autonomous"
    DEFAULT = True
    driveTrain: DriveTrain
    shooter: ShooterLogic
    shooterMotors: ShooterMotorCreation
    pneumatics: Pneumatics
    drive_speed = tunable(.25)

    @state(first = True)
    def engage_shooter(self):
        """Starts shooter and fires"""
        self.pneumatics.deployLoader()
        self.shooter.engage()
        self.shooter.startShooting()
        self.next_state('shooter_wait')

    @timed_state(duration = shootTime, next_state="drive_backwards")
    def shooter_wait(self):
        """Waits for shooter to finish, then next state"""
        pass

    @timed_state(duration = time, next_state = 'turn')
    def drive_backwards(self):
        """Drives the bot backwards for a time"""
        self.shooter.doneShooting()
        self.driveTrain.setTank(self.drive_speed, self.drive_speed)

    @timed_state(duration = time, next_state = 'stop')
    def turn(self):
        """Turns for a time"""
        self.driveTrain.setTank(-self.drive_speed, self.drive_speed)

    @state(must_finish = True)
    def stop(self):
        """Stops driving bot"""
        self.driveTrain.setTank(0, 0)
        self.done()

class AutonomousAutoShoot(AutonomousStateMachine):
    """Creates the autonomous code"""
    time = 1.4
    MODE_NAME = "AutoShoot Autonomous"
    DEFAULT = False
    driveTrain: DriveTrain
    shooter: ShooterLogic
    shooterMotors: ShooterMotorCreation
    pneumatics: Pneumatics
    autoAlign: AutoAlign
    autoShoot: AutoShoot
    shooter: ShooterLogic
    drive_speed = tunable(.25)

    @state(first = True)
    def engage_shooter(self):
        """Starts shooter and fires"""
        self.autoAlign.setShootAfterComplete(True)
        self.autoAlign.engage()
        self.autoShoot.engage()
        self.shooter.engage()
        self.next_state("engage_shooter")




class AutonomousAutoStart(AutonomousStateMachine):
    """Creates the autonomous code"""
    time = 1.4
    MODE_NAME = "AutoShoot Autonomous"
    DEFAULT = False
    driveTrain: DriveTrain
    shooter: ShooterLogic
    shooterMotors: ShooterMotorCreation
    pneumatics: Pneumatics
    autoAlign: AutoAlign
    autoShoot: AutoShoot
    shooter: ShooterLogic
    drive_speed = tunable(.25)


    @state(first = true)