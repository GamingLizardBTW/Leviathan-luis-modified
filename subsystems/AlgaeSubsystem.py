import wpilib
import phoenix6
import commands2
import time
import wpimath.controller
import wpimath.trajectory

from phoenix6.hardware import talon_fx
from phoenix6.configs import TalonFXConfiguration
from phoenix6.configs.config_groups import Slot0Configs
from phoenix6.controls import PositionDutyCycle

from constants import SW, ELEC

class AlgaeSubsystemClass(commands2.Subsystem):
        
    def __init__(self) -> None:
        # Dio Sensors for AlgaeSubsystem
        self.LimitSwitch = wpilib.DigitalInput(1)
        
        # Motors for AlageSubsystem
        self.wristMotor = phoenix6.hardware.TalonFX(0)
        self.algaeintakemotor = phoenix6.hardware.TalonFX(9)
        
        # Settings for motors
        self.brakMode = phoenix6.signals.NeutralModeValue(1)
        self.algaeintakemotor.setNeutralMode(self.brakMode)
        self.wristMotor.setNeutralMode(self.brakMode)
        
        # PID for talonFX motor
        self.my_config = TalonFXConfiguration()
        self.algaeintakemotor.configurator.refresh(self.my_config) # Writes current configs into algaeintakemotor
        # self.my_slot0_pid_config = Slot0Configs(0.5)
        # self.wristMotor.configurator.apply(self.my_config.with_slot0(self.my_slot0_pid_config))
        
        # Pid settings for the wrist
        self.wristPID = wpimath.controller.PIDController(SW.AlgaeWristKp, 0, 0)
        self.wristPID.setTolerance(1)
        self.wristPID.setIntegratorRange(-0.3, 0.3)
        self.wristPIDOffset = self.wristMotor.get_rotor_position().value
        self.control_request = phoenix6.controls.DutyCycleOut(0.0)
        
    def periodic(self) -> None:
        
        # Update Wrist encoder
        self.wristsEncoder = self.wristMotor.get_rotor_position().value - self.wristPIDOffset
        
        # Display Values onto the Dashboard
        wpilib.SmartDashboard.putNumber("Wrist Position", self.wristsEncoder)
        wpilib.SmartDashboard.putBoolean("Arm PID at setpoint", self.wristPID.atSetpoint())
        
    def resetPIDOffset(self):
        self.wristPIDOffset = self.wristMotor.get_rotor_position().value
        
    
    def algaeoutake(self):
        print("outake")
        self.algaeintakemotor.set_control(self.control_request.with_output(-1.0))
        
    def algaeintake(self):
        print("Intake")
        self.algaeintakemotor.set(0.6)
    
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
        self.wristMotor.set(0)
        
    def wristToFloor(self):
        self.wristMotor.set(self.wristPID.calculate(self.wristsEncoder, 2))
        return self.wristPID.atSetpoint()
        
    def wristToRobot(self):
        self.wristMotor.set(self.wristPID.calculate(self.wristsEncoder, 0))
        return self.wristPID.atSetpoint()
    
    # def setPIDWithControlRequest(self):
    #     self.control_request = PositionDutyCycle(0.5, slot = 0)
    #     self.wristMotor.set_control(self.control_request)