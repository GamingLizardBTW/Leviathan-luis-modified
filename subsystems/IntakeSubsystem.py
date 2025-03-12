import wpilib
import phoenix6
import commands2

from constants import SW, ELEC

class IntakeSubsystemClass(commands2.Subsystem):
        
    def __init__(self) -> None:
        # Motors for Intake Subsystem
        self.Intakeintakemotor = phoenix6.hardware.TalonFX(ELEC.IntakeMotor_ID)
        
        # Settings for motors
        self.brakMode = phoenix6.signals.NeutralModeValue(1)
        self.Intakeintakemotor.setNeutralMode(self.brakMode)
    
    def Outake(self):
        print("outake")
        self.Intakeintakemotor.set(SW.IntakeSpeed)
        
    def Intake(self):
        print("Intake")
        self.Intakeintakemotor.set(SW.OutakeSpeed)
    
    def Stop(self):
        self.Intakeintakemotor.set(0)