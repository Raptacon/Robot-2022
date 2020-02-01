#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot

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

    def autonomousInit(self):
        '''This is where we pretend we do autonomous'''
        log.info("autonmous robot initialized")


    def operatorControl(self):
        '''This is where we take control'''
        log.info("operator control")
        while self.isOperatorControl and self.isEnabled:
            log.debug("joystick is %f y %f x", self.controller.getY(), self.controller.getX())
            wpilib.Timer.delay(.1)
            self.motor.set(self.controller.getY())
            self.pwMotor.set(self.controller.getX())

if __name__ == "__main__":
    wpilib.run(MyRobot)
