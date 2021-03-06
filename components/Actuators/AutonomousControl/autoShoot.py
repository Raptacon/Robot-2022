from networktables import NetworkTables as networktable
from magicbot import StateMachine
from magicbot.state_machine import state
from components.Actuators.HighLevel.driveTrainHandler import DriveTrainHandler
from components.Actuators.HighLevel.shooterLogic import ShooterLogic
from utils.guessDistance import guessDistanceTrig

import logging as log
import os

from utils import yaml


def findRPM(configName, basePath):
    """
    Will determine the correct yml file for the robot. Please run
    'echo (robotCfg.yml) > robotConfig' on the robot. This will tell the
    robot to use robotCfg file remove the () and use file name file.
    Files should be in configs dir
    """
    configPath = os.path.join(basePath,"configs")

    try:

        if os.path.isfile(os.path.join(configPath,configName)):
            log.info("Using %s config file", configPath)
            return configPath
        log.error("No config? Can't find %s", configPath)
    except Exception as e:
        log.error("Could not find %s", configPath)
        log.error(e)
        log.error("Using default %s", configPath)

    return configPath

def linearInterp(longRPM, shortRPM, dist, lowdist):
    diff = longRPM - shortRPM
    rpm = (dist - lowdist) * diff + shortRPM
    return rpm

def calculateRPM(dist, dir, filename):
    """
    Calculates a RPM based off of a set of values in rpmToDistance.yml
    as well as parameter dist. RPMdir is the location of rpmToDistance.yml.
    filename is the filename, most often rpmToDistance.yml
    """

    # default value in case nothing is calculated
    rpm = [ShooterLogic.teleShootingSpeed1, ShooterLogic.teleShootingSpeed2]

    try:
        with open(os.path.join(dir,filename), 'r') as yaml_stream:
            values = yaml.load(yaml_stream, Loader=yaml.SafeLoader)
    except:
        log.error("Cannot read yaml config file {}, check formatting.".format(yaml_stream))
        return
    maxRPM = 5000
    lowRPMs = [1500, -500]
    if "DISTtoRPM" in values:
        DtoRPM = values["DISTtoRPM"]
        distances = list(DtoRPM.keys())
        distFound = False
        for i, arrDist in enumerate(distances):
            if arrDist >= dist:
                highdist = arrDist
                if i == 0:
                    lowdist = -1
                    lowRPM1 = lowRPMs[0]
                    lowRPM2 = lowRPMs[1]
                else:
                    lowdist = distances[i-1]
                    lowRPM1 = DtoRPM[lowdist][0]
                    lowRPM2 = DtoRPM[lowdist][1]
                highRPM1 = DtoRPM[highdist][0]
                highRPM2 = DtoRPM[highdist][1]
                distFound = True

                break
        if distFound:
            rpm = [linearInterp(highRPM1, lowRPM1, dist, lowdist),
            linearInterp(highRPM2, lowRPM2, dist, lowdist)]
        else:
            log.error("Dist outside of range")
            rpm = [maxRPM, maxRPM]

    else:
        log.error("Given file did not have values at base, using default RPM")

    # If either of the RPMs are too high, set both to maxRPM
    if rpm[0] > maxRPM or rpm[1] > maxRPM:
        log.error("RPM too high. Using max of "+str(maxRPM))
        return [maxRPM, maxRPM]
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

    compatString = ["doof", "teapot"]
    dist = int(0)
    angle = int(0)
    smartTable = networktable.getTable('SmartDashboard')
    # Initializing network table variables
    smartTable.putNumber("Distance", 0)
    smartTable.putNumber("Vertical angle offset", 0)
    smartTable.putNumber("Estimated Necessary RPM", 0)

    robotDir: str

    # Config file vars
    RPMfilename = "rpmToDistance.yml"

    # Distance estimate variables

    # height of the middle of the limelight target in feet.
    targetHeight = 104/12
    # height of the limelight on the robot in feet.
    # Used to calculate distance from the target.
    limeHeight = 31/12
    # Could also be changed using the crosshair in limelight settings
    limeLightAngleOffset = 32.08235

    # IF "limeLightAngleOffset" is 0,
    # CROSSHAIR MUST BE ON HORIZONTAL IN LIMELIGHT

    shooter: ShooterLogic
    driveTrainHandler: DriveTrainHandler

    starting = False
    stopping = False

    def setup(self):
        self.RPMdir = findRPM(self.RPMfilename, self.robotDir)

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
        rpms = calculateRPM(self.dist_x, self.RPMdir, self.RPMfilename)
        self.rpm1 = rpms[0]
        self.rpm2 = rpms[1]

        # Update variables on network tables,
        # accessable through Smart Dashboard.
        self.smartTable.putNumber("Distance", self.dist)
        self.smartTable.putNumber("Vertical angle offset", self.angle)
        self.smartTable.putNumberArray("Estimated Necessary RPM", rpms)

        self.next_state("stop_shoot")
    @state
    def stop_shoot(self):
        # set rpm
        self.shooter.setRPM(self.rpm1, self.rpm2)
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
