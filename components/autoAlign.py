from networktables import NetworkTables as networktable
from magicbot import StateMachine, tunable
from magicbot.state_machine import state, timed_state
import logging as log
from components.driveTrain import DriveTrain
from components.autoShoot import AutoShoot

class AutoAlign(StateMachine):
    """
    Puts the limelight (not necessarily the entirely robot)
    roughly perpendicular to any target the limelight
    currently has in its view.
    """

    compatString = ["doof"]
    time = 0.01
    driveTrain: DriveTrain

    # Auto Align variables
    shootAfterComplete = False
    # Maximum horizontal offset before shooting in degrees
    maxAimOffset = tunable(.25)
    PIDAimOffset = tunable(2.1)
    DumbSpeed = .14
    
    # PID
    P = tunable(0.01)
    I = tunable(0.08)
    D = tunable(0)
    PIDSpeedFloor = .11
    inverted = False
    speed = 0
    integral = 0
    preverror = 0
    #starting is false 
    starting = False

    limeTable = networktable.getTable("limelight")
    smartTable = networktable.getTable('SmartDashboard')
    smartTable.putNumber("PIDspeed", 0)
    smartTable.putNumber("Integral", 0)

    autoShoot: AutoShoot

    def setShootAfterComplete(self, input: bool):
        self.shootAfterComplete = input
        return self.shootAfterComplete

    def toggleShootAfterComplete(self):
        if self.shootAfterComplete:
            self.shootAfterComplete = False
        else:
            self.shootAfterComplete = True
        return self.shootAfterComplete
    #Stops robot from running until starting is true
    @state
    def idling(self):
        if self.starting:
            self.starting = False
            log.error("starting")
            self.next_state("start")
        else:
            self.next_state("idling")

    @state(first=True)
    def start(self):
        # If limelight can see something
        self.DeviationX = self.limeTable.getNumber("tx", -50)
        if self.DeviationX != -50 or self.DeviationX != 0:
            # "-50" is the default value, so if that is returned,
            # nothing should be done because there is no connection.
            DeviationX = self.limeTable.getNumber("DeviationX", -50)
            values = [
                     [[self.maxAimOffset, self.PIDAimOffset],["PID"]],
                     [[self.PIDAimOffset,"End"],[self.DumbSpeed]]
                     ]

            """
            
            """

            self.speed = 0
            done = True
            self.AbsolteX = abs(DeviationX)
            for section in values:
                for dists, speed in section:

                    if (len(dists) == 2 and
                       dists[0] < self.AbsolteX and
                       self.AbsolteX < dists[1] or
                       dists[1] == "End"):
                        self.speed = speed
                        self.next_state("adjust_self")
                        break

            log.info("Autoalign complete")
            self.driveTrain.setTank(0, 0)
            if self.shootAfterComplete:
                self.autoShoot.startAutoShoot()
        # If the horizontal offset is within the given tolerance,
        # finish.

        else:
            log.error("Limelight: No Valid Targets")
            self.next_state("idling")

    @timed_state(duration=time, next_state="start")
    def adjust_self(self):
        """Turns the bot"""
        if(self.DeviationX == self.AbsolteX):
            self.driveTrain.setTank(1 * self.speed, self.speed)
        else:
            self.driveTrain.setTank(-1 * self.speed, self.speed)
        self.next_state("start")

    def calc_PID(self, error):
        """
        Uses PID values defined in init section to give a power output for
        the drivetrain. "time" is the amount of time assumed to have passed.
        """
        self.integral = self.integral + error * self.time
        dError = error - self.preverror
        setspeed = self.P * (error) + self.D * dError + self.I * (self.integral)
        self.preverror = error

        if setspeed > 0:
            setspeed += self.PIDSpeedFloor
        elif setspeed < 0:
            setspeed -= self.PIDSpeedFloor

        if self.inverted:
            setspeed *= -1

        if setspeed > 1:
            setspeed = 1
        if setspeed < -1:
            setspeed = -1

        self.smartTable.putNumber("PIDspeed", setspeed)
        self.smartTable.putNumber("Integral", self.integral)
        return setspeed

    def reset_integral(self):
        self.integral = 0

    def StartautoAlign(self):
        self.start = True

    def stop(self):
        self.next_state_now("idling")
