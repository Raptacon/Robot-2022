from argparse import BooleanOptionalAction
from random import random
from turtle import speed
from typing_extensions import Self
from xmlrpc.client import boolean
from magicbot import StateMachine, state
from components.Actuators.AutonomousControl.turnToAngle import TurnToAngle
from components.Actuators.HighLevel.turretTurn import TurretTurn
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from components.SoftwareControl.speedSections import SpeedSections
from networktables import NetworkTables as networktable
import logging as log

# TODO: start scanning
# TODO: Return scan result

class TurretScan (StateMachine):
    compatString = ["doof", "greenChassis"]
    limeTable = networktable.getTable("limelight")
    turretTurn: TurretTurn
    speedSections: SpeedSections
    turretThreshold: TurretThreshold
    stateTurn = "turnRight"
     
    @state(first=True)
    def check(self):
        """
        Like an idling state, makes sure that limelight has a target.
        If it doesn't, transitions to scanning between the left limit and right limit
        until the limelight has a target.
        """
        if self.hasTarget() == False:
            self.next_state("turnLeft")
        else:
            self.next_state("check")

    @state  
    def turnLeft(self):
        if self.hasTarget() == False:
            self.turretTurn.setAngle(self.turretThreshold.Deadzones[0][0])
            self.next_state("wait")
        else:
            self.next_state("check")

    @state
    def wait(self):
        turn = self.turretTurn.getTurning()

        if turn:
            self.next_state("wait")
        else:
            self.next_state(self.stateTurn)

    @state
    def turnRight(self):
        if self.hasTarget() == False:
            self.turretTurn.setAngle(self.turretThreshold.Deadzones[0][1])
            self.stateTurn = "turnLeft"
            self.next_state("wait")
        else: 
            self.next_state("check")

    @feedback
    def hasTarget(self):
        self.tv = self.limeTable.getNumber("tv", None)
        if self.tv == 1:
            return True
        else:
            return False

