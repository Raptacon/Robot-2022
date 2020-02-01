#
# See the notes for the other physics sample
#


from pyfrc.physics import drivetrains


class PhysicsEngine(object):
    '''
    Simulates a 4-wheel mecanum robot using Tank Drive joystick control
    '''

    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.Physics` object
        to communicate simulation effects to
        '''

        self.physics_controller = physics_controller


    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.

            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''

        # Simulate the drivetrain
        # -> Remember, in the constructor we inverted the left motors, so
        #    invert the motor values here too!
        try:

            if hal_data['CAN'][1]['inverted']:
                l_motor = -hal_data['CAN'][1]['value']
            else:
                l_motor = hal_data['CAN'][1]['value']

            if hal_data['CAN'][0]['inverted']:
                r_motor = -hal_data['CAN'][0]['value']
            else:
                r_motor = hal_data['CAN'][0]['value']

            tm_diff = tm_diff * 0.5
            speed,rot = drivetrains.two_motor_drivetrain(l_motor,r_motor)
            self.physics_controller.drive(speed,rot, tm_diff)
        except:
            l_motor = r_motor = 0
            self.physics_controller.drive(0,0, tm_diff)

        #print(hal_data['joysticks'])
        #.mecanum_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor,speed = 0.01)
