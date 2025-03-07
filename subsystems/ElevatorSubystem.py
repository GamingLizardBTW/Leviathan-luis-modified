import wpilib
import commands2
import phoenix6
from constants import ELEC

class ElevatorSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        self.bottomSwitch = wpilib.DigitalInput(0)
        self.topmotor = phoenix6.hardware.TalonFX(ELEC.TopElevatorMotor_ID)
        self.bottommotor = phoenix6.hardware.TalonFX(ELEC.BottomElevatorMotor_ID)
        self.brakemode = phoenix6.signals.NeutralModeValue(ELEC.elevator_neutral_mode)
        self.topmotor.setNeutralMode(self.brakemode)
        self.bottommotor.setNeutralMode(self.brakemode)

    def wristwithjoystick(self, joystickinput):
        calculatedinput = joystickinput * ELEC.elevator_speed_multiplier
        if self.bottomSwitch.get() is False and joystickinput > 0:
            self.topmotor.set(0)
            self.bottommotor.set(0)
        else:
            self.topmotor.set(calculatedinput)
            self.bottommotor.set(calculatedinput)

    def elevatorMotorStop(self):
        self.topmotor.set(0)
        self.bottommotor.set(0)
        