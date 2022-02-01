from networktables import NetworkTables as networktable
from magicbot import StateMachine
from magicbot.state_machine import state
from components.shooterLogic import ShooterLogic
from components.driveTrain import DriveTrain
from utils.guessDistance import guessDistanceTrig

import logging as log
import os
from pathlib import Path

from utils import yaml


def findRPM(configName):
    """
    Will determine the correct yml file for the robot. Please run
    'echo (robotCfg.yml) > robotConfig' on the robot. This will tell the
    robot to use robotCfg file remove the () and use file name file.
    Files should be in configs dir
    """
    configPath = os.path.dirname(__file__) + os.path.sep + ".." + os.path.sep + "configs" + os.path.sep

    home = str(Path.home()) + os.path.sep
    defaultConfig = configName
    robotConfigFile = home + configName

    if not os.path.isfile(robotConfigFile):
        log.info("Could not find %s. Using %s", robotConfigFile,
                 configPath+configName)

        robotConfigFile = configPath + configName
    try:

        if os.path.isfile(robotConfigFile):
            log.info("Using %s config file", robotConfigFile)
            return configPath
        log.error("No config? Can't find %s", robotConfigFile)
    except Exception as e:
        log.error("Could not find %s", robotConfigFile)
        log.error(e)
        log.error(("Please run `echo <robotcfg.yml> >"
                   + " ~/robotConfig` on the robot"))
        log.error("Using default %s", defaultConfig)

    return configPath


def calculateRPM(dist, dir, filename):
    """
    Calculates a RPM based off of a set of values in rpmToDistance.yml
    as well as parameter dist. RPMdir is the location of rpmToDistance.yml.
    filename is the filename, most often rpmToDistance.yml
    """

    # default value in case nothing is calculated
    rpm = ShooterLogic.teleShootingSpeed

    values = yaml.load(open(dir+filename))
    minDist_x = 9
    maxRPM = 5750
    if dist < minDist_x:
        log.error("Dist is too low")
        # default rpm for low distances
        rpm = 5500
        return rpm
    if "DISTtoRPM" in values:
        DtoRPM = values["DISTtoRPM"]
        distances = list(DtoRPM.keys())
        distFound = False
        for i, distance in enumerate(distances):
            # truncate distance to integer (dist will likely be a float)
            if distance == int(dist):
                lowdist = distance
                if i < len(distances) - 1:
                    highdist = distances[i+1]
                    highRPM = DtoRPM[highdist]
                else:
                    highdist = -1
                    highRPM = 5700
                distFound = True
                lowRPM = DtoRPM[lowdist]
                break
        if distFound:
            #             4000               3500 = 500
            diff = highRPM - lowRPM
            #      5.2        5       500         3500
            rpm = (dist - lowdist) * diff + DtoRPM[lowdist]
        else:
            log.error("Dist outside of range")
            rpm = maxRPM

    else:
        log.error("Given file did not have values at base, using default RPM")

    if rpm > maxRPM:
        log.error("RPM too high. Using max of "+str(maxRPM))
        return maxRPM
    else:
        return rpm


class AutoShoot(StateMachine):
    """
    Uses the limelight's vertical offset from its target to estimate
    its distance from the target, then proceeds to use a dictionary of
    values to set a the shooter to a suitable RPM and shoot at the target.
    THIS RELIES ON THE ROBOT BEING ALIGNED.
    MAKE SURE THAT THE ROBOT IS ALIGNED BEFORE ENGAGING.
    """

    compatString = ["doof"]
    dist = int(0)
    angle = int(0)
    smartTable = networktable.getTable('SmartDashboard')
    # Initializing network table variables
    smartTable.putNumber("Distance", 0)
    smartTable.putNumber("Vertical angle offset", 0)
    smartTable.putNumber("Estimated Necessary RPM", 0)

    # Config file vars
    RPMfilename = "rpmToDistance.yml"
    RPMdir = findRPM(RPMfilename)

    # Distance estimate variables

    # height of the middle of the limelight target in feet.
    # So this is the middle of the lower half of the hexagon
    targetHeight = 82/12
    # height of the limelight on the robot in feet.
    # Used to calculate distance from the target.
    limeHeight = 35/12
    # Could also be changed using the crosshair in limelight settings
    limeLightAngleOffset = 7.81

    # IF "limeLightAngleOffset" is 0,
    # CROSSHAIR MUST BE ON HORIZONTAL IN LIMELIGHT

    shooter: ShooterLogic
    driveTrain: DriveTrain

    starting = False
    stopping = False

    @state
    def start(self):
        limeTable = networktable.getTable("limelight")

        # If limelight can see something
        self.tx = limeTable.getNumber("tx", -50)
        if self.tx != -50 or self.tx != 0:
            log.error("LImelight exist")
            # "ty" is the vertical offset from the limelight.
            self.ty = limeTable.getNumber("ty", -50)

            if self.ty == -50 or self.ty == -1 or self.ty == 0:
                log.error("ANGLES ARE MISSING, NO SHOOTING")
                self.next_state("idling")
            elif self.ty > -50 and self.ty < 50:
                self.next_state("calc_RPM_shoot")
            else:
                log.error("ANGLES ARE MISSING, NO SHOOTING")
                self.next_state("idling")
        else:
            log.error("Limelight: No Valid Targets")
            self.next_state("idling")

    @state
    def calc_RPM_shoot(self):

        self.dist_x = guessDistanceTrig(self.targetHeight, self.limeHeight,
                                        self.limeLightAngleOffset, self.ty)
        self.dist = self.dist_x
        self.angle = self.ty + self.limeLightAngleOffset
        self.rpm = calculateRPM(self.dist_x, self.RPMdir, self.RPMfilename)

        # Update variables on network tables,
        # accessable through Smart Dashboard.
        self.smartTable.putNumber("Distance", self.dist)
        self.smartTable.putNumber("Vertical angle offset", self.angle)
        self.smartTable.putNumber("Estimated Necessary RPM", self.rpm)

        self.next_state("stop_shoot")

    @state
    def stop_shoot(self):
        # stop
        self.driveTrain.setTank(0, 0)
        # set rpm
        self.shooter.setRPM(self.rpm)
        # shoot
        if not self.stopping:
            self.shooter.startShooting()
        self.next_state("idling")

    @state(first=True)
    def idling(self):
        if self.starting:
            self.starting = False
            log.error("STARTING")
            self.next_state("start")
        else:
            self.next_state('idling')

    def stop(self):
        self.stopping = True
        self.starting = False
        self.shooter.doneShooting()
        self.next_state("idling")

    def startAutoShoot(self):
        self.stopping = False
        self.starting = True
