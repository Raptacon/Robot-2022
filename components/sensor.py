from wpilib import DigitalInput as dio
from time import sleep
from components.towerMotors import ShooterMotorCreation

class sensors:

    Motors: ShooterMotorCreation
    sensorObjects: dio

    def __init__(self):

        # Basic init:
        self.CurrentSensor = None
        self.logicSensors = None
        self.shooterActivated = False

        self.logicArray = []

        self.SensorArray = []

        # Key for sensors in 'self.Sensors' array:
        self.sensorX = 0

        # Creates sensors:
        for x in range(1, 6):
            self.sensorObjects = dio(x)
            self.SensorArray.append(self.sensorObjects)

    def fireShooter(self):

        # Executes shooter if ball is at the shooter:
        if self.SensorArray[0].get() == False:
            self.shooterActivated = True
        else:
            self.shooterActivated = False

    def execute(self):

        # Assert that sensor called exists:
        try:
            assert(self.sensorX >= 0 and self.sensorX <= 4)
        except AssertionError as err:
            print("Sensor key assertion failed:", err)

        # Sets the current sensor:
        self.CurrentSensor = self.SensorArray[self.sensorX]

        '''
        Creates the basis for the logic regarding when the loader is run.
        Checks boolean values all sensors aside from current sensor.
        '''
        for x in range((self.sensorX + 1), 5):
            self.logicSensors = self.SensorArray[x].get()
            self.logicArray.append(self.logicSensors)

        # NOTE: After every control loop, the logicArray MUST be reset

        # If one ball is loaded:
        if (
            self.CurrentSensor.get() and
            all(self.logicArray) == False
        ):
            self.Motors.runLoader(1)
            self.logicArray = []

        # If one ball has reached loader sensor:
        elif self.CurrentSensor.get() == False and all(self.logicArray):
            self.Motors.stopLoader()
            self.sensorX += 1
            self.logicArray = []

        # If more than one ball is loaded:
        elif self.CurrentSensor.get() == False and all(self.logicArray) == False:
            self.Motors.runLoader(1)
            self.sensorX += 1
            self.logicArray = []

        # Intake has no ball:
        else:
            self.logicArray = []

        # Shifts loader responsibility:
        if self.sensorX > 0:
            if self.SensorArray[(self.sensorX - 1)].get():
                self.sensorX -= 1
                self.logicArray = []

            else:
                pass

        # Fires shooter:
        if (
            self.shooterActivated and 
            all(self.logicArray) and 
            self.CurrentSensor.get()
        ):
            self.Motors.stopLoader()
            sleep(.1)
            self.Motors.runLoader(-1)
            if self.SensorArray[0].get():
                self.Motors.runShooter(1)
                sleep(.3) # Add encoder logic to towerMotors.py
                self.Motors.runLoader(1)
                if all(self.logicArray) and self.SensorArray[0].get():
                    sleep(.5)
                    self.Motors.stopLoader()
