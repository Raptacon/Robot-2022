from wpilib import DigitalInput as dio
from time import sleep
# from components.loader import initloader
from components.towerMotors import ShooterMotorCreation

class sensors:

    Motors: ShooterMotorCreation

    sensorObjects: dio

    def __init__(self):

        # Basic init
        self.isCurrentSensorActivated = False # Checks if 'self.SensorArray[self.sensorX]' is 'True'
        self.isCurrentLoaderController = False # Checks if 'self.SensorArray[self.sensorX]' controls the loader
        self.CurrentSensor = None
        self.logicSensors = None
        self.shooterActivated = False

        self.logicArray = []

        self.SensorArray = []

        # Key for sensors in 'self.Sensors' array
        self.sensorX = 0

        for x in range(1, 6):
            self.sensorObjects = dio(x)
            self.SensorArray.append(self.sensorObjects)

    def detectSensorPresence(self):

        # Sets the current sensor
        self.CurrentSensor = self.SensorArray[self.sensorX]
        print("Sensor key:", self.sensorX)

        try:
            if self.CurrentSensor.get():
                self.isCurrentLoaderController = True
                self.isCurrentSensorActivated = False
                print("IsCurrentLoaderController?:", self.isCurrentLoaderController)

            elif self.CurrentSensor.get() == False:
                self.isCurrentLoaderController = False
                self.isCurrentSensorActivated = True

        except Exception as err:
            print("Failed to assign a sensor:", err)

    def executeShooter(self):
        if self.SensorArray[0].get() == False:
            self.shooterActivated = True
        else:
            self.shooterActivated = False

    def execute(self):
        try:
            assert(self.sensorX >= 0)
        except AssertionError as err:
            print("Sensor key assertion failed:", err)

        # Creates the basis for the logic regarding when the loader is run.
        for x in range((self.sensorX + 1), 5):
            self.logicSensors = self.SensorArray[x].get()
            self.logicArray.append(self.logicSensors)

        print("Logic Array:", self.logicArray)

        if (
            self.isCurrentLoaderController and
            # not any(self.logicArray) == False and 
            all(self.logicArray) == False
        ):
            self.Motors.runLoader(1)
            self.logicArray = []

        # Stops loader and shifts loader controller
        elif self.CurrentSensor.get() == False and all(self.logicArray):
            self.Motors.stopLoader()
            self.sensorX += 1
            self.logicArray = []

        elif self.CurrentSensor.get() == False and all(self.logicArray) == False:
            self.Motors.runLoader(1)
            self.sensorX += 1
            self.logicArray = []

        # Intake has no ball
        else:
            self.logicArray = []

        if self.sensorX > 0:
            if self.SensorArray[(self.sensorX - 1)].get():
                self.sensorX -= 1
                self.logicArray = []

            else:
                pass

        if self.shooterActivated:
            self.Motors.stopLoader()
            sleep(.1)
            self.Motors.runLoader(-1)
            if self.SensorArray[0].get():
                self.Motors.runShooter(1)
                sleep(.2) # Add encoder logic to towerMotors.py
                self.Motors.runLoader(1)
                if all(self.logicArray) and self.SensorArray[0].get():
                    sleep(.5)
                    self.Motors.stopLoader()

