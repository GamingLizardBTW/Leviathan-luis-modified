import wpilib
import phoenix6
import commands2   
from constants import ELEC
class CoralSubsystemClass(commands2.Subsystem):
    def __init__(self) -> None:
        self.coralintakeleftmotor = phoenix6.hardware.TalonFX(ELEC.coral_leftmotor_CAN_ID)
        self.coralintakerightmotor = phoenix6.hardware.TalonFX(ELEC.coral_rightmotor_CAN_ID)
        self.breakmode = phoenix6.signals.NeutralModeValue(ELEC.coral_neutral_mode)
        self.coralintakeleftmotor.setNeutralMode(self.breakmode)
        self.coralintakerightmotor.setNeutralMode(self.breakmode)

    def coralintake(self):
        self.coralintakeleftmotor.set(-ELEC.coral_speed)
        self.coralintakerightmotor.set(ELEC.coral_speed)

    def coralouttake(self):
        self.coralintakeleftmotor.set(ELEC.coral_speed)
        self.coralintakerightmotor.set(-ELEC.coral_speed)

    def coralstop(self):
        self.coralintakeleftmotor.set(0)
        self.coralintakerightmotor.set(0)

