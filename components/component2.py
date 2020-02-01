import wpilib
from .component1 import Component1
import math
from magicbot import will_reset_to

"""This class runs the autonomous code from two_steps"""
class Component2():
    counter = 0
    component1: Component1
    some_motor: wpilib.Talon
    # This is changed to the value in robot.py
    SOME_CONSTANT: int

    # This gets reset after each invocation of execute()
    did_something = will_reset_to(False)

    def on_enable(self):
        """Called when the robot enters teleop or autonomous mode"""
        self.logger.info(
            "Robot is enabled: I have SOME_CONSTANT=%s", self.SOME_CONSTANT
        )
        

    def do_something(self, speed):
        self.did_something = True
        self.speed = speed


    def execute(self):
        if self.did_something:
            self.some_motor.set(self.speed)

        else:
            self.some_motor.set(0)
