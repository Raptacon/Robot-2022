import wpilib
import logging
import motorHelper
from magicbot import MagicRobot
from components.shooterMotor import ShooterMotorClass
from components.shooterFire import ShooterFireClass
from components.loader import LoaderClass
from components.isReadytoFire import isReadyToFireClass
from components.sensor import SensorClass
from components.intake import IntakeClass

MagicBot = MagicRobot

# Remember self.on_enable and self.on_disable

class MyShooter(MagicBot):

    ShooterMotor: ShooterMotorClass
    Fire: ShooterFireClass
    Loader: LoaderClass
    IsReadyToFire: isReadyToFireClass
    Sensors: SensorClass
    Intake: IntakeClass

    def createObjects(self):
        
        # Motor Object Creation, FIXME (TODO: Get actual motors from motorHelper)
        self.LoaderMotor = wpilib.Talon(1)
        self.shooterMotor = wpilib.Talon(2)
        self.intakeMotor = wpilib.Talon(3)

        # Controller Object Creation, FIXME (TODO: Assign actual button)
        self.controller = wpilib.XboxController

        # Entry/Exit Sensor Creation, FIXME (TODO: Get actual inputs)
        self.entrySensor = wpilib.DigitalInput(0)
        self.exitSensor = wpilib.DigitalInput(5)

        # Other Sensor Creation, FIXME (TODO: Get actual inputs)
        self.sensor1 = wpilib.DigitalInput(1) # Array: 0
        self.sensor2 = wpilib.DigitalInput(2) # Array: 1
        self.sensor3 = wpilib.DigitalInput(3) # Array: 2
        self.sensor4 = wpilib.DigitalInput(4) # Array: 3

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        if self.controller.getTriggerAxis(1):
            self.Intake.run()

        if self.controller.getAButtonPressed():
            self.Fire.fire()

    def testInit(self):
        pass

    def testPeriodic(self):
        pass

if __name__ == '__main__':
    wpilib.run(MyShooter)