from time import sleep
import wpilib
from components.loader import LoaderClass

# NOTE: This code is written on the basis that 'True' means that the sensor is broken. REFACTOR IF NECESSARY!!!
# FIXME: Sensors read 'False' when BROKEN, so REFACTOR THIS ASAP!!!!!!!!!

dio = wpilib.DigitalInput

class SensorClass:

    Loader: LoaderClass

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

    def setCurrentSensorProperties(self):

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
        """
        try:
            assert(self.sensorX >= 0)
        except AssertionError as err:
            print("Sensor key assertion failed:", err)
        """

        # Creates the basis for the logic regarding when the loader is run.
        print("test")
        for x in range((self.sensorX + 1), 5):
            self.logicSensors = self.SensorArray[x].get()
            self.logicArray.append(self.logicSensors)

        print("Logic Array:", self.logicArray)

        # Runs loader if:
            # Sensor controls the loader
            # Any other sensors are activated
        if (
            self.isCurrentLoaderController and
            not any(self.logicArray)
            # all(self.loaderlogicSensors) == False
        ):
            # self.Loader.run()
            print("loader running")
            print(" ")
            self.logicArray = []

        # Stops loader and shifts sensor responsibility if:
            # ONLY the loader sensor is activated
        elif all(self.logicArray) and self.CurrentSensor.get() == False:
            # self.Loader.stop()
            self.sensorX += 1
            print("loader stopping")
            print(" ")
            self.logicArray = []

        # Shifts sensor responsibility if:
            # Sensor behind the current sensor doesn't have a ball FIXME: Incorrect pseudocode
        elif self.SensorArray[(self.sensorX - 1)].get():
            self.sensorX -= 1
            print("shift sensor up")
            print(" ")
            self.logicArray = []

        else:
            self.logicArray = []
            print("all else failed to pass")
            print(" ")

