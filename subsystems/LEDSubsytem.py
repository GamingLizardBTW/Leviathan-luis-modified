import logging
logger = logging.getLogger('LED-subsystem')

import wpilib
import commands2
from constants import ELEC

class LED_5v_Subsystem(commands2.Subsystem):
    """
    This class represents a subsystem of individually addressable LEDs.

    The following terms are all equivalent:
     * addressable LED strip
     * individually addressable LED strip
     * 5-volt LED strip
     * three-wire LED strip
     * different LEDs can be set to different colors at the same time

    THE OPPOSITE can be described with the following equivalent terms:
     * 12-volt LED strip
     * four-wire LED strip
     * LED strip that *requires* a Blinkin-style controller
     * all LEDs must be the same color (which can change, but all LEDs change)
    """
    def __init__(self, pwm_port, speed=1.0, length=ELEC.LED_length) -> None:
        """
        Constructor for our LED subsystem.
        Parameters:
          pwm_port (int): the number of the PWM port that the LED strip is
              plugged into
          speed (float): number of seconds between changes to the LED pattern
          length (int): number of active LEDs in the strip
        """
        super().__init__()
        self.length = length
        self.port = pwm_port
        self.leds = wpilib.AddressableLED(self.port)
        self.speed = speed
        self.timer = wpilib.Timer()
        self.timer.start()

        # Whats the default color
        self.data = self.white(self.length)
        

        self.leds.setLength(self.length)
        self.leds.setData(self.data)
        self.leds.start()
        logger.info("Initialized LED subsystem")


    def set_led_color(self, color):
        """Update LED color."""
        print(f"Changing LED color to: {color}")  # Debugging print
        led_data = [wpilib.AddressableLED.LEDData(*color)] * self.length
        self.leds.setData(led_data)
        self.leds.start()  # Apply changes


    # @classmethod
    # def red(cls, length):
    #     """
    #     Return a list of colors (as LEDData objects) that form a rainbow
    #     pattern of the given length.

    #     Parameters:
    #       length (int): number of active LEDs in the strip

    #     Returns:
    #       [LEDData("red"), LEDData("orange"), ...]
    #       with the pattern repeated until the given length is reached
    #       where "red" actually means (255, 0, 0) which is RGB values for red,
    #       and "orange" actually means etc. etc.

    #       In other words, this method returns a list of LEDData objects
    #       representing a rainbow pattern, which can be passed in as a parameter
    #       to self.leds.setData() if you want to set your LEDs to a rainbow.
    #     """
    #     color = (255, 0, 0) #single RGB color

    #     result = []
    #     for _ in range(length):
    #         return [wpilib.AddressableLED.LEDData(255, 0, 0) for _ in range(length)]
    @classmethod
    def white(cls, length):
        """
        Return a list of colors (as LEDData objects) that form a rainbow
        pattern of the given length.

        Parameters:
          length (int): number of active LEDs in the strip

        Returns:
          [LEDData("red"), LEDData("orange"), ...]
          with the pattern repeated until the given length is reached
          where "red" actually means (255, 0, 0) which is RGB values for red,
          and "orange" actually means etc. etc.

          In other words, this method returns a list of LEDData objects
          representing a rainbow pattern, which can be passed in as a parameter
          to self.leds.setData() if you want to set your LEDs to a rainbow.
        """
        color = (255, 255, 255) #single RGB color

        result = []
        for _ in range(length):
            return [wpilib.AddressableLED.LEDData(255, 255, 255) for _ in range(length)]

    
    @classmethod
    def green(cls, length):

        color = (0, 255, 0) #single RGB color

        result = []
        for _ in range(length):
            return [wpilib.AddressableLED.LEDData(0, 255, 0) for _ in range(length)]



    @classmethod
    def off(cls, length):
        """
        Return a list of colors (as LEDData objects) that turn off LEDs in a
        strip of the given length.

        Parameters:
          length (int): number of active LEDs in the strip

        Returns:
          [LEDData("off"), LEDData("off"), ...]
          where "off" actually means (0, 0, 0) which is RGB values for black,
          which turns off the LED

          In other words, this method returns a list of LEDData objects
          representing an LED strip that is turned off, which can be passed
          in as a parameter to self.leds.setData() if you want to turn off
          your LEDs.
        """
        result = []
        for _ in range(length):
            return [wpilib.AddressableLED.LEDData(0, 0, 0) for _ in range(length)]


    def teleopInit(self):
        """
        Turn LED's to red when teleop mode starts.
        """
        self.data = self.red(self.length)
        self.leds.setData(self.data)  # Update LEDs with new color
        self.leds.start()

    def disabledInit(self):
        """
        Turn off all LEDs when disabled mode starts.
        """
        self.data = self.off(self.length)
        self.leds.setData(self.data)  # Update LEDs with new color
        self.leds.start()
