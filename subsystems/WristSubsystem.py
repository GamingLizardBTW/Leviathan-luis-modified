import wpilib
import commands2
import phoenix6
import wpimath.controller
import wpimath.trajectory

from constants import ELEC, SW

class WristSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        # Dio Sensors for Intake Subsystem
        self.wristEncoder = wpilib.DutyCycleEncoder(ELEC.Wrist_Encoder_DIO, 1, SW.WristOffset)
        
        # Motors for Intake Subsystem
        self.wristMotor = phoenix6.hardware.TalonFX(ELEC.WristMotor_ID)
        self.brakemode = phoenix6.signals.NeutralModeValue(ELEC.wrist_neutral_mode)
        self.wristMotor.setNeutralMode(self.brakemode)
        
        # Pid settings for the wrist
        self.wristPID = wpimath.controller.PIDController(SW.WristKp, 0, 0)
        self.wristPID.enableContinuousInput(0, 1)
        self.wristPID.setTolerance(.3)
        self.wristPID.setIntegratorRange(-0.8, 0.8)

    def periodic(self) -> None:
        
        # Update Wrist encoder
        self.wristsEncoderVal = self.wristEncoder.get()
        
        # Display Values onto the Dashboard
        wpilib.SmartDashboard.putBoolean("Wrist PID at setpoint", self.wristPID.atSetpoint())
        wpilib.SmartDashboard.putNumber("Wrist Encoder Value", self.wristEncoder.get())
        
    def wristForward(self):
        self.wristMotor.set(0.25)
        
    def wristBackwards(self):
        self.wristMotor.set(-0.4)
        
    def wristWithJoystick(self, joystickInput):
        motorOutput = joystickInput * ELEC.wrist_speed_multiplier
        self.wristMotor.set(motorOutput)
        
    def WristStop(self):
        self.wristMotor.set(0)
        
    def writPID(self, target):
        self.wristMotor.set(self.wristPID.calculate(self.wristsEncoderVal, target))
        
    def WristL2(self):
        self.wristMotor.set(self.wristPID.calculate(self.wristsEncoderVal, 0))
        return self.wristPID.atSetpoint()
    
    def WristL3(self):
        self.wristMotor.set(self.wristPID.calculate(self.wristsEncoderVal, .18)) # Not tested
        return self.wristPID.atSetpoint()
        
    def WristL4(self):
        self.wristMotor.set(self.wristPID.calculate(self.wristsEncoderVal, .3)) # Not tested
        return self.wristPID.atSetpoint()
        