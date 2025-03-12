import wpilib
import commands2
import phoenix6

from wpilib import LEDPattern
from constants import ELEC

class LedSubsystem(commands2.subsystem):
    def init_(self) -> None:
        print("Led Start")
        
        # Create Led instance
        self.Led = wpilib.AddressableLED(2)
        
        # Set Length
        self.Led.setLength(180)
        
        #Create an LED Data Object
        self.left = wpilib.AddressableLED.LEDData(255, 0, 0)
        
        self.Led.ColorOrder(5)