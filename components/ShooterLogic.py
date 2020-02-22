from wpilib import DigitalInput as dio
from robotMap import XboxMap
from components.ShooterMotors import ShooterMotorCreation
from magicbot import StateMachine, state, tunable


class ManualShooter:

    shooterMotors: ShooterMotorCreation
    xboxMap: XboxMap
    loaderMulti = tunable(.4)
    intakeMin = tunable(.5)
    intakeMax = tunable(.7)

    def __init__(self):
        self.isAutomatic = False

    def runLoaderManually(self):
        self.isAutomatic = False

    def getAutomaticStatus(self):
        return self.isAutomatic

    def stopManual(self):
        self.isAutomatic = True

    def fireShooter(self):
        self.shooterMotors.stopIntake()
        self.shooterMotors.stopLoader()
        print("manual shooter running")
        self.shooterMotors.runShooter(1)
        if self.shooterMotors.shooterMotor.getEncoder().getVelocity() >= 5000:
            self.shooterMotors.runLoader(1 * self.loaderMulti)

    def execute(self):
        if not self.isAutomatic:
            if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
                self.shooterMotors.runLoader(0.6 * self.loaderMulti)
                self.shooterMotors.runIntake((self.xboxMap.getMechRightTrig()*(self.intakeMax-self.intakeMin))+self.intakeMin)
                print("right trig manual", self.xboxMap.getMechRightTrig())

            elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
                self.shooterMotors.runLoader(-0.2)
                self.shooterMotors.runIntake(-((self.xboxMap.getMechRightTrig()*(self.intakeMax-self.intakeMin))+self.intakeMin))
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
    loaderMulti = tunable(.4)
    intakeMin = tunable(.5)
    intakeMax = tunable(.7)

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

    def getAutomaticStatus(self):
        return self.isAutomatic
    
    def stopAutomatic(self):
        self.isAutomatic = False

    def initAutoLoading(self):
        if self.isAutomatic:
            self.engage()
        elif self.isAutomatic == False:
            pass

    def switchToReverse(self):
        if all(self.logicArray):
            self.next_state_now('reverseShooting')

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
            self.shooterMotors.runIntake((self.xboxMap.getMechRightTrig()*(self.intakeMax-self.intakeMin))+self.intakeMin)
            print("right trig automatic:", self.xboxMap.getMechRightTrig())

        elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
            self.shooterMotors.runIntake(-((self.xboxMap.getMechRightTrig()*(self.intakeMax-self.intakeMin))+self.intakeMin))
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
            self.shooterMotors.runLoader(1 * self.loaderMulti)
            self.logicArray = []

        # If one ball has reached loader sensor:
        elif self.CurrentSensor.get() == False and all(self.logicArray):
            self.shooterMotors.stopLoader()
            self.sensorX += 1
            self.logicArray = []

        # If more than one ball is loaded:
        elif self.CurrentSensor.get() == False and all(self.logicArray) == False:
            self.shooterMotors.runLoader(0.6 * self.loaderMulti)
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

    @state
    def reverseShooting(self, state_tm):
        if not self.SensorArray[0].get():
            self.shooterMotors.runLoader(-0.6 * self.loaderMulti)
            self.next_state_now('runShooterMotor')

        elif state_tm > 3:
            self.done()

    @state
    def runShooterMotor(self, state_tm):
        if self.SensorArray[0].get():
            self.shooterMotors.stopLoader()
            self.shooterMotors.runShooter(1)
            if self.shooterMotors.shooterMotor.getEncoder().getVelocity() >= 5000 or state_tm > 3:
                self.next_state_now('shoot')

    @state
    def shoot(self, state_tm):
        self.shooterMotors.runLoader(0.6 * self.loaderMulti)
        if state_tm > 6:
            self.shooterMotors.stopLoader()
            self.next_state_now('beginLoading')
