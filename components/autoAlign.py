from networktables import NetworkTables as networktable
from magicbot import StateMachine, tunable
from magicbot.state_machine import state, timed_state
from components.driveTrain import DriveTrain
from components.autoShoot import AutoShoot
import math

import logging as log
import os
from pathlib import Path

import yaml

class AutoAlign(StateMachine):
    """
    Puts the limelight (not necessarily the entirely robot) roughly perpendicular to
    any target the limelight currently has in its view.
    """

    compatString = ["doof"]
    time = 0.1
    driveTrain: DriveTrain

    #Auto Align variables
    shootAfterComplete = False
    drive_speed_left = tunable(.2)
    drive_speed_right = tunable(-.2)
    maxAimOffset = 6

    def setShootAfterComplete(self, input: bool):
        self.shootAfterComplete = input

    def toggleShootAfterComplete(self):
        if self.shootAfterComplete:
            self.shootAfterComplete = False
        else:
            self.shootAfterComplete = True

    @state(first = True)
    def start(self):
        limeTable = networktable.getTable("limelight")


        if limeTable.getNumber("tx", -50) != -50 or limeTable.getNumber("tx", -50) != 0: #If limelight can see something
            tx = limeTable.getNumber("tx", -50) # "-50" is the default value, so if that is returned, nothing should be done because there is no connection.
            if tx != -50:
                if tx < -1 * self.maxAimOffset:
                    self.next_state_now("adjust_self_left")

                elif tx > self.maxAimOffset:
                    self.next_state_now("adjust_self_right")

                elif tx < self.maxAimOffset and tx > -1 * self.maxAimOffset: #If the horizontal offset is within the given tolerance, finish.
                    if self.shootAfterComplete:
                        AutoShoot.engage()
                        self.done()
                    else:
                        self.done()

        else:
            log.error("Limelight: No Valid Targets")


    @timed_state(duration = time, next_state = "start")
    def adjust_self_left(self):
        """Drives the bot backwards for a time"""
        self.driveTrain.setTank(self.drive_speed_left, self.drive_speed_right) #We could do this based off of PID and error at some point, instead of timing.
    
    @timed_state(duration = time, next_state = "start")
    def adjust_self_right(self):
        """Drives the bot backwards for a time"""
        self.driveTrain.setTank(self.drive_speed_right, self.drive_speed_left)
