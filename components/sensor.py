from wpilib import DigitalInput as dio
from time import sleep
# from components.loader import initloader
from components.towerMotors import ShooterMotorCreation

class sensors:

    Motors: ShooterMotorCreation

    sensorObjects: dio
    # loaderlogicSensors: dio

    def __init__(self):

        # Basic init
        self.isCurrentSensorActivated = False # Checks if 'self.SensorArray[self.sensorX]' is 'True'
        self.isCurrentLoaderController = False # Checks if 'self.SensorArray[self.sensorX]' controls the loader
        self.CurrentSensor = None
        self.logicSensors = None

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
        print("Current sensor status:", self.CurrentSensor.get())

        try:
            if self.CurrentSensor.get():
                self.isCurrentLoaderController = True
                self.isCurrentSensorActivated = False
                # print("current sense unbroken")
                print("IsCurrentLoaderController?:", self.isCurrentLoaderController)

            elif self.CurrentSensor.get() == False:
                self.isCurrentLoaderController = False
                self.isCurrentSensorActivated = True
                # print("current sense broken")

        except Exception as err:
            print("Failed to assign a sensor:", err)

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

        # Runs loader if any other sensor (aside from the loader controller) is broken and the loader controller
        # is NOT activated
        if (
            self.isCurrentLoaderController and
            not any(self.logicArray) == False and 
            all(self.logicArray) == False
        ):
            self.Motors.runLoader(1)
            # print("loader running")
            print(" ")
            self.logicArray = []

        # Stops loader and shifts loader controller
        elif all(self.logicArray) and self.CurrentSensor.get() == False:
            self.Motors.stopLoader()
            self.sensorX += 1
            # print("loader stopping")
            print(" ")
            self.logicArray = []

        # Loader has no ball
        else:
            self.logicArray = []
            print("all else failed")
            print(" ")

        if self.sensorX > 0:
            if self.SensorArray[(self.sensorX - 1)].get():
                self.sensorX -= 1
                print("shift sensor up")
                print(" ")
                self.logicArray = []

            else:
                pass
