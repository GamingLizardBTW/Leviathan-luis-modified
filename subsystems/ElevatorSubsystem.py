import wpilib
import commands2
import phoenix6
import math

from constants import ELEC, SW, MECH
from phoenix6 import hardware, controls, configs, StatusCode, signals
from wpimath import controller, trajectory
from wpilib import SmartDashboard

class ElevatorSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        # Sensors
        self.bottomSwitch = wpilib.DigitalInput(ELEC.BottomLimitSwitch)
        self.topSwitch = wpilib.DigitalInput(ELEC.TopLimitSwitch)
        
        # Creating Motor Instances
        self.topMotor = hardware.TalonFX(ELEC.TopElevatorMotor_ID)
        self.bottoMmotor = hardware.TalonFX(ELEC.BottomElevatorMotor_ID)
        
        # Motor Settings
        self.motion_magic = controls.MotionMagicVoltage(0)
        config = configs.TalonFXConfiguration()
        self.follow_left_request = controls.Follower(ELEC.TopElevatorMotor_ID, False)
        self.bottoMmotor.set_control(self.follow_left_request)
        elevatorGravity = signals.GravityTypeValue(0)
        
        # Setting motor brakemode
        self.brakemode = signals.NeutralModeValue(ELEC.elevator_neutral_mode)
        self.topMotor.setNeutralMode(self.brakemode)
        self.bottoMmotor.setNeutralMode(self.brakemode)
        
        # Configure gear ratio
        feedBack = config.feedback
        feedBack.sensor_to_mechanism_ratio = MECH.Elevator_gear_ratio
        
        # Configure Motion Magic
        motionMagic = config.motion_magic
        motionMagic.motion_magic_cruise_velocity = SW.Cruise_Velocity
        motionMagic.motion_magic_acceleration = SW.acceleration
        motionMagic.motion_magic_jerk = SW.motion_jerk
        
        # Configure the PID for slot 0
        slot0 = config.slot0
        slot0.k_s = SW.Elevatorks # Add 0.25 V output to overcome static friction
        slot0.k_v = SW.Elevatorkv # A velocity target of 1 rps results in 0.12 V output
        slot0.k_a = SW.Elevatorka # An acceleration of 1 rps/s requires 0.01 V output
        slot0.k_p = SW.Elevatorkp # A position error of 0.2 rotations results in 12 V output
        slot0.k_i = SW.Elevatorki # No output for integrated error
        slot0.k_d = SW.Elevatorkd # A velocity error of 1 rps results in 0.5 V output
        slot0.gravity_type = elevatorGravity

        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.topMotor.configurator.apply(config)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")
        
    def periodic(self) -> None:
        # Update encoders
        self.encoder = self.topMotor.get_rotor_position().value
        
        # SmartDashboard
        SmartDashboard.putNumber("Top Motor encoder", self.encoder)
        SmartDashboard.putNumber("Mechanism rotations", (self.encoder/MECH.Elevator_gear_ratio))
        SmartDashboard.putNumber("Elevator Setpoint", self.topMotor.get_differential_closed_loop_reference().value_as_double)
        SmartDashboard.putNumber("Top Motor Speed", self.topMotor.get_velocity().value_as_double)
        
        SmartDashboard.putBoolean("Top Limit Switch", self.topSwitch.get())
        SmartDashboard.putBoolean("Bottom Limit Switch", self.bottomSwitch.get())
        
        # This is used to force stop any elevator commands if limit switch is hit
        self.topOveride = self.topSwitch.get()
        self.bottomOveride = self.bottomSwitch.get()
        
        # Get values from SmartDashboard
        self.elevatorPosition = SmartDashboard.getNumber("Mechanism rotations", 0)
        self.elevatorSetpoint = SmartDashboard.getNumber("Elevator Setpoint", 0)
        self.velocity = SmartDashboard.getNumber("Top Motor Speed", 0)
        

    def elevatorWithjoystick(self, joystickinput):
        calculatedinput = joystickinput * ELEC.elevator_speed_multiplier
        if self.bottomOveride is True and joystickinput > 0:
            self.topMotor.set(0)
            self.bottoMmotor.set(0)
        elif self.topOveride is True and joystickinput < 0:
            self.topMotor.set(0)
            self.bottoMmotor.set(0)
        else:
            self.topMotor.set(calculatedinput)
            self.bottoMmotor.set(calculatedinput)

    def elevatorMotorStop(self):
        self.topMotor.set(0)
        self.bottoMmotor.set(0)
            
    # def setEncoderToZeroAtBottom(self):
    #     if self.bottomSwitch.get():
    #         self.topMotor.set_position(0)
        
    
    # PID controls with mtion magic
    def motionMagicWithJoystick(self, left_y):
        self.topMotor.set_control(self.motion_magic.with_position(left_y * 10).with_slot(0)
            .with_limit_forward_motion(self.topOveride)
            .with_limit_reverse_motion(self.bottomOveride))
        self.bottoMmotor.set_control(self.follow_left_request)
            
    def elevatorPID(self, target):
        self.topMotor.set_control(self.motion_magic.with_position(target).with_slot(0)
            .with_limit_forward_motion(self.topOveride)
            .with_limit_reverse_motion(self.bottomOveride))
        self.bottoMmotor.set_control(self.follow_left_request)
        
    def motionFinished(self):
        if math.fabs(self.elevatorPosition - self.elevatorSetpoint) < SW.ElevatorTolerance and math.fabs(self.velocity) < SW.ElevatorSpeedTolerence:
            return True
        else:
            return False