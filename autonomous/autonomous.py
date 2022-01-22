from magicbot import AutonomousStateMachine, tunable, timed_state, state
import logging as log
from components.driveTrain import DriveTrain
from components.driveTrainGoToDist import GoToDist
from components.turnToAngle import TurnToAngle
from components.shooterLogic import ShooterLogic
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
    MODE_NAME = "Hallway Autonomous"
    DEFAULT = False
    driveTrain: DriveTrain
    shooter: ShooterLogic
    goToDist: GoToDist
    turnToAngle: TurnToAngle
    pneumatics: Pneumatics
    autoAlign: AutoAlign
    autoShoot: AutoShoot
    shooter: ShooterLogic
    drive_speed = tunable(.25)
    StopRunningFirstCall = True
    CheckAngleFirstCall = True
    TurnsCompleted = 0

    @state(first = True)
    def drive_forwards(self):
        """Drives the bot forwards for 5 feet"""
        self.driveTrain.setup()
        self.driveTrain.resetDistTraveled()
        self.goToDist.engage()
        self.goToDist.setTargetDist(-60)
        self.goToDist.start()
        self.driveTrain.execute()
        self.next_state("stoprunning")

    @state
    def stoprunning(self):
        self.goToDist.engage()
        self.driveTrain.execute()
        if self.StopRunningFirstCall:
            self.StopRunningFirstCall = not self.StopRunningFirstCall
            self.next_state("stoprunning")
        elif self.goToDist.running:
            self.next_state("stoprunning")
        else:
            self.next_state("turn")


    @state
    def turn(self):
        """One method that completes all turns"""
        turn1 = -90
        turn2 = 180
        turn3 = -90
        self.turnToAngle.engage()
        self.CheckAngleFirstCall = True
        if self.TurnsCompleted == 0:
            log.info("States first turn")
            self.turnToAngle.setAngle(turn1)
            self.next_state("check_angle")
        elif self.TurnsCompleted == 1:
            log.info("States Sencond turn")
            self.turnToAngle.setAngle(turn2)
            self.next_state("check_angle")
        elif self.TurnsCompleted == 2:
            self.turnToAngle.setAngle(turn3)
            self.next_state("check_angle")

    @state
    def check_angle(self):
        self.turnToAngle.engage()
        self.driveTrain.execute()
        #self.turnToAngle.stop()
        if self.CheckAngleFirstCall:
            self.CheckAngleFirstCall = False
            self.next_state("check_angle")
        elif self.turnToAngle.running:
            self.next_state("check_angle")
        else:
            self.TurnsCompleted += 1
            self.next_state("turn")
            if self.TurnsCompleted >= 3:
                self.next_state("drive_backwards")




    @state
    def drive_backwards(self):
        """Drives the bot backwards for 5 feet"""
        self.goToDist.engage()
        self.goToDist.setTargetDist(60)
        self.goToDist.start()
        self.StopRunningFirstCall = True
        self.next_state("stoprunning2")

    @state
    def stoprunning2(self):
        self.goToDist.engage()
        self.driveTrain.execute()
        if self.StopRunningFirstCall:
            self.StopRunningFirstCall = not self.StopRunningFirstCall
            self.next_state("stoprunning2")
        elif self.goToDist.running:
            self.next_state("stoprunning2")
        else:
            self.next_state("stop")

    @state(must_finish = True)
    def stop(self):
        """Stops driving bot"""
        self.driveTrain.setArcade(0, 0)
        self.done()


