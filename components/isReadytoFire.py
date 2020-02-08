import time
from components.sensor import SensorClass
from components.shooterMotor import ShooterMotorClass
from components.loader import LoaderClass

class isReadyToFireClass:

    Sensor: SensorClass
    Loader: LoaderClass
    ShooterMotor: ShooterMotorClass

    def __init__(self):
        self.SensorsReady = False
        self.MotorReady = False
        self.isReady = False

    def SensorReadyCheck(self):
        if self.Sensor.getSensorShooterStatus():
            self.Loader.reverse()
            time.sleep(0.1)
            self.SensorsReady = True

        else:
            self.SensorsReady = False

    def MotorReadyCheck(self):
        # Check to see if motor is at full speed
        self.MotorReady = True

    def ReadyToFire(self):
        return self.isReady

    def execute(self):
        if self.MotorReady and self.SensorsReady:
            self.isReady = True