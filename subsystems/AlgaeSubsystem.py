import wpilib
import phoenix6
import commands2
from constants import ELEC

class AlgaeSubsystemClass(commands2.Subsystem):
    def __init__(self) -> None:
        self.algaeintakeLeftmotor = phoenix6.hardware.TalonFX(ELEC.algae_leftmotor_CAN_ID)
        self.algaeintakeRightmotor = phoenix6.hardware.TalonFX(ELEC.algae_rightmotor_CAN_ID)

        
    
    def algaeintake(self):
        self.algaeintakeLeftmotor.set(0.5)
        self.algaeintakeRightmotor.set(-0.5)
        
    def algaeoutake(self):
        self.algaeintakeLeftmotor.set(-0.5)
        self.algaeintakeRightmotor.set(0.5)
    
    def algaestop(self):
        self.algaeintakeLeftmotor.set(0)
        self.algaeintakeRightmotor.set(0)


        

