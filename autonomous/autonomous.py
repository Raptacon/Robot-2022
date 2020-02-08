from magicbot import AutonomousStateMachine, tunable, timed_state
import math
from components.driveTrain import DriveTrain


class autonomous(AutonomousStateMachine):
    """Creates the autonomous code"""
    time = 5
    MODE_NAME = "Two Steps"
    DEFAULT = True
    driveTrain: DriveTrain

    drive_speed = tunable(-1)

    @timed_state(duration=2, next_state="do_something", first=True)
    def dont_do_something(self):
        """This happens first"""
        pass

    @timed_state(duration=time)
    def do_something(self, state_tm):
        """This happens second"""
        
        speed = math.sin(2 * math.pi * (1 / self.time) * state_tm)
        """First integer is # of times to run through program, second is time. combined creates value."""
        print('{}  {}'.format(state_tm, speed))
        self.driveTrain.setTank(speed, speed)
