from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.driveTrain import DriveTrain
from components.shooterLogic import ShooterLogic

class autonomous(AutonomousStateMachine):
    """Creates the autonomous code"""
    time = 1.4
    MODE_NAME = "Basic Autonomous"
    DEFAULT = True
    driveTrain: DriveTrain
    shooter: ShooterLogic
    drive_speed = tunable(.25)

    @state(first = True)
    def engage_shooter(self):
        """Starts shooter and fires"""
        self.shooter.shootBalls()
        print("engaged")
        self.next_state("shooter_wait")

    @state
    def shooter_wait(self, state_tm):
        """Waits for shooter to finish, then next state"""
        if state_tm > 4:
            self.next_state_now("drive_backwards")

    @timed_state(duration = time, next_state = "turn")
    def drive_backwards(self):
        """Drives the bot backwards for a time"""
        self.driveTrain.setTank(self.drive_speed, self.drive_speed)

    @timed_state(duration = time, next_state = "stop")
    def turn(self):
        """Turns for a time"""
        self.driveTrain.setTank(-self.drive_speed, self.drive_speed)

    @state(must_finish = True)
    def stop(self):
        """Stops driving bot"""
        self.driveTrain.setTank(0, 0)
