# """
# This file defines constants related to your robot.  These constants include:

#  * Physical constants (exterior dimensions, wheelbase)

#  * Mechanical constants (gear reduction ratios)

#  * Electrical constants (current limits, CAN bus IDs, roboRIO slot numbers)

#  * Operation constants (desired max velocity, max turning speed)

#  * Software constants (USB ID for driver joystick)
# """

import math
from collections import namedtuple
import phoenix6

#Unit Conversions
cvr_data = {
    "meterPerInch": 0.0254
}
CVR = namedtuple("Data", cvr_data.keys())(**cvr_data)

# Physical constants
phys_data = {
    #Numbers are in inches
    "track_width_in_inch": 23.0,
    "wheel_base_in_inch": 23.0,
    "wheel_circumference_in_inch": 4 * math.pi
}
PHYS = namedtuple("Data", phys_data.keys())(**phys_data)

# Mechanical constants
mech_data = {
    "swerve_module_driving_gearing_ratio": 6.75,  # SDS Mk4i L2
    "swerve_module_steering_gearing_ratio": 150 / 7,  # SDS Mk4i

    "driving_motor_inverted": False,
    "steering_motor_inverted": True,
}
MECH = namedtuple("Data", mech_data.keys())(**mech_data)

# Electrical constants
elec_data = {

    #SwerveDrive
    "RF_steer_CAN_ID": 15,
    "RF_drive_CAN_ID": 1,
    "RF_encoder_DIO": 2,
    "RB_steer_CAN_ID": 2,
    "RB_drive_CAN_ID": 3,
    "RB_encoder_DIO": 3,
    "LB_steer_CAN_ID": 4,
    "LB_drive_CAN_ID": 5,
    "LB_encoder_DIO": 4,
    "LF_steer_CAN_ID": 6,
    "LF_drive_CAN_ID": 7,
    "LF_encoder_DIO": 1,  

    #Wrist
    "wrist_motor_CAN_ID": 1,

}
ELEC = namedtuple("Data", elec_data.keys())(**elec_data)

# Operation constants
op_data = {
    #Driver/Operator's controllers
    "driver_controller": 0,
    "operator_controller": 1,

    # These maximum parameters reflect the maximum physically possible, not the
    # desired maximum limit.
    # "max_speed": 4.5 * (u.m / u.s),
    # "max_angular_velocity": 11.5 * (u.rad / u.s),

    # # You can limit how fast your robot moves (e.g. during testing) using the
    # # following parameters.  Setting to None is the same as setting to
    # # max_speed/max_angular_velocity, and indicates no limit.
    # #
    # "speed_limit": 4.0 * (u.m / u.s),
    # "angular_velocity_limit": 8.0 * (u.rad / u.s),

    # 0 is coast, 1 is brake
    "driveMotor_neutral": 1,
    "steerMotor_neutral": 1,

}
OP = namedtuple("Data", op_data.keys())(**op_data)

# Software constants
sw_data = {
    # field_relative: True if "forward" means "down the field"; False if
    # "forward" means "in the direction the robot is facing".  A True value
    # requires a (non-Dummy) gyro.
    "field_relative": True,

    # drive_open_loop: True if we're not using PID control *for velocity targeting*,
    # i.e. when a target velocity is calculated, do we use the corresponding
    # CoaxialDriveComponent's follow_velocity_open() method (set motor output
    # proportionally based on target and max velocities) or
    # follow_velocity_closed() method (put motor in PID control mode and set
    # target velocity).
    #
    "drive_open_loop": True,

    # "Zero" (front-facing) positions, as read from the four encoders
	# NOTE: when facing wheels "front", make sure that the bevel gears are all
	# facing right.  Otherwise the wheel will run in reverse!
	#
	"lf_enc_zeropos":  9.7,
	"rf_enc_zeropos":  1.5,
	"lb_enc_zeropos":  93.7,
	"rb_enc_zeropos":  -35.0,

    # Constants for PID control of the propulsion AND steering motors
    # (kP must be non-zero, or azimuth motors won't engage.)
    #"kP": 0.3,  # representative value for Falcon500 motors
    "kP": 0.01,   # representative value for NEO motors
    "kI": 0,
    "kD": 0,

    # Constants for feed-forward of propulsion motors
    "kS": 0,
    "kV": 0,
    "kA": 0,
    
}
SW = namedtuple("Data", sw_data.keys())(**sw_data)