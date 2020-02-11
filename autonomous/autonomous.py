from magicbot import AutonomousStateMachine, tunable, timed_state
import math
from components.driveTrain import DriveTrain


class autonomous(AutonomousStateMachine):
    """Creates the autonomous code"""
    """DO NOT USE IN PRODUCTION THIS WILL BE DELETED """
    time = 15
    MODE_NAME = "Two Steps"
    DEFAULT = True
    driveTrain: DriveTrain

    drive_speed = tunable(-1)
    def on_enable(self):
        print("Enabled")
        self.engage()
        
    def engage(self):
        print("Engaged")

    @timed_state(duration=2, next_state="do_something", first=True)
    def dont_do_something(self):
        """This happens first"""
        self.driveTrain.setTank(0, 0)

    @timed_state(duration=time)
    def do_something(self, state_tm):
        """This happens second"""
        
        speed = math.sin(2 * math.pi * (1 / self.time) * state_tm)
        """First integer is # of times to run through program, second is time. combined creates value."""
        print('{}  {}'.format(state_tm, speed))
        self.driveTrain.setTank(speed, speed)
