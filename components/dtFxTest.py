import ctre


class DtFxTest:
    '''
        Tests DT with Talon FX
    '''

    def setup(self):
        """Init for Talon Fx"""
        self.fx = False
        
        if self.fx:
            self.dt_leftM = ctre.WPI_TalonFX(30)
            self.dt_leftF = ctre.WPI_TalonFX(31)
            self.dt_leftF.set(ctre.ControlMode.Follower, 30)
            self.dt_rightM = ctre.WPI_TalonFX(40)
            self.dt_rightF = ctre.WPI_TalonFX(41)
            self.dt_rightF.set(ctre.ControlMode.Follower, 40)
            self.dt_leftF.setInverted(True)
        else:
            self.dt_leftM = ctre.WPI_TalonSRX(0)
            self.dt_rightM = ctre.WPI_TalonSRX(1)

        self.dt_leftM.setInverted(True)
        
        self.reset()

    def on_enable(self):
        self.logger.info("Enabling")
        self.reset()
    
    def reset(self):
        """
        Resets internal state
        """
        self.leftSpeed = 0.0
        self.rightSpeed = 0.0
    
    def move(self, leftSp=0.0, rightSp=0.0, bothSp = None):
        """
        Sets left and right movement
        """
        #print("move", leftSp, rightSp, bothSp)
        if bothSp:
            print("Both speed", bothSp)
            leftSp = rightSp = bothSp

        self.leftSpeed = leftSp
        self.rightSpeed = rightSp

    def execute(self):
        """
        Sets motor power based on inputs
        """
        #self.logger.info("Left %f Right %f", self.leftSpeed, self.rightSpeed)
        self.dt_leftM.set(self.leftSpeed)
        #self.leftf.set(left)
        self.dt_rightM.set(self.rightSpeed)
        #self.rightf.set(right)
        #self.reset()

