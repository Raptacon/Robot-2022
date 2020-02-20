from wpilib import DigitalInput as dio
from wpilib import XboxController
from robotMap import XboxMap
from components.ShooterMotors import ShooterMotorCreation
from magicbot import StateMachine, state

class ManualShooter:

    ShooterMotors: ShooterMotorCreation

class AutomaticShooter(StateMachine):

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

    def fireShooter(self):
        self.ShooterMotors.stopIntake()
        self.ShooterMotors.stopLoader()
        print("manual shooter running")
        self.ShooterMotors.runShooter(1)
        if self.ShooterMotors.shooterMotor.getEncoder().getVelocity() >= 5000:
            self.ShooterMotors.runLoader(1)

    def fireShooterSensor(self):
        if self.SensorArray[0].get() == False:
            self.ShooterMotors.runLoader(-1)
            print("reverse loader")
        elif self.SensorArray[0].get():
            self.ShooterMotors.stopLoader()
            self.ShooterMotors.runShooter(1)
            print("automatic shooter running")
        if self.ShooterMotors.shooterMotor.getEncoder().getVelocity() >= 5000:
            self.ShooterMotors.runLoader(1)
        if self.CurrentSensor.get(): #FIXME: prevents reverse loader
            # self.ShooterMotors.stopLoader()
            # self.ShooterMotors.stopShooter()
            pass

    def runLoaderAutomatically(self):
        self.isAutomatic = True

    def runLoaderManually(self):
        self.isAutomatic = False

    def execute(self):
        # Checks if driver wants automatic loading:
        if self.isAutomatic:
            # Assert that key called exists
            try:
                assert(self.sensorX >= 0 and self.sensorX <= 4)
            except AssertionError as err:
                print("Failed to get sensor key in range:", err)

            # Sets the current sensor:
            self.CurrentSensor = self.SensorArray[self.sensorX]

            # Creats sensor logic array:
            for x in range((self.sensorX + 1), 5):
                self.logicSensors = self.SensorArray[x].get()
                self.logicArray.append(self.logicSensors)

            # NOTE: After every control loop, the logicArray MUST be reset

            if self.xboxMap.getMechRightTrig() and self.xboxMap.getMechLeftTrig() == 0:
                self.ShooterMotors.runIntake(self.xboxMap.getMechRightTrig())
                print("right trig automatic:", self.xboxMap.getMechRightTrig())

            elif self.xboxMap.getMechLeftTrig() and self.xboxMap.getMechRightTrig() == 0:
                self.ShooterMotors.runIntake(-self.xboxMap.getMechLeftTrig())
                print("left trig automatic:", self.xboxMap.getMechLeftTrig())

            else:
                self.ShooterMotors.stopIntake()

            if self.xboxMap.getMechAButton():
                self.fireShooterSensor()

            else:
                self.ShooterMotors.stopLoader()
                self.ShooterMotors.stopShooter()

            '''
            Creates the basis for the logic regarding when the loader is run.
            Checks boolean values all sensors aside from current sensor, and
            runs loader appropriately in if-elif-else chain:
            '''
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
            elif self.sensorX > 0:
                if self.SensorArray[(self.sensorX - 1)].get():
                    self.sensorX -= 1
                    self.logicArray = []

            # Intake has no ball:
            else:
                self.logicArray = []

        elif self.isAutomatic == False:

            if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
                self.ShooterMotors.runLoader(self.xboxMap.getMechRightTrig())
                self.ShooterMotors.runIntake(self.xboxMap.getMechRightTrig())
                print("right trig manual", self.xboxMap.getMechRightTrig())

            elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
                self.ShooterMotors.runLoader(-self.xboxMap.getMechLeftTrig())
                self.ShooterMotors.runIntake(-self.xboxMap.getMechLeftTrig())
                print("left trig manual", self.xboxMap.getMechLeftTrig())

            elif self.xboxMap.getMechAButton():
                self.fireShooter()

            else: #elif not self.runningShooter:
                self.ShooterMotors.stopIntake()
                self.ShooterMotors.stopLoader()
                self.ShooterMotors.stopShooter()
