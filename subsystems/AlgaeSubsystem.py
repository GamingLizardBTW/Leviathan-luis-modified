import wpilib
import phoenix6
import commands2
from constants import ELEC

class AlgaeSubsystemClass(commands2.Subsystem):
    def __init__(self) -> None:
        self.algaeintakeLeftmotor = phoenix6.hardware.TalonFX(ELEC.algae_leftmotor_CAN_ID)
        self.algaeintakeRightmotor = phoenix6.hardware.TalonFX(ELEC.algae_rightmotor_CAN_ID)
        self.brakemode = phoenix6.signals.NeutralModeValue(ELEC.algae_neutral_mode)
        self.algaeintakeLeftmotor.setNeutralMode(self.brakemode)
        self.algaeintakeRightmotor.setNeutralMode(self.brakemode)

    def algaeintake(self):
        self.algaeintakeLeftmotor.set(ELEC.algae_speed)
        self.algaeintakeRightmotor.set(-ELEC.algae_speed)
        
    def algaeoutake(self):
        self.algaeintakeLeftmotor.set(-ELEC.algae_speed)
        self.algaeintakeRightmotor.set(ELEC.algae_speed)
    
    def algaestop(self):
        self.algaeintakeLeftmotor.set(0)
        self.algaeintakeRightmotor.set(0)


        

