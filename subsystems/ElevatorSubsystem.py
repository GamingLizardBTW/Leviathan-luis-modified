import wpilib
import commands2
import phoenix6
from constants import ELEC, SW
from phoenix6 import hardware, controls, configs, StatusCode, signals

# Pid imports
import wpimath
import math
import wpimath.controller
import wpimath.trajectory

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
        
        # Configure gear ratio
        feedBack = config.feedback
        feedBack.sensor_to_mechanism_ratio = 14.5 # rotor rotations per mechanism rotation
        
        # Configure Motion Magic
        motionMagic = config.motion_magic
        motionMagic.motion_magic_cruise_velocity = 1.5 # (mechanism) rotations per second cruise
        motionMagic.motion_magic_acceleration = 100 # Take approximately 0.5 seconds to reach max vel
        motionMagic.motion_magic_jerk = 1000 # Take apprximately 0.1 seconds to reach max accel
        
        # Configure the PID for slot 0
        slot0 = config.slot0
        slot0.k_s = SW.Elevatorks # Add 0.25 V output to overcome static friction
        slot0.k_v = SW.Elevatorkv # A velocity target of 1 rps results in 0.12 V output
        slot0.k_a = SW.Elevatorka # An acceleration of 1 rps/s requires 0.01 V output
        slot0.k_p = SW.Elevatorkp # A position error of 0.2 rotations results in 12 V output
        slot0.k_i = SW.Elevatorki # No output for integrated error
        slot0.k_d = SW.Elevatorkd # A velocity error of 1 rps results in 0.5 V output

        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.topMotor.configurator.apply(config)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")
        
        # Setting motor brakemode
        self.brakemode = signals.NeutralModeValue(ELEC.elevator_neutral_mode)
        self.topMotor.setNeutralMode(self.brakemode)
        self.bottoMmotor.setNeutralMode(self.brakemode)
        
        
        
        
        'Remove the following soon: '
        # Normal PID Controll
        # self.topMotor.set_position(0)
        # self.bottoMmotor.set_position(0)
        self.elevatorPID = wpimath.controller.PIDController(SW.Elevatorkp, SW.Elevatorki, SW.Elevatorkd)
        self.elevatorPID.setTolerance(SW.ElevatorTolerance)
        
    def periodic(self) -> None:
        # Update encoders
        # self.encoder = (self.topMotor.get_rotor_position().value + self.bottoMmotor.get_rotor_position().value)/2
        self.encoder = self.topMotor.get_rotor_position().value
        # self.setEncoderToZeroAtBottom()
        
        # SmartDashboard
        # wpilib.SmartDashboard.putNumber("Elevator Setpoint", self.elevatorPID.getSetpoint())
        
        wpilib.SmartDashboard.putNumber("Top Motor encoder", self.topMotor.get_rotor_position().value)
        wpilib.SmartDashboard.putNumber("Bottom Motor Encoder", self.bottoMmotor.get_rotor_position().value)
        wpilib.SmartDashboard.putNumber("Average Motor Encoder", self.encoder)
        
        wpilib.SmartDashboard.putBoolean("Top Limit Switch", self.topSwitch.get())
        wpilib.SmartDashboard.putBoolean("Bottom Limit Switch", self.bottomSwitch.get())
        
        # This is used to force stop any elevator commands if limit switch is hit
        self.topOveride = self.topSwitch.get()
        self.bottomOveride = self.bottomSwitch.get()
        
        # if self.bottomOveride is False:
        #     self.topMotor.configurator.set_position(0)
        #     self.bottoMmotor.configurator.set_position(0)
        

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
        # self.setEncoderToZeroAtBottom()

    def elevatorMotorStop(self):
        self.topMotor.set(0)
        self.bottoMmotor.set(0)
        
    def normalPID(self, target):
        elevatorPIDoutput = self.elevatorPID.calculate(self.encoder, target)
        if self.bottomOveride and elevatorPIDoutput < 0:
            self.topMotor.set(0)
            self.bottoMmotor.set(0)
        elif self.topOveride and elevatorPIDoutput > 0:
            self.topMotor.set(0)
            self.bottoMmotor.set(0)
        else:
            self.topMotor.set(elevatorPIDoutput)
            self.bottoMmotor.set(elevatorPIDoutput)
        # if self.topOveride:
        #     setpoint = self.elevatorPID.calculate(self.encoder, target)
        #     self.topMotor.set(setpoint)
        #     self.bottoMmotor.set(setpoint)
        # setpoint = self.elevatorPID.calculate(self.encoder, target)
        # self.topMotor.set(setpoint)
        # self.bottoMmotor.set(setpoint)
        
    def homeElevator(self):
        elevatorPIDoutput = self.elevatorPID.calculate(self.encoder, 0)
        if self.bottomOveride and elevatorPIDoutput < 0:
            self.topMotor.set(0)
            self.bottoMmotor.set(0)
        elif self.topOveride and elevatorPIDoutput > 0:
            self.topMotor.set(0)
            self.bottoMmotor.set(0)
        else:
            self.topMotor.set(elevatorPIDoutput)
            self.bottoMmotor.set(elevatorPIDoutput)
            
    def setEncoderToZeroAtBottom(self):
        if self.bottomSwitch.get():
            self.topMotor.set_position(0)
        
    
    # PID controls with mtion magic
    def motionMagic(self, left_y):
        self.topMotor.set_control(self.motion_magic.with_position(left_y * 10).with_slot(0)
            .with_limit_forward_motion(not self.bottomOveride)
            .with_limit_reverse_motion(not self.topOveride))
        self.bottoMmotor.set_control(self.follow_left_request)
        
    def homeElevator2(self):
        self.topMotor.set_control(self.motion_magic.with_position(0).with_slot(0)
            .with_limit_forward_motion(not self.bottomOveride)
            .with_limit_reverse_motion(not self.topOveride))
        self.bottoMmotor.set_control(self.follow_left_request)
            
    def normalPID2(self, target):
        self.topMotor.set_control(self.motion_magic.with_position(target).with_slot(0)
            .with_limit_forward_motion(not self.bottomOveride)
            .with_limit_reverse_motion(not self.topOveride))
        self.bottoMmotor.set_control(self.follow_left_request)