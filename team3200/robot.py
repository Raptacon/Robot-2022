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

    # You can even pass constants to components
    SOME_CONSTANT = 1

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

