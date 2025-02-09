import wpilib
import phoenix6
import commands2
import time
import wpimath.controller
import wpimath.trajectory

from constants import SW, ELEC

class AlgaeSubsystemClass(commands2.Subsystem):
    def __init__(self) -> None:
        
        # Dio Sensors for AlgaeSubsystem
        self.LimitSwitch = wpilib.DigitalInput(1)
        
        # Motors for AlageSubsystem
        self.wristMotor = phoenix6.hardware.TalonFX(ELEC.AlgaeWristMotor)
        self.algaeintakemotor = phoenix6.hardware.TalonFX(ELEC.AlgaeMotor)
        
        # Settings for motors
        self.brakMode = phoenix6.signals.NeutralModeValue(1)
        self.algaeintakemotor.setNeutralMode(self.brakMode)
        self.wristMotor.setNeutralMode(self.brakMode)
        
        # Pid settings for the wrist
        self.wristPID = wpimath.controller.PIDController(SW.AlgaeWristKp, 0, 0)
        self.wristPID.setTolerance(1)
        self.wristPID.setIntegratorRange(-0.3, 0.3)
        self.wristPIDOffset = self.wristMotor.get_rotor_position().value
        
    def periodic(self) -> None:
        # Update Wrist encoder
        self.wristsEncoder = self.wristMotor.get_rotor_position().value - self.wristPIDOffset
        
        # Display Values onto the Dashboard
        wpilib.SmartDashboard.putNumber("Wrist Position", self.wristsEncoder)
        wpilib.SmartDashboard.putBoolean("Arm PID at setpoint", self.wristPID.atSetpoint())
        
    def resetPIDOffset(self):
        self.wristPIDOffset = self.wristMotor.get_rotor_position().value
        
    
    def algaeoutake(self):
        # self.algaeintakeLowermotor.set(0.5)
        self.algaeintakemotor.set(SW.AlgaeOutakeSpeed)
        
    def algaeintake(self):
        # self.algaeintakeLowermotor.set(-0.25)
        self.algaeintakemotor.set(SW.AlgaeIntakeSpeed)
    
    def algaestop(self):
        # if self.LimitSwitch.get():
        #     self.algaeintakeLowermotor.set(0)
        #     self.algaeintakeUppermotor.set(0)
        # else:
        #     self.algaeintakeLowermotor.set(0.05)
        #     self.algaeintakeUppermotor.set(-0.05)
        # self.algaeintakeLowermotor.set(0)
        self.algaeintakemotor.set(0)
        
    def wristForward(self):
        self.wristMotor.set(-0.2)
        
    def wristBackwards(self):
        self.wristMotor.set(0.2)
        
    def algaeWristStop(self):
        # print(self.wristsEncoder)
        self.wristMotor.set(0)
        
    def wristToFloor(self):
        self.wristMotor.set(self.wristPID.calculate(self.wristsEncoder, 2))
        return self.wristPID.atSetpoint()
        
    def wristToRobot(self):
        self.wristMotor.set(self.wristPID.calculate(self.wristsEncoder, 0))
        return self.wristPID.atSetpoint()