from wpilib import DigitalInput as dio
from wpilib import XboxController
from robotMap import XboxMap
from components.ShooterMotors import ShooterMotorCreation
from magicbot import StateMachine, state, tunable


class ManualShooter:

    ShooterMotors: ShooterMotorCreation
    xboxMap: XboxMap

    def __init__(self):
        self.isAutomatic = False

    def runLoaderManually(self):
        self.isAutomatic = False

    def getAutomaticStatus(self):
        return self.isAutomatic

    def stopManual(self):
        self.isAutomatic = True

    def fireShooter(self):
        self.ShooterMotors.stopIntake()
        self.ShooterMotors.stopLoader()
        print("manual shooter running")
        self.ShooterMotors.runShooter(1)
        if self.ShooterMotors.shooterMotor.getEncoder().getVelocity() >= 5000:
            self.ShooterMotors.runLoader(1)

    def execute(self):
        if not self.isAutomatic:
            if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
                self.max = .7
                self.min = .5
                self.ShooterMotors.runLoader(.6*.4)
                self.ShooterMotors.runIntake((self.xboxMap.getMechRightTrig()*(self.max-self.min))+self.min)
                print("right trig manual", self.xboxMap.getMechRightTrig())

            elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
                self.max = .9
                self.min = .5
                self.ShooterMotors.runLoader(-.2)
                self.ShooterMotors.runIntake(-((self.xboxMap.getMechRightTrig()*(self.max-self.min))+self.min))
                print("left trig manual", self.xboxMap.getMechLeftTrig())

            elif self.xboxMap.getMechAButton():
                self.fireShooter()

            else:
                self.ShooterMotors.stopIntake()
                self.ShooterMotors.stopLoader()
                self.ShooterMotors.stopShooter()
        
        elif self.isAutomatic:
            pass

class AutomaticShooter(StateMachine):

    ShooterMotors: ShooterMotorCreation
    sensorObjects: dio
    xboxMap: XboxMap

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
            self.ShooterMotors.runIntake(self.xboxMap.getMechRightTrig()*.6)
            self.max = .7
            self.min = .5
            self.ShooterMotors.runIntake((self.xboxMap.getMechRightTrig()*(self.max-self.min))+self.min)
            print("right trig automatic:", self.xboxMap.getMechRightTrig())

        elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
            self.max = .9
            self.min = .5
            self.ShooterMotors.runLoader(-.2)
            self.ShooterMotors.runIntake(-((self.xboxMap.getMechRightTrig()*(self.max-self.min))+self.min))
            print("left trig automatic:", self.xboxMap.getMechLeftTrig())

        else:
            self.ShooterMotors.stopIntake()

        '''
        Creates the basis for the logic regarding when the loader is run.
        Checks boolean values all sensors aside from current sensor, and
        runs loader appropriately in if-elif-else chain:
        '''
        # NOTE: After every control loop, the logicArray MUST be reset
        # If one ball is loaded:
        if (
            self.CurrentSensor.get() and
            all(self.logicArray) == False
        ):
            self.ShooterMotors.runLoader(1*.4)
            self.logicArray = []

        # If one ball has reached loader sensor:
        elif self.CurrentSensor.get() == False and all(self.logicArray):
            self.ShooterMotors.stopLoader()
            self.sensorX += 1
            self.logicArray = []

        # If more than one ball is loaded:
        elif self.CurrentSensor.get() == False and all(self.logicArray) == False:
            self.ShooterMotors.runLoader(1*.4)
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

        if self.xboxMap.getMechAButton() and all(self.logicArray):
            self.next_state_now('reverseShooting')

    @state
    def reverseShooting(self, state_tm):
        if not self.SensorArray[0].get():
            self.ShooterMotors.runLoader(-1*.4)
            self.next_state_now('runShooterMotor')

        elif state_tm > 2:
            self.done()

    @state
    def runShooterMotor(self, state_tm):
        if self.SensorArray[0].get():
            self.ShooterMotors.stopLoader()
            self.ShooterMotors.runShooter(1)
            if self.ShooterMotors.shooterMotor.getEncoder().getVelocity() >= 5000 or state_tm > 3:
                self.next_state_now('shoot')

    @state
    def shoot(self, state_tm):
        self.ShooterMotors.runLoader(1*.4)
        if state_tm > 4:
            self.ShooterMotors.stopLoader()
            self.next_state_now('beginLoading')
