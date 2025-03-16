import wpilib
from wpilib import Timer
import phoenix6
import commands2


from constants import SW, ELEC

class IntakeSubsystemClass(commands2.Subsystem):
        
    def __init__(self) -> None:
        # Motors for Intake Subsystem
        self.Intakeintakemotor = phoenix6.hardware.TalonFX(ELEC.IntakeMotor_ID)
        
        # Dio ports for sensors
        self.beamBreak = wpilib.DigitalInput(ELEC.IntakeBeamBreakID)
        
        # Settings for motors
        self.brakMode = phoenix6.signals.NeutralModeValue(1)
        self.Intakeintakemotor.setNeutralMode(self.brakMode)
    
    def Outake(self):
        print("outake")
        self.Intakeintakemotor.set(ELEC.IntakeSpeed)
        
    def Intake(self):
        self.Intakeintakemotor.set(ELEC.OutakeSpeed)
        # print("Intake")
        # if self.beamBreak.get():
        #     Timer.reset()
        #     Timer.start()
        #     if Timer.get() == 1:
        #         self.Intakeintakemotor.set(0)
        # else:
        #     self.Intakeintakemotor.set(ELEC.OutakeSpeed)
    
    def Stop(self):
        self.Intakeintakemotor.set(0)