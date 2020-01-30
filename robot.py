#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot
from team3200 import robotMap

from components.component1 import Component1
from components.component2 import Component2


class MyRobot(MagicRobot):

    #
    # Define components here
    #

    component1: Component1
    component2: Component2

    # You can even pass constants to components
    SOME_CONSTANT = 1

    def createObjects(self):
        """Initialize all wpilib motors & sensors"""

        # TODO: create button example here
        self.robotMap = robotMap.RobotMap()
        self.component1_motor = wpilib.Talon(1)
        self.some_motor = wpilib.Talon(2)

        self.joystick = wpilib.Joystick(0)

    #
    # No autonomous routine boilerplate required here, anything in the
    # autonomous folder will automatically get added to a list
    #

    def teleopPeriodic(self):
        """Place code here that does things as a result of operator
           actions"""

        try:
            if self.joystick.getTrigger():
                self.component2.do_something()
        except:
            self.onException()


if __name__ == "__main__":
    wpilib.run(MyRobot)
=======
"""
Base file that setups basic robot. Actual robot is in team3200 module.
This file should not need to be edited.
"""
import wpilib
from team3200 import Robot as Robot

if __name__ == '__main__':
    try:
        # patch no exit error if not running on robot
        try:
            print(wpilib._impl.main.exit)
        except Exception:
            wpilib._impl.main.exit = exit

        # fixes simulation rerun errors.
        # todo verify this causes no issues on robot
        wpilib.DriverStation._reset()

    except Exception as err:
        print("Failed to do extra setup. Error", err)

    wpilib.run(Robot, physics_enabled=True)
