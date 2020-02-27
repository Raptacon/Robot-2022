from wpilib import DigitalInput as dio
from time import sleep
from robotMap import XboxMap
from components.ShooterMotors import ShooterMotorCreation
from magicbot import StateMachine, state, default_state, tunable
import logging


class ShooterLogic(StateMachine):
    """
    State-machine based shooter
    """
    compatString = ["doof"]
    logger: logging
    shooterMotors: ShooterMotorCreation
    xboxMap: XboxMap
    loaderMotorVal = tunable(.4)
    intakeMotorMinVal = tunable(.5)
    intakeMotorMaxVal = tunable(.7)

    def on_enable(self):
        self.isAutomatic = False
        self.SensorArray = []
        self.sleepTime = 0

        # Creates sensors:
        for x in range(1, 6):
            self.sensorObjects = dio(x) # .get()
            self.SensorArray.append(self.sensorObjects)
            # NOTE: Sensor keys are different than dio value:
            # dio(1) >>> SensorArray[0]
            # dio(2) >>> SensorArray[1]
            # dio(3) >>> SensorArray[2]
            # dio(4) >>> SensorArray[3]
            # dio(5) >>> SensorArray[4]

        self.currentSensor = None

        # self.logger.setLevel(logging.DEBUG)

    def initManual(self):
        """Initializes manual control"""
        self.isAutomatic = False

    def startManual(self):
        """Starts manual control"""
        if not self.isAutomatic:
            self.done()
        else:
            pass

    def fireManualShooter(self):
        """Fires shooter manually"""
        if not self.isAutomatic:
            print("shooter running:")
            self.shooterMotors.runShooter(1)
        else:
            pass

    def initAutomatic(self):
        """Initializes automatic control"""
        self.isAutomatic = True

        # if all(self.SensorArray):
        #     self.isAutomatic = True
        # else:
        #     self.logger.info("Unable to enable automatic; ball(s) already loaded")
        #TODO: Need to add logic to prevent automatic switch if balls are loaded

    def startAutomatic(self):
        """Starts automatic control"""
        if self.isAutomatic:
            self.engage()

    def fireAutomaticShooter(self):
        """Fires shooter automatically"""
        if self.isAutomatic:
            self.next_state('setupShootAutomatically')

    # Beginning of manual
    @default_state # Run if self.engage() is not called
    def runManually(self):
        """Logic for running loader/intake manually"""
        if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
            self.shooterMotors.runLoader(self.loaderMotorVal)
            self.shooterMotors.runIntake((self.xboxMap.getMechRightTrig()*(self.intakeMotorMaxVal-self.intakeMotorMinVal))+self.intakeMotorMinVal)
            self.logger.debug("right trig manual", self.xboxMap.getMechRightTrig())

        elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
            self.shooterMotors.runLoader(-0.35)
            self.shooterMotors.runIntake(-((self.xboxMap.getMechRightTrig()*(self.intakeMotorMaxVal-self.intakeMotorMinVal))+self.intakeMotorMinVal))
            self.logger.debug("left trig manual", self.xboxMap.getMechLeftTrig())

        else:
            self.shooterMotors.stopIntake()
            self.shooterMotors.stopLoader()

    def runIntakeAutomatically(self):
        """Logic for running intake automatically"""
        if self.isAutomatic:
            if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
                self.shooterMotors.runIntake((self.xboxMap.getMechRightTrig()*(self.intakeMotorMaxVal-self.intakeMotorMinVal))+self.intakeMotorMinVal)
                self.logger.debug("right trig automatic", self.xboxMap.getMechRightTrig())

            elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
                self.shooterMotors.runIntake(-((self.xboxMap.getMechRightTrig()*(self.intakeMotorMaxVal-self.intakeMotorMinVal))+self.intakeMotorMinVal))
                self.logger.debug("left trig automatic", self.xboxMap.getMechLeftTrig())

            else:
                self.shooterMotors.stopIntake()
        
        elif not self.isAutomatic:
            pass

    # Beginning of automatic
    @state(first = True) # Run if self.engage() is called
    def runLoaderAutomatically(self):
        """Instantiates automatic loading"""
        self.next_state('autoLoading')

    @state
    def autoLoading(self, state_tm):
        """Logic for running loader automatically"""
        loaderSensor = 4
        if not self.SensorArray[loaderSensor].get() and self.SensorArray[0].get():
            self.shooterMotors.runLoader(self.loaderMotorVal)
            self.sleepTime = .25

        elif not self.SensorArray[loaderSensor].get() and not self.SensorArray[0].get():
            self.shooterMotors.runLoader(self.loaderMotorVal)
            self.sleepTime = 0
            print("loader run final")

        if self.SensorArray[loaderSensor].get():
            sleep(self.sleepTime)
            self.shooterMotors.stopLoader()
            self.sleepTime = 0

    @state
    def setupShootAutomatically(self):
        """Predecessor to automatic shooting"""
        if not self.SensorArray[0].get():
            self.shooterMotors.runLoader(-.3)

        elif self.SensorArray[0].get():
            self.shooterMotors.stopLoader()
            self.next_state('shootAutomatically')

    @state(must_finish = True) # Potentially change to timed_state?
    def shootAutomatically(self, state_tm):
        """Execute shoot automatically"""
        self.shooterMotors.runShooter(1)
        self.logger.debug("running auto shooter")
        if state_tm > 1:
            self.shooterMotors.runLoader(self.loaderMotorVal)
            if state_tm > 4:
                self.shooterMotors.stopLoader()
                self.shooterMotors.stopShooter()
                self.currentSensor = 3
                self.done()
