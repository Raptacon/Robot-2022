#!/usr/bin/env python3
import team3200

import wpilib
from magicbot import MagicRobot

from components.driveTrain import DriveTrain


class MyRobot(MagicRobot):

    #
    # Define components here
    #

    driveTrain: DriveTrain

    def createObjects(self):
        """Initialize all wpilib motors & sensors"""

        # TODO: create button example here
        
        self.joystick = wpilib.Joystick(0)

        self.driveTrain_motorsList = dict(team3200.robotMap.motorsMap.driveMotors)

    #
    # No autonomous routine boilerplate required here, anything in the
    # autonomous folder will automatically get added to a list
    #

    def teleopPeriodic(self):
        """Place code here that does things as a result of operator
           actions"""
        self.driveTrain.setTank(1,1)


if __name__ == "__main__":
    wpilib.run(MyRobot)
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
