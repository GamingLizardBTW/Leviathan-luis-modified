import wpilib
import commands2
import phoenix6

class WristSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        self.wristmotor = phoenix6.hardware.TalonFX(0) 
        self.wristmotoroutput = phoenix6.controls.DutyCycleOut(0)

    def wristwithjoystick(self, joystickinput):
        self.calculatedinput = joystickinput * 0.5
        self.wristmotor.set_control(self.wristmotoroutput.with_output(self.calculatedinput))

    def wristmotorstop(self):
        self.wristmotor.set_control(self.wristmotoroutput.with_output(0))