from wpimath.geometry import Translation2d, Rotation2d
from wpilib import kinematics
from utils import UnitEnums
import math


class movementKinematics:
    motors_drivetrain:dict
    driveTrainType: str
    # Configurable
    frontLeftLocation = Translation2d(0.3556, 0.3356)
    frontRightLocation = Translation2d(0.3356, -0.3356)
    backLeftLocation = Translation2d(-0.3356, 0.3356)
    backRightLocation = Translation2d(-0.3356, -0.3356)
    SwerveDriveKinematics = kinematics.SwerveDrive4Kinematics(frontLeftLocation, frontRightLocation, backLeftLocation, backRightLocation)

    def setup(self):
        if self.driveTrainType == "Swerve":
            self.rotationMotors = []
            for motor in self.motors_drivetrain.keys():
                if "rotation" in motor.lower():
                    self.rotationMotors.append(motor)


    def transformations(self, x,y,r):

        # Put speeds on a circle so that x^2+y^2 is never >1
        x = x*(1-(y**2)/2)**.5
        y = y*(1-(x**2)/2)**.5

        # Configurable
        topSpeed = 5
        topRotation = 2*math.pi
        x*= topSpeed
        y*= topSpeed
        r*= topRotation

        speeds = kinematics.ChassisSpeeds(y, x, r)
        moduleStates = self.SwerveDriveKinematics.toSwerveModuleStates(speeds)
        optimizedStates = []

        motorNames = ["FrontLeftRotationMotor","FrontRightRotationMotor","BackLeftRotationMotor","BackRightRotationMotor"]

        # Configurable
        gearRatio = 5

        counter = 0
        for moduleState in moduleStates:
            currentAngle = Rotation2d(self.rotationMotors[motorNames[counter]].getPosition(0, UnitEnums.positionUnits.kRotations)*2*math.pi/gearRatio)
            optimizedStates.append(kinematics.SwerveModuleState.optimize(moduleState,currentAngle))
            counter += 1

        return optimizedStates




