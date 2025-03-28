import wpilib
import commands2
from phoenix6 import hardware, signals, configs, StatusCode, controls
from enum import Enum
import wpimath.controller
import wpimath.trajectory

from constants import ELEC, SW, MECH

class WristSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        # Dio Sensors for Intake Subsystem
        self.wristEncoder = wpilib.DutyCycleEncoder(ELEC.Wrist_Encoder_DIO, 1, SW.WristOffset)
        
        # Motor for wrist Subsystem
        self.wristMotor = hardware.TalonFX(ELEC.WristMotor_ID)
        
        # Configs for motor
        self.motion_magic = controls.MotionMagicVoltage(0)
        motor_config = configs.TalonFXConfiguration()
        # motor_config.motor_output.inverted = False
        
        # Neutral mode for motor
        brakemode = signals.NeutralModeValue(ELEC.wrist_neutral_mode)
        
        # Configure gear ratio
        feedBack = motor_config.feedback
        feedBack.sensor_to_mechanism_ratio = MECH.wrist_gearing_ratio
        
        # Config for motion magic
        motionMagic = motor_config.motion_magic
        motionMagic.motion_magic_cruise_velocity = SW.Wrist_Cruise_Velocity
        motionMagic.motion_magic_acceleration = SW.Wrist_acceleration
        motionMagic.motion_magic_jerk = SW.Wrist_motion_jerk
        
        # Configure the PID for slot 0
        slot0 = motor_config.slot0
        slot0.k_s = SW.WristKs # Add 0.25 V output to overcome static friction
        slot0.k_v = SW.WristKv # A velocity target of 1 rps results in 0.12 V output
        slot0.k_a = SW.WristKa # An acceleration of 1 rps/s requires 0.01 V output
        slot0.k_p = SW.WristKp # A position error of 0.2 rotations results in 12 V output
        slot0.k_i = SW.WristKi # No output for integrated error
        slot0.k_d = SW.WristKd # A velocity error of 1 rps results in 0.5 V output
        
        # Pid settings for the wrist
        self.wristPID = wpimath.controller.PIDController(SW.WristKp, 0, 0)
        self.wristPID.enableContinuousInput(0, 1)
        self.wristPID.setTolerance(.3)
        self.wristPID.setIntegratorRange(-0.8, 0.8)
        
        # Set the target mode
        self.coralMode = True
        
        # self.wristMotor.configurator.apply(motor_config)

        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.wristMotor.configurator.apply(motor_config)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")
            
        self.wristMotor.setNeutralMode(brakemode)

    def periodic(self) -> None:
        
        # Update Wrist encoder
        self.wristAbsoluteEncoder = self.wristEncoder.get()
        self.encoder = self.wristMotor.get_rotor_position().value
        
        # Display Values onto the Dashboard
        wpilib.SmartDashboard.putBoolean("Wrist PID at setpoint", self.wristPID.atSetpoint())
        wpilib.SmartDashboard.putBoolean("Coral Mode", self.coralMode)
        
        wpilib.SmartDashboard.putNumber("Wrist Absolute Encoder Value", self.wristAbsoluteEncoder)
        wpilib.SmartDashboard.putNumber("Wrist Mechanism rotations", self.encoder/MECH.wrist_gearing_ratio)
        wpilib.SmartDashboard.putNumber("Wrist Motor Encoder Value", self.encoder)

    def wristwithjoystick(self, joystickinput):
        calculatedinput = joystickinput * ELEC.elevator_speed_multiplier
        self.wristMotor.set(calculatedinput)
        
    def WristStop(self):
        self.wristMotor.set(0)
        
    def wristWithPID(self, target):
        self.wristMotor.set(self.wristPID.calculate(self.encoder, target))
            
    def wristMotionMagic(self, target):
        self.wristMotor.set_control(self.motion_magic.with_position(target).with_slot(0))
        
        
    # Set what game piece to target algae/coral
    def cMode(self):
        self.coralMode = True
        
    def aMode(self):
        self.coralMode = False
        
    # read what game piece it's targetting
    def pieceStatus(self):
        """True: `Coral Mode`
        False: `Algae Mode` """
        
        return self.coralMode