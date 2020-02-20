from wpilib import DigitalInput as dio
from wpilib import XboxController
from robotMap import XboxMap
from components.ShooterMotors import ShooterMotorCreation

class shooterLogic:

    ShooterMotors: ShooterMotorCreation
    sensorObjects: dio
    xboxMap: XboxMap

    def __init__(self):

        # Basic init:
        self.CurrentSensor = None
        self.logicSensors = None
        self.initShooter = False
        self.startShooter = False
        self.isAutomatic = False
        self.runningShooter = False

        # Arrays for sensors/logic-based sensors:
        self.logicArray = []
        self.SensorArray = []

        # Key for sensors in 'self.SensorArray' array:
        self.sensorX = 0

        # Creates sensors:
        for x in range(1, 6):
            self.sensorObjects = dio(x)
            self.SensorArray.append(self.sensorObjects)

    def fireShooterSensor(self):
        self.ShooterMotors.runLoader(-0.8)
        if self.SensorArray[0].get():
            self.ShooterMotors.runShooter(.9)
            if self.ShooterMotors.shooterMotor.getEncoder().getVelocity() >= 3500:
                self.ShooterMotors.runLoader(0.2)
                if all(self.SensorArray[self.sensorX].get()):
                    self.ShooterMotors.stopLoader()

    def fireShooter(self):
        self.runningShooter = True
        self.ShooterMotors.runShooter(0.9)
        print("shooter firing, velocity : ", self.ShooterMotors.shooterMotor.getEncoder().getVelocity())
        if self.ShooterMotors.shooterMotor.getEncoder().getVelocity() >= 3500:
            self.ShooterMotors.runLoader(1)


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
            if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
                self.ShooterMotors.runLoader(self.xboxMap.getMechRightTrig())
                self.ShooterMotors.runIntake(self.xboxMap.getMechRightTrig())
                print("right trig", self.xboxMap.getMechRightTrig())
            elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
                self.ShooterMotors.runLoader(-self.xboxMap.getMechLeftTrig())
                self.ShooterMotors.runIntake(-self.xboxMap.getMechLeftTrig())
                print("left trig", self.xboxMap.getMechLeftTrig())
            elif not self.runningShooter:
                self.ShooterMotors.runIntake(0)
                self.ShooterMotors.runLoader(0)

            #TODO: Look at drive station for proper inversions of variables
