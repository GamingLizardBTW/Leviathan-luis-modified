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
from pathplannerlib.config import RobotConfig

#Unit Conversions
cvr_data = {
    "meterPerInch": 0.0254,
    "radianPerRotation": math.tau
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
    #Drivetrain
    "swerve_module_driving_gearing_ratio": 6.75,  # SDS Mk4i L2  6.75 rotation on motor per 1 rotatio on drivetrain
    "swerve_module_steering_gearing_ratio": 150 / 7,  # SDS Mk4i
    "driving_motor_inverted": False,
    "steering_motor_inverted": True,
    
    #Wrist
    "wrist_gearing_ratio": 125, #About 208.3 motor rotation to 1 wrist rotation
    "wrist_motor_inverted": False,
    
    # Elevator
    "Elevator_gear_ratio": 57.48, # rotor rotations per mechanism rotation
}
MECH = namedtuple("Data", mech_data.keys())(**mech_data)

# Electrical constants
elec_data = {

    #SwerveDrive
    "RF_drive_CAN_ID": 3,
    "RF_steer_CAN_ID": 20,
    "RF_encoder_DIO": 8,
    "RB_steer_CAN_ID": 12,
    "RB_drive_CAN_ID": 1,
    "RB_encoder_DIO": 7,
    "LB_steer_CAN_ID": 8,
    "LB_drive_CAN_ID": 7,
    "LB_encoder_DIO": 9,
    "LF_steer_CAN_ID": 11,
    "LF_drive_CAN_ID": 5,
    "LF_encoder_DIO": 0,  
    "driveMotor_neutral": phoenix6.signals.NeutralModeValue(1),
    "steerMotor_neutral": phoenix6.signals.NeutralModeValue(1),

    #Wrist
    "WristMotor_ID": 9,
    "wrist_neutral_mode": 1,
    "wrist_speed_multiplier": 0.5,
    "Wrist_Encoder_DIO": 6,

    #Intake
    "IntakeMotor_ID": 6,
    "IntakeBeamBreakID": 3,
    "IntakeSpeed": 1,
    "OutakeSpeed": -1,
    
    # Elevator
    "TopElevatorMotor_ID": 18,
    "BottomElevatorMotor_ID": 17,
    "elevator_neutral_mode": 1,
    "elevator_speed_multiplier": -0.4,
    "BottomLimitSwitch": 5,
    "TopLimitSwitch": 4,
    
    # Hang
    "Hang_Motor_ID": 16,
    "Hang_Neutal_Mode": 1,
    
    #LED
    "LED_length": 200,
    "pwm_port": 0,

}    
ELEC = namedtuple("Data", elec_data.keys())(**elec_data)

# Operation constants
op_data = {
    
    #Driver/Operator's controllers
    "driver_controller": 0,
    "operator_controller": 1,
    
    #Swerve
    "max_steering_velocity": math.pi,
    "max_steering_acceleration": math.tau,
    "max_speed": 3.25, #unit in meter per second
    "max_turn_speed": 6.5 #unit in radian per second

}
OP = namedtuple("Data", op_data.keys())(**op_data)

# Software constants
sw_data = {
    # field_relative: True if "forward" means "down the field"; False if
    # "forward" means "in the direction the robot is facing".  A True value
    # requires a (non-Dummy) gyro.
    "field_relative": True,

    # "Zero" (front-facing) positions, as read from the four encoders
	# NOTE: when facing wheels "front", make sure that the bevel gears are all
	# facing right.  Otherwise the wheel will run in reverse!
	#
    "path_planner_config": RobotConfig.fromGUISettings(),

	"lf_enc_zeropos":  0.3395293834882346,
	"rf_enc_zeropos":  0.1649970041249251,
	"lb_enc_zeropos":  0.7011371425284285,
	"rb_enc_zeropos":  0.44212201105305027,

    "swerve_drive_kS": 0,
    "swerve_drive_kV": 0.12,
    "swerve_drive_kP": 0.11,
    "swerve_drive_kI": 0,
    "swerve_drive_kD": 0,

    "swerve_steer_kP": 1,
    # "swerve_steer_kP": 0,
    "swerve_steer_kI": 0,
    "swerve_steer_kD": 0,
    
    # Automation:
    "drivetrain_rotation_kP": 0.1,
    "drivetrain_rotation_kI": 0,
    "drivetrain_rotation_kD": 0,
    
    # -------------------------------- WRIST --------------------------------------
    
    # Wrist PID constants
    "WristKs": 2,
    "WristKv": 0.12,
    "WristKa": 0,
    "WristKp": 65,
    "WristKi": 0,
    "WristKd": 0,
    "WristOffset": 0,
    
    # Wrist PID Setpoints
    "Wrist_L2_Setpoint": 0.31801953125, # Coral L2
    "Wrist_L3_Setpoint": 0.28, # Coral L3
    "Wrist_L4_Setpoint": 0.265, # Coral L4
    
    "Algae_L2_Setpoint": 0.265, # Algae L2
    "Algae_L3_Setpoint": 0.263, # Algae L3
    "Wrist_Barge_Setpoint": 0.08, # Barge
    
    "Wrist_Processor_Setpoint": 0.285, # Processor
    "Wrist_ground_Setpoint": 0.35, # Algae Ground Intake
    "Wrist_Human_Player_Setpoint": 0.145, # Human Player
    
    # Elevator Speed controls
    "Wrist_Cruise_Velocity": 20, # (mechanism) cruise (measured in rotations per sec)
    "Wrist_acceleration": 35, # seconds to reach max vel (Measured in rotations per sec²) (time = Velocity/accel)
    "Wrist_motion_jerk": 280, # seconds to reach max accel (Measured in rotations per sec³) (time = accel/jerk)
    
    # ------------------------------- ELEVATOR ---------------------------------------
    
    # Elevator PID Constats
    "Elevatorks": 3, # Add 3 V output to overcome static friction
    "Elevatorkv": 0.12, # A velocity target of 1 rps results in 0.12 V outp
    "Elevatorka": 0, # An acceleration of 1 rps/s requires 0 V output
    "Elevatorkp": 45,
    "Elevatorki": 0.01, # No output for integrated error
    "Elevatorkd": 0.01,
    
    # Elevator Tolerence Constants
    "ElevatorTolerance": 0.15,
    "ElevatorSpeedTolerence": 0.2,
    
    # Elevator Speed controls
    "Elevator_Cruise_Velocity": 24, # (mechanism) cruise (measured in rotations per sec)
    "Elevator_acceleration": 54, # seconds to reach max vel (Measured in rotations per sec²) (time = Velocity/accel)
    "Elevator_motion_jerk": 500, # seconds to reach max accel (Measured in rotations per sec³) (time = accel/jerk)
    
    # Elevator PID Setpoints (Using Mechanism rotations not motor rotations)
    "L2_Setpoint": 0.9030026181,
    "L3_Setpoint": 1.6501570686,
    "L4_Setpoint": 2.8098507863,
    # "L2_AlgaeSetpoint": 0.9030026181,
    "L3_AlgaeSetpoint": 1.7876701577,
    "Human_Player_Station": 0.3483664923,
    "Home": 0.0458376964,
    
}
SW = namedtuple("Data", sw_data.keys())(**sw_data)