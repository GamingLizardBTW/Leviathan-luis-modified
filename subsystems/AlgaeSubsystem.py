import wpilib
import phoenix6
import commands2

class AlgaeSubsystemClass(commands2.Subsystem):
    def __init__(self) -> None:
        self.algaeintakeLeftmotor = phoenix6.hardware.TalonFX(1)
        self.algaeintakeRightmotor = phoenix6.hardware.TalonFX(0)
    
    def algaeintake(self):
        self.algaeintakeLeftmotor.set(0.5)
        self.algaeintakeRightmotor.set(-0.5)
        
    def algaeoutake(self):
        self.algaeintakeLeftmotor.set(-0.5)
        self.algaeintakeRightmotor.set(0.5)
    
    def algaestop(self):
        self.algaeintakeLeftmotor.set(0)
        self.algaeintakeRightmotor.set(0)


        

