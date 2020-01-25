    # -*- coding: utf-8 -*-

import rev
import ctre 
import wpilib
import logging
log = logging.getLogger("console") #These logs were set up for testing, should not be persistent, please delete if you see these and I forgot
log.setLevel(logging.DEBUG)

def createMotor(motorDescp, motors = {}):
    #Might want more motor types for set up
    '''This is where all motors are set up'''
    motor = None
    if motorDescp['type'] == 'CANTalon':
        #if we want to use the built in encoder set it here
        if 'pid' in motorDescp and motorDescp['pid'] != None:
            if 'encoderSource' in motorDescp and motorDescp['encoderSource'] != None:
                motor = WPI_TalonFeedback(motorDescp)
                encoder = encoderFeedback(motorDescp, motor)
                motor.setEncoder(encoder)
            else:
                motor = WPI_TalonFeedback(motorDescp)
                motor.setupPid()
        else:
            motor = ctre.wpi_talonsrx.WPI_TalonSRX(motorDescp['channel'])

    elif motorDescp['type'] == 'CANTalonFollower':
        motor =ctre.wpi_talonsrx.WPI_TalonSRX(motorDescp['channel'])
        motor.set(mode = ctre.wpi_talonsrx.ControlMode.Follower, demand0 = motorDescp['masterChannel'])
        
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
        print("Unknown Motor")
    
    if 'inverted' in motorDescp and motor !=None: 
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

    if 'rampRate' in motorDescp:
        motor.configOpenLoopRamp(motorDescp['rampRate'],10)    
    
    return motor 

class encoderFeedback(object):
    def __init__(self, motorDescription, motor):
        self.motorDescp = motorDescription
        self.motor = motor
        print(self.motor)
        self.encoder = None
        if 'encoderSource' in motorDescription and motorDescription['encoderSource'] != None:
            self.encoder = motorDescription['encoderSource']
            print("Starting dist is: %f", self.encoder.get())
        self.pid = None
        if 'pid' in motorDescription and motorDescription['pid'] != None:
            self.pid = motorDescription['pid']
            self.PIDController = wpilib.PIDController(self.pid['kP'], self.pid['kI'], self.pid['kD'], self.encoder, self.motor)
            self.PIDController.setInputRange(-2048, 2048)
            self.PIDController.setOutputRange(-1, 1)
            self.PIDController.setPIDSourceType(self.pid['controlType'])
            self.PIDController.enable()
        else:
            log.debug("You NEED to pass in a pid array to use encoders. You haven't.")
    def set(self, speed):
        self.PIDController.setSetpoint(speed*self.pid['kPreScale'])
    def get(self):
        return self.PIDController.get()
    def getPos(self):
        return self.encoder.get()
    def getError(self):
        return self.PIDController.getError()
    def getRate(self):
        return self.encoder.getRate()

class WPI_TalonFeedback(ctre.wpi_talonsrx.WPI_TalonSRX):
    def __init__(self, motorDescription, encoder = None):
        ctre.wpi_talonsrx.WPI_TalonSRX.__init__(self,motorDescription['channel'])
        self.motorDescription = motorDescription
        self.pid = None
        self.encoder = encoder
        if 'pid' in self.motorDescription:
            self.pid = self.motorDescription['pid']

    def setEncoder(self, encoder):
        self.encoder = encoder
        
    def setupPid(self, motorDescription = None):
        if not motorDescription:
            motorDescription = self.motorDescription
        if not 'pid' in self.motorDescription:
            print("Motor channel %d has no PID"%(self.motorDescription['channel']))
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
        if self.pid != None and self.encoder == None:
            return ctre.wpi_talonsrx.WPI_TalonSRX.set(self, self.controlType, speed * self.kPreScale)
        elif self.encoder != None:
            self.encoder.set(speed)
            log.debug("Out: %f, Error: %f, speed: %f", self.encoder.get(), self.encoder.getRate()-(speed*self.pid['kPreScale']), speed)
            return ctre.wpi_talonsrx.WPI_TalonSRX.set(self, self.encoder.get())
        else:
            return ctre.wpi_talonsrx.WPI_TalonSRX.set(self, speed)

#class WPI_TalonFXFeedback(ctre.ta)
            
class SparkMaxFeedback(rev.CANSparkMax):
    def __init__(self, motorDescription, motors):
        self.motorDescription = motorDescription
        rev.CANSparkMax.__init__(self, self.motorDescription['channel'], self.motorDescription['motorType'])
        self.setInverted(self.motorDescription['inverted'])
        self.motors = motors

    def setupPid(self):
        '''Sets up the PIDF values and a pidcontroller to use to control the motor using pid.'''
        if not 'pid' in self.motorDescription:
            print("Motor channel %f has no PID", (self.motorDescription['channel']))
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
        if self.motorDescription['type'] != "SparkMaxFollower":
            log.debug("error = %f", (speed*self.pid['kPreScale'])-self.encoder.getVelocity())
            return self.PIDController.setReference(speed*self.pid['kPreScale'], self.pidControlType)
        return
