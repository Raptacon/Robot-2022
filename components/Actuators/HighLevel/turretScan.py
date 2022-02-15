from random import random
from magicbot import StateMachine, state
from components.Actuators.HighLevel.turretTurn import TurretTurn
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
     
    @state(first=True)
    def check(self):
        """
        Like an idling state, makes sure that limelight has a target.
        If it doesn't, transitions to scanning between the left limit and right limit
        until the limelight has a target.
        """
        if self.checkTarget() == False:
            self.next_state("turnLeft")


    def checkTarget(self):
        """
        Returns true if limelight has target
        false if not
        """
        table = networktable.getTable("limelight")
        self.tv = table.getNumber('tv',None)

        if self.tv == 1:
            return True
        else:
            return False

    @state  
    def turnLeft(self):
        if self.tv == 0:
            self.turretTurn.setAngle(5)
            self.next_state("turnRight")
        else:
            self.next_state("check")
    @state
    def turnRight(self):
        self.turnright = self.rightMotor
        if self.tv == 0:
            self.turnright = random
            self.next_state("idling")
        else: 
            self.next_state("checkTarget")
    
    @feedback
    def hasTarget(self):
        return self.tv
