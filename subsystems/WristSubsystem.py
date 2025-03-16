import wpilib
import commands2
import phoenix6
import wpimath.controller
import wpimath.trajectory

from constants import ELEC, SW, MECH

class WristSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        # Dio Sensors for Intake Subsystem
        self.wristEncoder = wpilib.DutyCycleEncoder(ELEC.Wrist_Encoder_DIO, 1, SW.WristOffset)
        
        # Motors for Intake Subsystem
        self.wristMotor = phoenix6.hardware.TalonFX(ELEC.WristMotor_ID)
        self.brakemode = phoenix6.signals.NeutralModeValue(ELEC.wrist_neutral_mode)
        self.wristMotor.setNeutralMode(self.brakemode)
        # self.wristMotor.set_position(self.wristEncoder.get() * MECH.wrist_gearing_ratio)

        
        # Pid settings for the wrist
        self.wristPID = wpimath.controller.PIDController(SW.WristKp, 0, 0)
        self.wristPID.enableContinuousInput(0, 1)
        self.wristPID.setTolerance(.3)
        self.wristPID.setIntegratorRange(-0.8, 0.8)

    def periodic(self) -> None:
        
        # Update Wrist encoder
        self.wristsEncoderVal = self.wristEncoder.get()
        self.encoder = self.wristMotor.get_rotor_position().value
        
        # Display Values onto the Dashboard
        wpilib.SmartDashboard.putBoolean("Wrist PID at setpoint", self.wristPID.atSetpoint())
        wpilib.SmartDashboard.putNumber("Wrist Absolute Encoder Value", self.wristEncoder.get())
        wpilib.SmartDashboard.putNumber("Wrist Motor Encoder Value", self.encoder)

    def wristwithjoystick(self, joystickinput):
        calculatedinput = joystickinput * ELEC.elevator_speed_multiplier
        self.wristMotor.set(calculatedinput)
        
    def wristForward(self):
        self.wristMotor.set(0.25)
        
    def wristBackwards(self):
        self.wristMotor.set(-0.4)
        
    def wristWithJoystick(self, joystickInput):
        motorOutput = joystickInput * ELEC.wrist_speed_multiplier
        self.wristMotor.set(motorOutput)
        
    def WristStop(self):
        self.wristMotor.set(0)
        
    def wristWithPID(self, target):
        self.wristMotor.set(self.wristPID.calculate(self.wristsEncoderVal, target))
        
    def WristL2(self):
        self.wristMotor.set(self.wristPID.calculate(self.encoder, SW.Wrist_L2_Setpoint))
        return self.wristPID.atSetpoint()
    
    def WristL3(self):
        self.wristMotor.set(self.wristPID.calculate(self.encoder, SW.Wrist_L3_Setpoint)) # Not tested
        return self.wristPID.atSetpoint()
        
    def WristL4(self):
        self.wristMotor.set(self.wristPID.calculate(self.encoder, SW.Wrist_L4_Setpoint)) # Not tested
        return self.wristPID.atSetpoint()
        