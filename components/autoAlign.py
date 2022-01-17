from networktables import NetworkTables as networktable
from magicbot import StateMachine, tunable
from magicbot.state_machine import state, timed_state
import logging as log
from components.driveTrain import DriveTrain
from components.autoShoot import AutoShoot
from utils.DirectionEnums import Direction

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

    @state(first=True)
    def start(self):
        # If limelight can see something
        self.tx = self.limeTable.getNumber("tx", -50)
        if self.tx != -50 or self.tx != 0:
            # "-50" is the default value, so if that is returned,
            # nothing should be done because there is no connection.
            tx = self.limeTable.getNumber("tx", -50)
            if tx != -50 and tx != 0:
                if tx > self.maxAimOffset:
                    if tx < self.PIDAimOffset:
                        self.speed = self.calc_PID(tx)
                    else:
                        self.speed = self.DumbSpeed
                    self.next_state_now("adjust_self_right")

                elif tx < -1 * self.maxAimOffset:
                    if tx > -1 * self.PIDAimOffset:
                        self.speed = -1 * self.calc_PID(tx)
                    else:
                        self.speed = self.DumbSpeed
                    self.next_state_now("adjust_self_left")

                # If the horizontal offset is within the given tolerance,
                # finish.
                else:
                    log.info("Autoalign complete")
                    self.driveTrain.setTank(0, 0)
                    if self.shootAfterComplete:
                        self.autoShoot.startAutoShoot()

        else:
            log.error("Limelight: No Valid Targets")

    @timed_state(duration=time, next_state="start")
    def adjust_self_right(self):
        """Turns the bot right"""
        self.driveTrain.setTank(-1 * self.speed, self.speed)

    @timed_state(duration=time, next_state="start")
    def adjust_self_left(self):
        """Turns the bot left"""
        self.driveTrain.setTank(self.speed, -1 * self.speed)

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

    @state
    def idling(self):
        pass

    def stop(self):
        self.next_state_now("idling")
