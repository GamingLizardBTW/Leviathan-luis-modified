import wpilib
import phoenix6
import commands2
import time
import wpimath.controller
import wpimath.trajectory
from navx import AHRS

from constants import SW, ELEC

class AlgaeSubsystemClass(commands2.Subsystem):
        
    def __init__(self) -> None:
        # Dio Sensors for AlgaeSubsystem
        self.wristEncoder = wpilib.DutyCycleEncoder(22, 1, SW.AlgaeWristOffset)
        
        # Motors for AlageSubsystem
        self.wristMotor = phoenix6.hardware.TalonFX(0)
        self.algaeintakemotor = phoenix6.hardware.TalonFX(9)
        
        # Settings for motors
        self.brakMode = phoenix6.signals.NeutralModeValue(1)
        self.algaeintakemotor.setNeutralMode(self.brakMode)
        self.wristMotor.setNeutralMode(self.brakMode)
        
        # Pid settings for the wrist
        self.wristPID = wpimath.controller.PIDController(SW.AlgaeWristKp, 0, 0)
        self.wristPID.setTolerance(.3)
        self.wristPID.setIntegratorRange(-0.5, 0.5)

    def periodic(self) -> None:
        
        # Update Wrist encoder
        self.wristsEncoderVal = self.wristEncoder.get()
        
        # Display Values onto the Dashboard
        wpilib.SmartDashboard.putBoolean("Arm PID at setpoint", self.wristPID.atSetpoint())
        wpilib.SmartDashboard.putNumber("Encoder Value", self.wristsEncoderVal)
    
    def algaeoutake(self):
        print("outake")
        self.algaeintakemotor.set(-1)
        
    def algaeintake(self):
        print("Intake")
        self.algaeintakemotor.set(1)
    
    def algaestop(self):
        self.algaeintakemotor.set(0)
        
    def wristForward(self):
        self.wristMotor.set(0.25)
        
    def wristBackwards(self):
        self.wristMotor.set(-0.4)
        
    def algaeWristStop(self):
        self.wristMotor.set(0)
        
    def wristToFloor(self):
        self.wristMotor.set(self.wristPID.calculate(self.wristsEncoderVal, .3)) # Not tested
        return self.wristPID.atSetpoint()
        
    def wristToRobot(self):
        self.wristMotor.set(self.wristPID.calculate(self.wristsEncoderVal, 0))
        return self.wristPID.atSetpoint()
    
    def wristToProcesor(self):
        self.wristMotor.set(self.wristPID.calculate(self.wristsEncoderVal, .18)) # Not tested
        return self.wristPID.atSetpoint()