from time import sleep
import wpilib
from components.loader import LoaderClass

# NOTE: This code is written on the basis that 'True' means that the sensor is broken. REFACTOR IF NECESSARY!!!

dio = wpilib.DigitalInput

class SensorClass:

    Loader: LoaderClass

    sensor1: dio
    sensor2: dio
    sensor3: dio
    sensor4: dio

    def on_enable(self):

        # Basic init
        self.isCurrentSensorActivated = False # Checks if 'self.Sensors[self.sensorX]' is 'True'
        self.isCurrentLoaderController = False # Checks if 'self.Sensors[self.sensorX]' controls the loader

        # Sensor creation
        self.sensor1 = dio(1).get()
        self.sensor2 = dio(2).get()
        self.sensor3 = dio(3).get()
        self.sensor4 = dio(4).get()

        # Sensor array
        self.Sensors = [
            self.sensor1, 
            self.sensor2, 
            self.sensor3, 
            self.sensor4
        ]

        # Key for sensors in 'self.Sensors' array
        self.sensorX = 0

        # Sets the current sensor
        self.CurrentSensor = self.Sensors[self.sensorX]

    def setCurrentSensorProperties(self):
        try:
            if self.CurrentSensor == False:
                self.isCurrentLoaderController = True
                self.isCurrentSensorActivated = False

            elif self.CurrentSensor.get():
                self.isCurrentLoaderController = False
                self.isCurrentSensorActivated = True

        except Exception as err:
            print("Failed to assign a sensor.", err)

    def execute(self):

        # Runs loader if:
            # Sensor controls the loader
            # Sensor is NOT activated (meaning it has yet to recieve a ball)
            # Any other sensors are activated, FIXME: Configure for other sensors, not just sensor1
        if (
            self.isCurrentLoaderController and
            self.isCurrentSensorActivated == False and
            any(self.Sensors)
        ):
            self.Loader.run()

        # Stops loader and shifts sensor responsibility if:
            # Current sensor is activated (recieved a ball)
        elif self.isCurrentSensorActivated:
            self.Loader.stop()
            self.sensorX += 1

        # Shifts sensor responsibility if:
            # Sensor behind the current sensor doesn't have a ball
        elif self.Sensors[(self.sensorX - 1)] == False:
            self.sensorX -= 1

        # Assertion that array keys called exist
        assert(
            self.sensorX >= 0 and
            self.sensorX <= 3,
            'Sensor not in array range.' 
        )
