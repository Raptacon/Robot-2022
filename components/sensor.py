from wpilib import DigitalInput as dio
from components.towerMotors import ShooterMotorCreation

class sensors:

    ShooterMotors: ShooterMotorCreation
    sensorObjects: dio

    def __init__(self):

        # Basic init:
        self.CurrentSensor = None
        self.logicSensors = None
        self.initShooter = False
        self.startShooter = False

        # Arrays for sensors/logic-based sensors:
        self.logicArray = []
        self.SensorArray = []

        # Key for sensors in 'self.SensorArray' array:
        self.sensorX = 0

        # Creates sensors:
        for x in range(1, 6):
            self.sensorObjects = dio(x)
            self.SensorArray.append(self.sensorObjects)

    def fireShooter(self, contInput):

        # Executes shooter if ball is at the shooter:
<<<<<<< HEAD
        # if self.SensorArray[0].get() == False:
        #     self.shooterActivated = True
        self.Motors.runShooter(.9)
        print("Velocity: ",self.Motors.shooterMotor.getEncoder().getVelocity()>=3500)
        if self.Motors.shooterMotor.getEncoder().getVelocity()>=3500:
            self.Motors.runLoader(.2)
=======
        if self.SensorArray[0].get() == False:
            self.initShooter = contInput
>>>>>>> f0e6b46dd53c459eb7cb02c9b6a767e9e49eadb3

    def execute(self):

        # Assert that sensor called exists: (For some reason this doesn't work)
        if self.sensorX<0:
            self.sensorX = 0
        elif self.sensorX>4:
            self.sensorX = 4

        # Sets the current sensor:
        self.CurrentSensor = self.SensorArray[self.sensorX]
        '''
        Creates the basis for the logic regarding when the loader is run.
        Checks boolean values all sensors aside from current sensor, and
        runs loader appropriately in if-elif-else chain:
        '''
        for x in range((self.sensorX + 1), 5):
            self.logicSensors = self.SensorArray[x].get()
            self.logicArray.append(self.logicSensors)

        # NOTE: After every control loop, the logicArray MUST be reset

        # If one ball is loaded:
<<<<<<< HEAD
        # if (
        #     self.CurrentSensor.get() and
        #     all(self.logicArray) == False
        # ):
        #     self.Motors.runLoader(1)
        #     self.logicArray = []

        # If one ball has reached loader sensor:
        # elif self.CurrentSensor.get() == False and all(self.logicArray):
        #     self.Motors.stopLoader()
        #     self.sensorX += 1
        #     self.logicArray = []

        # If more than one ball is loaded:
        # elif self.CurrentSensor.get() == False and all(self.logicArray) == False:
        #     self.Motors.runLoader(1)
        #     self.sensorX += 1
        #     self.logicArray = []
=======
        if (
            self.CurrentSensor.get() and
            all(self.logicArray) == False
        ):
            self.ShooterMotors.runLoader(1)
            self.logicArray = []

        # If one ball has reached loader sensor:
        elif self.CurrentSensor.get() == False and all(self.logicArray):
            self.ShooterMotors.stopLoader()
            self.sensorX += 1
            self.logicArray = []

        # If more than one ball is loaded:
        elif self.CurrentSensor.get() == False and all(self.logicArray) == False:
            self.ShooterMotors.runLoader(1)
            self.sensorX += 1
            self.logicArray = []
>>>>>>> f0e6b46dd53c459eb7cb02c9b6a767e9e49eadb3

        # Intake has no ball:
        else:
            self.logicArray = []

        # Shifts loader responsibility:
        if self.sensorX > 0:
            if self.SensorArray[(self.sensorX - 1)].get():
                self.sensorX -= 1
                self.logicArray = []
        # Fires shooter:
<<<<<<< HEAD
        # if (
        #     self.shooterActivated and 
        #     all(self.logicArray) and 
        #     self.CurrentSensor.get()
        # ):
        #     self.Motors.stopLoader()
        #     self.Motors.runLoader(-1)

        #     if self.SensorArray[0].get():
        #         self.Motors.stopLoader()
        #         self.Motors.runShooter(1)

        #         if self.Motors.isShooterAtSpeed() == 1:
        #             self.Motors.runLoader(1)

        #             if all(self.logicArray) and self.SensorArray[0].get():
        #                 self.Motors.stopLoader()
        #                 self.Motors.stopShooter()
        #                 self.shooterActivated = False
=======
        if (
            self.initShooter and 
            all(self.logicArray) and 
            self.CurrentSensor.get()
        ):
            self.startShooter = True

        if self.startShooter:
            self.ShooterMotors.stopLoader()
            self.ShooterMotors.runLoader(-1)

            if self.SensorArray[0].get():
                self.ShooterMotors.stopLoader()
                self.ShooterMotors.runShooter(1)

                if self.ShooterMotors.isShooterAtSpeed() == 1:
                    self.ShooterMotors.runLoader(1)

                    if all(self.logicArray) and self.SensorArray[0].get():
                        self.ShooterMotors.stopLoader()
                        self.ShooterMotors.stopShooter()
                        self.initShooter = False
                        self.startShooter = False

# TODO: Add manual loading class if sensors don't work

class ManualControl:

    ShooterMotors: ShooterMotorCreation

    def __init__(self):
        self.shootSpeed = 0

    def RunLoader(self, loaderSpeed): # Intake handled by robot.py
        self.ShooterMotors.runLoader(loaderSpeed)

    def reverseLoader(self, reverseLoaderSpeed):
        self.ShooterMotors.runLoader(-reverseLoaderSpeed)

    def runShooter(self, shootActive):
        if shootActive:
            self.shootSpeed = 1

    def execute(self):
        self.ShooterMotors.runShooter(self.shootSpeed)
>>>>>>> f0e6b46dd53c459eb7cb02c9b6a767e9e49eadb3
