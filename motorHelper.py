# -*- coding: utf-8 -*-

import rev
import ctre

import logging
log = logging.getLogger("console") #These logs were set up for testing, should not be persistent, please delete if you see these and I forgot
log.setLevel(logging.DEBUG)

def createMotor(motorDescp, motors = {}):
    '''This is where all motors are set up'''
    if motorDescp['type'] == 'CANTalon':
        #if we want to use the built in encoder set it here
        if('pid' in motorDescp) and motorDescp['pid'] != None:
            motor = WPI_TalonFeedback(motorDescp)
            motor.setupPid()
        else:
            motor = ctre.WPI_TalonSRX(motorDescp['channel'])
        motors[str(motorDescp['channel'])] = motor

    elif motorDescp['type'] == 'CANTalonFollower':
        motor = ctre.WPI_TalonSRX(motorDescp['channel'])
        motor.set(mode = ctre.wpi_talonsrx.ControlMode.Follower, demand0 = motorDescp['masterChannel'])
        motors[str(motorDescp['channel'])] = motor

    elif motorDescp['type'] == 'SparkMax':
        '''This is where SparkMax motor controllers are set up'''
        if 'pid' in motorDescp and motorDescp['pid'] != None:
            motor = SparkMaxFeedback(motorDescp, motors)
            motor.setupPid()
        else:
            motor = SparkMaxFeedback(motorDescp, motors)
        motors[str(motorDescp['channel'])] = motor

    elif motorDescp['type'] == 'SparkMaxFollower':
        '''This is where SparkMax followers are set up
        For masterChannel, use a motor object. MASTER MUST BE A "CANSparkMax"  '''
        motor = SparkMaxFeedback(motorDescp, motors)
        motor.follow(motors.get(str(motorDescp['masterChannel'])), motorDescp['inverted'])

    else:
        log.error("Unknown Motor")

    if 'inverted' in motorDescp:
        motor.setInverted(motorDescp['inverted'])

    if 'currentLimits' in motorDescp:
        currentLimits = motorDescp['currentLimits']
        absMax = currentLimits['absMax']
        absMaxTimeMs = currentLimits['absMaxTimeMs']
        nominalMaxCurrent = currentLimits['maxNominal']
        motor.configPeakCurrentLimit(absMax,10)
        motor.configPeakCurrentDuration(absMaxTimeMs,10)
        motor.configContinuousCurrentLimit(nominalMaxCurrent,10)
        motor.enableCurrentLimit(True)

    #if 'rampRate' in motorDescp:
    #    motor.configOpenLoopRamp(motorDescp['rampRate'],10)

    return motor

class WPI_TalonFeedback(ctre.WPI_TalonSRX):#ctre.wpi_talonsrx.WPI_TalonSRX
    """
    Class used to setup TalonSRX motors if there are PID setting for it
    """
    def __init__(self, motorDescription):
        ctre.wpi_talonsrx.WPI_TalonSRX.__init__(self,motorDescription['channel'])
        self.motorDescription = motorDescription
        self.pid = None

    def setupPid(self,motorDescription = None):
        """
        Allows for the PID to be changed after its creation
        """
        if not motorDescription:
            motorDescription = self.motorDescription
        if not 'pid' in self.motorDescription:
            log.warning("Motor channel %d has no PID"%(self.motorDescription['channel']))
            return
        self.pid = self.motorDescription['pid']
        self.controlType = self.pid['controlType']
        self.configSelectedFeedbackSensor(self.pid['feedbackDevice'], 0, 10)
        self.setSensorPhase(self.pid['sensorPhase'])
        self.pidControlType = self.pid['controlType']

        self.kPreScale = self.pid['kPreScale']

        #/* set the peak, nominal outputs, and deadband */
        self.configNominalOutputForward(0, 10)
        self.configNominalOutputReverse(0, 10)
        self.configPeakOutputForward(1, 10)
        self.configPeakOutputReverse(-1, 10)


        self.configVelocityMeasurementPeriod(self.VelocityMeasPeriod.Period_1Ms,10)
        #/* set closed loop gains in slot0 */
        self.config_kF(0, self.pid['kF'], 10)
        self.config_kP(0, self.pid['kP'], 10)
        self.config_kI(0, self.pid['kI'], 10)
        self.config_kD(0, self.pid['kD'], 10)

    def set(self, speed):
        """
        Overrides the default set() to allow for controll using the pid loop
        """
        if self.pid != None:
            return ctre.wpi_talonsrx.WPI_TalonSRX.set(self, self.controlType, speed * self.kPreScale)
        else:
            return self.set(speed)

class SparkMaxFeedback(rev.CANSparkMax):
    """
    Class used to setup SparkMax motor if there are PID settings for it
    """
    def __init__(self, motorDescription, motors):
        self.motorDescription = motorDescription
        rev.CANSparkMax.__init__(self, self.motorDescription['channel'], self.motorDescription['motorType'])
        self.setInverted(self.motorDescription['inverted'])
        self.motors = motors

    def setupPid(self):
        '''Sets up the PIDF values and a pidcontroller to use to control the motor using pid.'''
        if not 'pid' in self.motorDescription:
            log.warning("Motor channel %f has no PID", (self.motorDescription['channel']))
            return
        self.pid = self.motorDescription['pid']
        pid = self.pid
        self.pidControlType = rev.ControlType(pid['controlType'])
        self.encoder = self.getEncoder()

        self.kPreScale = pid['kPreScale']
        self.PIDController = self.getPIDController() #creates pid controller

        self.PIDController.setP(pid['kP'], pid['feedbackDevice'])
        self.PIDController.setI(pid['kI'], pid['feedbackDevice'])
        self.PIDController.setD(pid['kD'], pid['feedbackDevice'])
        self.PIDController.setFF(pid['kF'], pid['feedbackDevice'])

        self.PIDController.setOutputRange(-1, 1, pid['feedbackDevice'])
        self.PIDController.setReference(0 , self.pidControlType, pid['feedbackDevice']) #Sets the control type to velocity on the pid slot we passed in

    def setControlType(self, type):
        '''Use the rev.ControlType.k(control type) as arg'''
        if isinstance(type, rev.ControlType):
            self.pidControlType = type
        else:
            log.debug("Wrong type. Use the rev.ControlType.k(control type)")

    def set(self, speed):
        """
        Overrides the default set() to allow for controll using the pid loop
        """
        if self.motorDescription['type'] != "SparkMaxFollower":
            log.debug("error = %f", (speed*self.pid['kPreScale'])-self.encoder.getVelocity())
            return self.PIDController.setReference(speed*self.pid['kPreScale'], self.pidControlType)
        return
