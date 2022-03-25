from robotMap import XboxMap
from components.Actuators.LowLevel.intakeMotor import IntakeMotor
from components.Actuators.HighLevel.hopperMotor import HopperMotor
from components.Input.breakSensors import Sensors, State
from components.Input.ballCounter import BallCounter
from components.Actuators.HighLevel.feederMap import FeederMap, Type
from components.Input.colorSensor import ColorSensor
from utils.DirectionEnums import Direction
from magicbot import StateMachine, state, timed_state, tunable, feedback

class LoaderLogic(StateMachine):
    """StateMachine-based loader. Has both automatic and manual modes."""
    compatString = ["teapot"]

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
    automaticHopperMotor2Speed = tunable(.6)
    # Other variables
    isAutomatic = True
    isAutonomous = False
    loaderStoppingDelay = .16
    ballEjectTime = .3
    eject = False

    def on_enable(self):
        self.isAutomatic = True

    def setAutoLoading(self):
        """Runs sensor-based loading."""
        self.isAutomatic = True
        self.next_state('checkForBall')

    def setIsAutonomous(self, isAutono:bool):
        """
        Sets whether the loader acts as if it's autonomous or not
        """
        self.isAutonomous = isAutono

    def setManualLoading(self):
        """Runs trigger-based loading."""
        self.isAutomatic = False
        self.next_state('runHopperManually')

    def stopLoading(self):
        if self.hopperMotor.isHopperForesideRunning() or self.hopperMotor.isHopperBacksideRunning():
            return
        self.next_state('nextAction')

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
        # ballCount = self.ballCounter.getBallCount()
        if self.sensors.loadingSensor(State.kTripped):
            self.next_state('checkEject')
        # if type(ballCount[0]) == Ball and ballCount[1] == None:
        #     self.hopperMotor.runHopperMotorForeside(self.hopperMotor.movingSpeed, Direction.kForwards)
        #     self.next_state('move_ball')

    @state
    def move_ball(self):
        """
        Moves the ball forewards, goes back so we can eject if need be
        """
        self.hopperMotor.runHopperMotorForeside(self.hopperMotor.movingSpeed, Direction.kForwards)
        self.hopperMotor.runHopperMotorBackside(self.hopperMotor.movingSpeed, Direction.kForwards)
        self.next_state('checkForBall')

    @state
    def checkEject(self):
        """
        If we're ejecting balls of the other team's color,
        makes sure that the ball is our color
        """
        self.next_state('nextAction')

        opposingColor = ""
        if self.allianceColor == "red":
            opposingColor = "blue"
        elif self.allianceColor == "blue":
            opposingColor = "red"

        if self.eject and self.colorSensor.displayColor() == opposingColor:
            self.next_state('eject_ball')
        else:
            self.next_state('nextAction')

    @timed_state(duration = ballEjectTime, next_state = 'nextAction')
    def eject_ball(self):
        """
        Runs the loader backwards for a set time
        """
        self.hopperMotor.runHopperMotorForeside(self.automaticHopperMotor1Speed, Direction.kBackwards)

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
        if not self.isAutonomous:
            self.runIntake()
        super().execute()
