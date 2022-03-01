from magicbot import feedback
from networktables import NetworkTables as networktable
import logging as log

class TurretThreshold:
    compatString = ["teapot"]
    motors_turret: dict
    speed = 0
    pos = 0
    exitSpeed = .05
    safetySpeed = .07
    gearRatio = 5
    sprocketRatio = 175/18
    turretMotor = None
    DegreeToAngle = 0
    limitSwitchTable = networktable.getTable("SmartDashboard")
    leftLim = None
    rightLim = None

    calibrating = False
    calibSpeed = .11
    manual = False

    def setManual(self, manual:bool):
        self.manual = manual

    def setup(self):
        #connects moters and gets position
        # Clear any existing deadzones (they probably aren't good)
        self.limitSwitchTable.delete("Left Limit")
        self.limitSwitchTable.delete("Right Limit")
        self.turretMotor = self.motors_turret["turretMotor"]
        self.encoder = self.turretMotor.getEncoder()


    def on_enable(self):

        self.leftLim = self.limitSwitchTable.getNumber("Left Limit", None)
        self.rightLim = self.limitSwitchTable.getNumber("Right Limit", None)

        if self.leftLim == None and self.rightLim == None:
            log.error("MUST CALIBRATE TURRET")
            self.calibrated = False
        elif self.LeftLim != None and self.RightLim != None:
            self.calibrated = True
        else:
            log.error("Half calibrated turret")
        self.pos = self.encoder.getPosition()
        self.speed = 0

    def setDeadzones(self, lLimit, rLimit):
        """
        Pass deadzones to turret.
        ONLY DO THIS IF YOU KNOW EXACTLY WHAT YOU ARE DOING
        """
        self.leftLim = lLimit
        self.rightLim = rLimit
        self.calibrated = True

    def setCalibrating(self, calib):
        """
        SHOULD ONLY BE USED IF YOU KNOW
        /EXACTLY/ WHAT YOU ARE DOING
        DO NOT USE
        Sets calibrating to true, overriding
        safety checks so that we can calibrate the turret.
        """
        self.calibrating = calib

    def setTurretspeed(self, tSpeed):
        """
        sets speed
        """
        self.speed = tSpeed

    def stopTurret(self):
        """
        stops turret
        """
        self.speed = 0

    def angleCheck(self, angle):
        """
        Checks if desired angle is within the deadzone. Then, returns closest point to the angle it can reach.
        Also checks if the desired angle jumps over the deadzone relative to where you are now.
        """
        if self.calibrated == False and self.calibrating:
            return angle
        elif self.calibrated == False:
            return False

        lLim = self.leftLim
        rLim = self.rightLim

        # If angle is beyond limits in either direction
        if angle < lLim:
            return lLim
        if angle > rLim:
            return rLim
        return angle

    @feedback
    def getPosition(self):
        return self.pos

    @feedback
    def getSpeed(self):
        return self.speed

    def calc_Position(self):
        """
        Returns position based on encoder + gear ratios.
        """
        self.pos = 360 * self.encoder.getPosition() / (self.gearRatio * self.sprocketRatio)

    def execute(self):
        """
        gets position, sets speed for every frames
        """
        self.calc_Position()

        if self.calibrated:

            # If we are currently outside of deadzones, re-enter
            if self.pos < self.leftLim:
                log.error("Too low")
                self.speed = self.exitSpeed
            elif self.pos > self.rightLim:
                log.error("Too high")
                self.speed = -1*self.exitSpeed


            self.turretMotor.set(self.speed)

        elif self.calibrating:
            log.error("Calibrating Turret")
            if abs(self.speed) > abs(self.calibSpeed):
                if self.speed > 0:
                    self.speed = self.calibSpeed
                else:
                    self.speed = -1*self.calibSpeed
            self.turretMotor.set(self.speed)
        elif self.manual:
            self.turretMotor.set(self.speed)
        else:
            self.turretMotor.set(0)
            log.debug("Calibrate the turret bud.")
