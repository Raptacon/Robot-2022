from robotMap import XboxMap
from components.Actuators.LowLevel.intakeMotor import IntakeMotor
from components.Actuators.LowLevel.hopperMotor import HopperMotor
from components.Input.breakSensors import Sensors, State
from components.Actuators.HighLevel.feederMap import FeederMap, Type
from components.Input.colorSensor import ColorSensor
from wpilib import DriverStation
from utils.DirectionEnums import Direction
from magicbot import StateMachine, state, timed_state, tunable, feedback

class LoaderLogic(StateMachine):
    """StateMachine-based loader. Has both automatic and manual modes."""
    compatString = ["doof"]

    # Component/module related things
    intakeMotor: IntakeMotor
    hopperMotor: HopperMotor
    feeder: FeederMap
    sensors: Sensors
    xboxMap: XboxMap
    colorSensor: ColorSensor
    allianceColor: DriverStation.Alliance

    # Tunable
    automaticHopperMotor1Speed = tunable(.4)
    automaticHopperMotor2Speed = tunable(.4)
    # Other variables
    isAutomatic = True
    loaderStoppingDelay = .16
    ballEjectTime = .3
    eject = False

    def on_enable(self):
        self.isAutomatic = True

    def setAutoLoading(self):
        """Runs sensor-based loading."""
        self.isAutomatic = True
        self.next_state('checkForBall')

    def setManualLoading(self):
        """Runs trigger-based loading."""
        self.isAutomatic = False
        self.next_state('runHopperManually')

    def stopLoading(self):
        if self.hopperMotor.isHopper1Running or self.hopperMotor.isHopper2Running():
            return
        self.next_state('shooting')

    def determineNextAction(self):
        self.next_state('nextAction')

    def setEjectBall(self, boolEject: bool):
        self.eject = boolEject

    @feedback
    def isRunningAutomatic(self):
        return self.isAutomatic

    def runIntake(self):
        """Universal function for running the intake. Used in both manual and automatic."""
        self.feeder.run(Type.kIntake)

    @state
    def runHopperManually(self):
        """Trigger-based manual loader."""
        self.feeder.run(Type.kHopper)

    @state(first = True)
    def checkForBall(self):
        """Checks for ball to enter the loader, runs the loader if entry sensor is broken."""
        self.hopperMotor.stopHopperMotor1()
        self.hopperMotor.stopHopperMotor2()
        if self.sensors.loadingSensor(State.kTripped):
            self.next_state('waitForBallIntake')

    @state
    def waitForBallIntake(self):
        """Checks for intake to be completed."""
        if self.sensors.loadingSensor(State.kNotTripped) and self.eject == False:
            self.hopperMotor.runHopperMotor1(self.automaticHopperMotor1Speed, Direction.kForwards)
            self.next_state('stopBall')
        elif self.eject and ColorSensor.getColor() != self.allianceColor:
            self.hopperMotor.runHopperMotor1(self.automaticHopperMotor2Speed, Direction.kBackwards)
            self.next_state('eject_ball')
        if self.sensors.middleSensor(State.kTripped):
            self.hopperMotor.RunHopperMotor2(self.automaticHopperMotor1Speed, Direction.kForwards)
            self.hopperMotor.stopHopperMotor1()
            self.next_state('stopBall')

    @timed_state(duration = ballEjectTime, next_state = 'checkforBall')
    def eject_ball(self):
        """
        Runs the loader backwards for a set time
        """
        pass

    @timed_state(duration = loaderStoppingDelay, next_state = 'checkForBall')
    def stopBall(self):
        """Stops ball after a short delay."""
        pass

    @state
    def shooting(self):
        """While shooting, do nothing with the loader."""
        pass

    @state
    def nextAction(self):
        """Determine what to do after shooting."""
        if self.isAutomatic:
            self.next_state('checkForBall')
        elif not self.isAutomatic:
            self.next_state('runHopperManually')

    def execute(self):
        """Constantly runs state machine and intake. Necessary for function."""
        self.engage()
        self.runIntake()
        super().execute()
