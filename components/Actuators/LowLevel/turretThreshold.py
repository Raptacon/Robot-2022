from magicbot import feedback
from networktables import NetworkTables as networktable
import logging as log
class TurretThreshold:
    compatString = ["teapot"]
    motors_turret: dict
    speed = 0
    pos = 0
    exitSpeed = .02
    safetySpeed = .07
    safetyThreshold = 5
    gearRatio = 5
    sprocketRatio = 175/18
    turretMotor = None
    DegreeToAngle = 0
    limitSwitchTable = networktable.getTable("SmartDashboard")
    Deadzones = [[]]

    calibrating = False
    calibSpeed = .1
    def setup(self):
        #connects moters and gets position
        # Clear any existing deadzones (they probably aren't good)
        self.limitSwitchTable.delete("Left Limit")
        self.limitSwitchTable.delete("Right Limit")
        self.turretMotor = self.motors_turret["turretMotor"]
        self.encoder = self.turretMotor.getEncoder()


    def on_enable(self):

        self.Deadzones[0] = [self.limitSwitchTable.getNumber("Left Limit", None), self.limitSwitchTable.getNumber("Right Limit", None)]

        if self.Deadzones[0][0] == None or self.Deadzones[0][1] == None:
            log.error("MUST CALIBRATE TURRET")
            self.calibrated = False
        else:
            self.calibrated = True
        self.pos = self.encoder.getPosition()
        self.speed = 0

    def setDeadzones(self, lLimit, rLimit):
        self.Deadzones[0] = [lLimit, rLimit]
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
        for lLim, rLim in self.Deadzones:
            # If we're jumping the deadzone in either direction
            # or the angle is inside of the deadzone
            if ((lLim >= self.pos and rLim <= angle)
                or (lLim >= angle and rLim <= self.pos)):
                if lLim >= self.pos:
                    return lLim
                if lLim >= angle:
                    return rLim
                # Return the limit on the nearest side of the deadzone
            if (angle >= lLim and angle <= rLim):
                if lLim >= self.pos:
                    return lLim
                if rLim <= self.pos:
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

            for lLimit, rLimit in self.Deadzones:
                if self.pos > lLimit and self.pos < rLimit:
                    if abs(lLimit - self.pos) < abs(rLimit - self.pos):
                        self.speed = -1*self.exitSpeed
                    else:
                        self.speed = self.exitSpeed

            self.turretMotor.set(self.speed)

        elif self.calibrating:
            if self.speed > self.calibSpeed:
                self.speed = self.calibSpeed
            self.turretMotor.set(self.speed)
        else:
            log.error("Calibrate the turret bud.")
