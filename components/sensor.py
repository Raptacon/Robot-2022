from time import sleep
import wpilib
from components.loader import LoaderClass

# NOTE: This code is written on the basis that 'True' means that the sensor is broken. REFACTOR IF NECESSARY!!!
# FIXME: Sensors read 'False' when BROKEN, so REFACTOR THIS ASAP!!!!!!!!!

dio = wpilib.DigitalInput

class SensorClass:

    Loader: LoaderClass

    """
    sensor1: dio
    sensor2: dio
    sensor3: dio
    sensor4: dio
    sensor5: dio
    """
    sensorObjects: dio

    # sensorObjects: dio

    def __init__(self):

        # Basic init
        self.isCurrentSensorActivated = False # Checks if 'self.SensorArray[self.sensorX]' is 'True'
        self.isCurrentLoaderController = False # Checks if 'self.SensorArray[self.sensorX]' controls the loader
        self.CurrentSensor = None

        """
        # Sensor array
        self.SensorArray = [
            self.sensor1,
            self.sensor2,
            self.sensor3,
            self.sensor4,
            self.sensor5
        ]
        """

        self.SensorArray = []

        for x in range(1, 6):
            sensorObjects = dio(x)
            self.SensorArray.append(sensorObjects)

        # Key for sensors in 'self.Sensors' array
        self.sensorX = 0

        """
        # Creates all 5 sensors and allocates them to an array, NOTE: Needs testing
        for senseCreation in range(1, 6):
            self.SensorArray.append(self.sensorObjects(senseCreation))
        """

    def setCurrentSensorProperties(self):

        # Sets the current sensor
        self.CurrentSensor = self.SensorArray[self.sensorX]

        try:
            if self.CurrentSensor.get():
                self.isCurrentLoaderController = True
                self.isCurrentSensorActivated = False
                print("current sense unbroken")

            elif self.CurrentSensor.get() == False:
                self.isCurrentLoaderController = False
                self.isCurrentSensorActivated = True
                print("current sense broken")

        except Exception as err:
            print("Failed to assign a sensor:", err)

    def execute(self):

        # Creates the basis for the logic regarding when the loader is run.
        for sensorKey in range((self.sensorX + 1), 6):
            self.loaderlogicSensors = self.SensorArray[sensorKey].get()

        # Runs loader if:
            # Sensor controls the loader
            # Any other sensors are activated
        if (
            self.isCurrentLoaderController and
            not any(self.loaderlogicSensors)
        ):
            # self.Loader.run()
            print("loader running")

        # Stops loader and shifts sensor responsibility if:
            # ONLY the loader sensor is activated
        elif any(self.loaderlogicSensors):
            self.Loader.stop()
            self.sensorX += 1

        # Shifts sensor responsibility if:
            # Sensor behind the current sensor doesn't have a ball FIXME: Incorrect pseudocode
        elif self.SensorArray[(self.sensorX - 1)].get() == False:
            self.sensorX -= 1

        # Assertion that array keys called exist
        assert(
            self.sensorX >= 0 and
            self.sensorX <= 4,
            'Sensor not in array range.' 
        )