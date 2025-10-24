import wpilib
import commands2
import phoenix6
import wpimath.controller
import wpimath.trajectory

from constants import ELEC, SW

class HangSubsystem(commands2.Subsystem):

    def __init__(self) -> None:

        # Motors for Intake Subsystem
        self.hangMotor = phoenix6.hardware.TalonFX(ELEC.Hang_Motor_ID)
        self.brakemode = phoenix6.signals.NeutralModeValue(ELEC.Hang_Neutal_Mode)
        self.hangMotor.setNeutralMode(self.brakemode)
        
    def hangForward(self):
        self.hangMotor.set(1)
        
    def hangBackwards(self):
        self.hangMotor.set(-1)
        
    def hangStop(self):
        self.hangMotor.set(0)