import wpilib
import commands2
import phoenix6
from constants import ELEC

class ElevatorSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        self.topWristmotor = phoenix6.hardware.TalonFX(ELEC.TopElevatorMotor_ID)
        self.bottomWristmotor = phoenix6.hardware.TalonFX(ELEC.BottomElevatorMotor_ID)
        self.brakemode = phoenix6.signals.NeutralModeValue(ELEC.elevator_neutral_mode)
        self.topWristmotor.setNeutralMode(self.brakemode)
        self.bottomWristmotor.setNeutralMode(self.brakemode)

    def wristwithjoystick(self, joystickinput):
        self.calculatedinput = joystickinput * ELEC.elevator_speed_multiplier
        self.topWristmotor.set(self.calculatedinput)
        self.bottomWristmotor.set(self.calculatedinput)

    def elevatorMotorStop(self):
        self.topWristmotor.set(0)
        self.bottomWristmotor.set(0)
        