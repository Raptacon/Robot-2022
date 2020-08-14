from networktables import NetworkTables as networktable
from magicbot import StateMachine, tunable
from magicbot.state_machine import state, timed_state
from components.driveTrain import DriveTrain
from components.shooterLogic import ShooterLogic
import math

import logging as log
import os
from pathlib import Path

import yaml



def findRPM(configName):
    """
    Will determine the correct yml file for the robot.
    Please run 'echo (robotCfg.yml) > robotConfig' on the robot.
    This will tell the robot to use robotCfg file remove the () and use file name file.
    Files should be configs dir
    """
    configPath = os.path.dirname(__file__) + os.path.sep + ".." +os.path.sep + "configs" + os.path.sep
    home = str(Path.home()) + os.path.sep
    defaultConfig = configName
    robotConfigFile = home + configName

    if not os.path.isfile(robotConfigFile):
        log.info("Could not find %s. Using %s", robotConfigFile, configPath+configName)
        robotConfigFile = configPath + configName
    try:

        if os.path.isfile(robotConfigFile):
            log.info("Using %s config file", robotConfigFile)
            return configPath
        log.error("No config? Can't find %s", robotConfigFile)
    except Exception as e:
        log.error("Could not find %s", robotConfigFile)
        log.error(e)
        log.error("Please run `echo <robotcfg.yml> > ~/robotConcig` on the robot")
        log.error("Using default %s", defaultConfig)

    return configPath


def calculateRPM(dist, dir, filename):
    """Calculates a RPM based off of a quadratic derived from values in rpmToDistance.yml
    as well as parameter dist. RPMdir is the location of rpmToDistance.yml. filename is the filename, most often rpmToDistance.yml"""


    values = yaml.load(open(dir+filename))
    if "QuadVals" in values:
        quadVals = values["QuadVals"]
        if "a" in quadVals and "b" in quadVals and "c" in quadVals:
            a = quadVals["a"]
            b = quadVals["b"]
            c = quadVals["c"]
        else:
            log.error("Given file did not have correct values in QuadVals (needs a, b and c)")
            return
    else:
        log.error("Given file did not have QuadVals at base")
        return

    rpm = (a*(dist**2))+b*dist+c
    return rpm



class AutoAim(StateMachine):
    compatString = ["doof"]
    time = 0.1
    driveTrain: DriveTrain
    shooter: ShooterLogic
    targetHeight = 6.97916667 #height of the middle of the limelight target in feet. So this is the middle of the lower half of the hexagon
    limeHeight = 3.5 #height of the limelight on the robot in feet. Used to calculate distance from the target.
    drive_speed_left = tunable(.05)
    drive_speed_right = tunable(-.05)
    minAimOffset = .5;
    RPMfilename = "rpmToDistance.yml"
    RPMdir = findRPM(RPMfilename)

    @state(first = True)
    def start(self):
        #TODO: Calculate distance from target using limelight values.
        table = networktable.getTable("limelight")


        if table.getNumber("tv", -1) == 1: #If limelight has any valid targets
            tx = table.getNumber("tx", -50) # "-50" is the default value, so if that is returned, nothing should be done because there is no connection.
            self.ty = table.getNumber("ty", -50) #"ty" is the vertical offset. I figure this is more reliable than using size as a guess for distance.
            if tx != -50:
                if tx > self.minAimOffset:
                    self.next_state_now("adjust_self_left")
                elif tx < -1 * self.minAimOffset:
                    self.next_state_now("adjust_self_right")
                elif tx < self.minAimOffset and tx > -1 * self.minAimOffset:
                    self.next_state_now("stop_shoot")
                else:
                    self.next_state("calc_RPM")
                    self.next_state_now("stop")
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

    @state(must_finish = True)
    def stop_shoot(self):
        #stop
        self.driveTrain.setTank(0, 0)
        #set rpm
        self.shooter.setRPM(self.rpm)
        #shoot
        self.shooter.shootBalls()

    @state(must_finish = True)
    def calc_RPM(self):
        
        dist_x = (self.targetHeight - self.limeHeight) / math.degrees(math.tan(self.ty))
        self.rpm = calculateRPM(dist_x, self.RPMdir, self.RPMfilename)
        print("        RPM CALCULATED: ", self.rpm)
