import commands2
from subsystems.LEDSubsytem import LED_5v_Subsystem

class SetLEDColorCommand(commands2.Command):
    """Command to set the LED color."""

    def __init__(self, led_subsystem: LED_5v_Subsystem, color):
        super().__init__()
        self.led_subsystem = led_subsystem
        self.color = color
        self.addRequirements(self.led_subsystem)

    def initialize(self):
        """Set the LED color when the command starts."""
        
        """Set the LED color when the command starts."""
        print(f"Setting LEDs to {self.color}")  #Debugging print
        self.led_subsystem.set_led_color(self.color)

    def isFinished(self):
        return True  # This is a one-time command