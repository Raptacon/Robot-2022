from wpilib import DigitalInput as dio
from wpilib import XboxController
from components.ShooterMotors import ShooterMotorCreation
from robotMap import XboxMap

class ShooterLogic:

    ShooterMotors: ShooterMotorCreation
    sensorObjects: dio

    def __init__(self):

        # Basic init:
        self.XboxMap = XboxMap(XboxController(0), XboxController(1))
        self.CurrentSensor = None
        self.logicSensors = None
        self.initShooter = False
        self.startShooter = False
        self.isAutomatic = False

        # Arrays for sensors/logic-based sensors:
        self.logicArray = []
        self.SensorArray = []

        # Key for sensors in 'self.SensorArray' array:
        self.sensorX = 0

        # Creates sensors:
        for x in range(1, 6):
            self.sensorObjects = dio(x)
            self.SensorArray.append(self.sensorObjects)

    def fireShooter(self):
        self.ShooterMotors.runLoader(-0.8)
        if self.SensorArray[0].get():
            self.ShooterMotors.runShooter(.9)
            if self.ShooterMotors.shooterMotor.getEncoder().getVelocity() >= 3500:
                self.ShooterMotors.runLoader(0.2)
                if all(self.SensorArray[self.sensorX].get()):
                    self.ShooterMotors.stopLoader()

    def runLoaderAutomatically(self):
        self.isAutomatic = True

    def runLoaderManually(self):
        self.isAutomatic = False

    def execute(self):
        # Checks if driver wants automatic loading:
        if self.isAutomatic:
            # Assert that key called exists
            try:
                assert(self.sensorX >= 0 and self.sensorX >= 4)
            except AssertionError as err:
                print("Failed to get sensor key in range:", err)

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

            # Shifts loader responsibility:
            elif self.SensorArray[(self.sensorX - 1)].get():
                self.sensorX -= 1
                self.logicArray = []

            # Intake has no ball:
            else:
                self.logicArray = []

        elif self.isAutomatic == False:
            self.ShooterMotors.runLoader(self.XboxMap.getMechRightTrig())
            self.ShooterMotors.runIntake(self.XboxMap.getMechRightTrig())
            self.ShooterMotors.runLoader(self.XboxMap.getMechLeftTrig())
            self.ShooterMotors.runIntake(self.XboxMap.getMechLeftTrig())

            if self.XboxMap.getMechAButton():
                self.ShooterMotors.runShooter(0.9)
            elif self.XboxMap.getMechBButton():
                self.ShooterMotors.runShooter(0)

            #TODO: Look at drive station for proper inversions of variables

        else:
            pass
