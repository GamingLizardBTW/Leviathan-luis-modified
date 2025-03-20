import wpilib
import commands2
import phoenix6
from constants import ELEC, SW

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
        self.topMotor = phoenix6.hardware.TalonFX(ELEC.TopElevatorMotor_ID)
        self.bottoMmotor = phoenix6.hardware.TalonFX(ELEC.BottomElevatorMotor_ID)
        
        # Get motor encoders
        # self.encoder = (self.topMotor.get_rotor_position().value + self.bottoMmotor.get_rotor_position().value)/2

        
        # Motor Settings
        self.brakemode = phoenix6.signals.NeutralModeValue(ELEC.elevator_neutral_mode)
        # self.motorGroup = wpilib.MotorControllerGroup(self.bottoMmotor, self.topMotor)
        
        # Setting motor brakemode
        self.topMotor.setNeutralMode(self.brakemode)
        self.bottoMmotor.setNeutralMode(self.brakemode)
        
        # Normal PID Controll
        self.topMotor.set_position(0)
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
        # if self.bottomOveride:
        #     setpoint = self.elevatorPID.calculate(self.encoder, 0)
        #     self.topMotor.set(setpoint)
        #     self.bottoMmotor.set(setpoint)