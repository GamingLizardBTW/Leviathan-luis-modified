import wpilib
import commands2
import phoenix6
from constants import ELEC

class WristSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        self.wristmotor = phoenix6.hardware.TalonFX(ELEC.wrist_motor_CAN_ID) 
        self.brakemode = phoenix6.signals.NeutralModeValue(ELEC.wrist_neutral_mode)
        self.wristmotor.setNeutralMode(self.brakemode)

    def wristwithjoystick(self, joystickinput):
        self.calculatedinput = joystickinput * 0.5
        self.wristmotor.set(self.calculatedinput)

    def wristmotorstop(self):
        self.wristmotor.set(0)