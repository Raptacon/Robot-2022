import wpilib
import logging
from components.loader import LoaderClass

# NOTE: This code is written on the basis that 'True' means that the sensor is broken. REFACTOR IF NECESSARY!!!

class SensorClass:

    Loader: LoaderClass

    entrySensor: wpilib.DigitalInput
    exitSensor: wpilib.DigitalInput

    sensor1: wpilib.DigitalInput
    sensor2: wpilib.DigitalInput
    sensor3: wpilib.DigitalInput
    sensor4: wpilib.DigitalInput

    def __init__(self):
        self.CurrentSensor = None
        self.sensorX = 0
        self.isCurrentSensorActivated = False
        self.isLoaderSensor = True

        # self.EntrySensorStatus = False
        self.EntryLoaderStatus = False
        self.ExitSensorStatus = False
        # self.ExitLoaderStatus = False

        self.Sensors = [
            self.sensor1, 
            self.sensor2, 
            self.sensor3, 
            self.sensor4
        ]

    def setSensor(self):
        assert(
            self.sensorX >= 0 and
            self.sensorX <= 3,
            'Sensor not in array range.' 
        )
        self.CurrentSensor = self.Sensors[self.sensorX]

    def setCurrentSensorProperties(self):
        try:
            if self.CurrentSensor.get() == False:
                self.isLoaderSensor = True
                self.isCurrentSensorActivated = False

            elif self.CurrentSensor.get():
                self.isLoaderSensor = False
                self.isCurrentSensorActivated = True

        except Exception as err:
            print("Failed to assign a sensor.", err)

    def LoaderLogic(self):
        if self.entrySensor.get():
            if self.entrySensor.get() == False:
                self.EntryLoaderStatus = True

        elif self.isCurrentSensorActivated:
            self.EntryLoaderStatus = False

        if self.exitSensor.get():
            if self.exitSensor.get() == False:
                self.ExitSensorStatus = True

                if self.ExitSensorStatus == True:
                    self.ExitSensorStatus = False

    def getSensorShooterStatus(self):
        return self.Sensors[self.sensor1].get()

    def getSensorStatus(self):
        return self.CurrentSensor.get()

    def execute(self):
        if (
            self.isLoaderSensor and
            self.isCurrentSensorActivated == False and
            self.EntryLoaderStatus
        ):
            self.Loader.run()

        elif self.isCurrentSensorActivated:
            self.Loader.stop()
            self.sensorX += 1

        elif self.ExitSensorStatus:
            self.sensorX -= 1