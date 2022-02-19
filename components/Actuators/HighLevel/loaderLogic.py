from robotMap import XboxMap
from components.Actuators.LowLevel.intakeMotor import IntakeMotor
from components.Actuators.HighLevel.hopperMotor import HopperMotor
from components.Input.breakSensors import Sensors, State
from components.Input.ballCounter import BallCounter
from components.Actuators.HighLevel.feederMap import FeederMap, Type
from components.Input.colorSensor import ColorSensor
from wpilib import DriverStation
from utils.DirectionEnums import Direction
from magicbot import StateMachine, state, timed_state, tunable, feedback

class LoaderLogic(StateMachine):
    """StateMachine-based loader. Has both automatic and manual modes."""
    compatString = ["doof", "teapot"]

    # Component/module related things
    intakeMotor: IntakeMotor
    hopperMotor: HopperMotor
    feeder: FeederMap
    sensors: Sensors
    ballCounter: BallCounter
    xboxMap: XboxMap
    colorSensor: ColorSensor
    allianceColor: str

    # Tunable
    automaticHopperMotor1Speed = tunable(.4)
    automaticHopperMotor2Speed = tunable(.4)
    # Other variables
    isAutomatic = True
    loaderStoppingDelay = .16
    ballEjectTime = .3
    eject = True

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
        if self.hopperMotor.isHopper1Running() or self.hopperMotor.isHopper2Running():
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

    @state
    def checkForBall(self):
        """Checks for ball to enter the loader, runs the loader if entry sensor is broken."""
        if self.sensors.loadingSensor(State.kTripped):
            self.next_state('checkEject')
        if self.ballCounter.getBallCount() == [1, 0]:
            self.next_state('move_ball')

    @state
    def move_ball(self):
        ballArr = self.ballCounter.getBallCount()
        movingSpeed = self.hopperMotor.movingSpeed
        self.hopperMotor.runHopperMotor1(movingSpeed, Direction.kForwards)
        if ballArr[1] == 1:
            self.next_state('checkForBall')
        else:
            self.next_state('move_ball')

    @state
    def checkEject(self):
        """
        If we're ejecting balls of the other team's color,
        makes sure that the ball is our color
        """
        self.next_state('checkForBall')

        opposingColor = ""
        if self.allianceColor == "red":
            opposingColor = "blue"
        elif self.allianceColor == "blue":
            opposingColor = "red"

        if self.eject and self.colorSensor.displayColor() == opposingColor:
            self.hopperMotor.runHopperMotor1(self.automaticHopperMotor2Speed, Direction.kBackwards)
            self.next_state('eject_ball')

    @timed_state(duration = ballEjectTime, next_state = 'checkForBall')
    def eject_ball(self):
        """
        Runs the loader backwards for a set time
        """
        pass

    @state(first = True)
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
