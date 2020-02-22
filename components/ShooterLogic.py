from wpilib import DigitalInput as dio
from robotMap import XboxMap
from components.ShooterMotors import ShooterMotorCreation
from magicbot import StateMachine, state, tunable


class ManualShooter:

    shooterMotors: ShooterMotorCreation
    xboxMap: XboxMap
    loaderMotorVal = tunable(.24)
    intakeMotorMinVal = tunable(.5)
    intakeMotorMaxVal = tunable(.7)

    def __init__(self):
        self.isAutomatic = False

    def runLoaderManually(self):
        self.isAutomatic = False

    def stopManual(self):
        self.isAutomatic = True

    # Checks if bot is running loader automatically
    def getAutomaticStatus(self):
        return self.isAutomatic

    def fireShooter(self):
        if not self.isAutomatic:
            self.shooterMotors.stopIntake()
            self.shooterMotors.stopLoader()
            print("manual shooter running")
            self.shooterMotors.runShooter(1)
            if self.shooterMotors.shooterMotor.getEncoder().getVelocity() >= 5000:
                self.shooterMotors.runLoader(self.loaderMotorVal)

        elif self.isAutomatic:
            pass

    def execute(self):
        if not self.isAutomatic:
            if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
                self.shooterMotors.runLoader(self.loaderMotorVal)
                self.shooterMotors.runIntake((self.xboxMap.getMechRightTrig()*(self.intakeMotorMaxVal-self.intakeMotorMinVal))+self.intakeMotorMinVal)
                print("right trig manual", self.xboxMap.getMechRightTrig())

            elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
                self.shooterMotors.runLoader(-0.2)
                self.shooterMotors.runIntake(-((self.xboxMap.getMechRightTrig()*(self.intakeMotorMaxVal-self.intakeMotorMinVal))+self.intakeMotorMinVal))
                print("left trig manual", self.xboxMap.getMechLeftTrig())

            else:
                self.shooterMotors.stopIntake()
                self.shooterMotors.stopLoader()
                self.shooterMotors.stopShooter()
        
        elif self.isAutomatic:
            pass

class AutomaticShooter(StateMachine):

    shooterMotors: ShooterMotorCreation
    sensorObjects: dio
    xboxMap: XboxMap
    loaderMotorVal = tunable(.4)
    intakeMotorMinVal = tunable(.5)
    intakeMotorMaxVal = tunable(.7)

    def __init__(self):

        # Basic init:
        self.CurrentSensor = None
        self.logicSensors = None
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

    def runLoaderAutomatically(self):
        self.isAutomatic = True

    def stopAutomatic(self):
        self.isAutomatic = False

    # Checks if bot is running loader automatically
    def getAutomaticStatus(self):
        return self.isAutomatic

    def initAutoLoading(self):
        if self.isAutomatic:
            self.engage()
        elif self.isAutomatic == False:
            pass

    @state(first = True)
    def beginLoading(self):
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

        if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
            self.shooterMotors.runIntake(self.xboxMap.getMechRightTrig()*.6)
            self.shooterMotors.runIntake((self.xboxMap.getMechRightTrig()*(self.intakeMotorMaxVal-self.intakeMotorMinVal))+self.intakeMotorMinVal)
            print("right trig automatic:", self.xboxMap.getMechRightTrig())

        elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
            self.shooterMotors.runIntake(-((self.xboxMap.getMechRightTrig()*(self.intakeMotorMaxVal-self.intakeMotorMinVal))+self.intakeMotorMinVal))
            print("left trig automatic:", self.xboxMap.getMechLeftTrig())

        else:
            self.shooterMotors.stopIntake()

        '''
        Creates the basis for the logic regarding when the loader is run.
        Checks boolean values all sensors aside from current sensor, and
        runs loader appropriately in if-elif-else chain:
        '''
        # NOTE: After every control loop, the logicArray MUST be reset
        # If one ball is loaded:
        if (
            self.CurrentSensor.get() and all(self.logicArray) == False
        ):
            self.shooterMotors.runLoader(self.loaderMotorVal)
            self.logicArray = []

        # If one ball has reached loader sensor:
        elif self.CurrentSensor.get() == False and all(self.logicArray):
            self.shooterMotors.stopLoader()
            self.sensorX += 1
            self.logicArray = []

        # If more than one ball is loaded:
        elif self.CurrentSensor.get() == False and all(self.logicArray) == False:
            self.shooterMotors.runLoader(self.loaderMotorVal)
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

    def initAutoShooting(self):
        if self.isAutomatic:
            # If first sensor is broken and loader is not running:
            if not self.SensorArray[0].get() and not self.shooterMotors.isLoaderActive():
                self.next_state('reverseShooting')

    @state
    def reverseShooting(self, state_tm):
        self.shooterMotors.runLoader(-self.loaderMotorVal)
        self.next_state('runShooterMotor')

    @state
    def runShooterMotor(self, state_tm):
        if self.SensorArray[0].get():
            self.shooterMotors.stopLoader()
            self.shooterMotors.runShooter(1)
            if self.shooterMotors.shooterMotor.getEncoder().getVelocity() >= 5000 or state_tm > 5:
                self.next_state('shoot')

    @state
    def shoot(self, state_tm):
        self.shooterMotors.runLoader(self.loaderMotorVal)
        if state_tm > 6:
            self.shooterMotors.stopLoader()
            self.next_state('beginLoading')
