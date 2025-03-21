import wpilib
import commands2
from wpilib import XboxController
from phoenix6 import hardware, controls, configs, StatusCode
from constants import SW, OP, ELEC

class MotionMagicClass(commands2.Subsystem):

    def __init__(self) -> None:
        """Robot initialization function"""

        # Keep a reference to all the motor controllers used
        self.talonfx = hardware.TalonFX(22)
        self.motion_magic = controls.MotionMagicVoltage(0)

        self.joystick = XboxController(OP.operator_controller)

        cfg = configs.TalonFXConfiguration()

        # Configure gear ratio
        fdb = cfg.feedback
        fdb.sensor_to_mechanism_ratio = 12.8 # 12.8 rotor rotations per mechanism rotation

        # Configure Motion Magic
        mm = cfg.motion_magic
        mm.motion_magic_cruise_velocity = 5 # 5 (mechanism) rotations per second cruise
        mm.motion_magic_acceleration = 10 # Take approximately 0.5 seconds to reach max vel
        
        # Take apprximately 0.1 seconds to reach max accel
        mm.motion_magic_jerk = 100

        slot0 = cfg.slot0
        slot0.k_s = 0.25 # Add 0.25 V output to overcome static friction
        slot0.k_v = 0.12 # A velocity target of 1 rps results in 0.12 V output
        slot0.k_a = 0.01 # An acceleration of 1 rps/s requires 0.01 V output
        slot0.k_p = 60 # A position error of 0.2 rotations results in 12 V output
        slot0.k_i = 0 # No output for integrated error
        slot0.k_d = 0.5 # A velocity error of 1 rps results in 0.5 V output

        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.talonfx.configurator.apply(cfg)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")

    def teleopInit(self):
        pass
        
    def periodic(self) -> None:
        pass
        # wpilib.SmartDashboard.putNumber("Num", 0)
        # num = wpilib.SmartDashboard.getNumber("Num", 0)
        # print(num)
            
    def motionMagic(self):
        # Deadband the joystick
        left_y = self.joystick.getLeftY()
        if abs(left_y) < 0.1:
            left_y = 0

        self.talonfx.set_control(self.motion_magic.with_position(left_y * 10).with_slot(0))
        if (self.joystick.getBButton()):
            self.talonfx.set_position(1)
        # elif (self.joystick)