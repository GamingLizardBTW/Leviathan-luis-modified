import wpilib
import wpimath
import commands2
import wpimath.filter
from subsystems.DrivetrainSubsystem import drivetrainSubsystemClass
from subsystems.VisionSubsystem import visionSubsystem
import logging
logger = logging.getLogger("Drivetrain Logger")
from wpilib import XboxController
from constants import OP, PHYS, SW

VISION_TURN_kP = 0.01

class driveWithJoystickCommand(commands2.Command):
    def __init__(self, drivetrainSubsystem: drivetrainSubsystemClass, visionSubsystem: visionSubsystem) -> None :
        self.drivetrainSub = drivetrainSubsystem
        self.visionSub = visionSubsystem
        self.xSpeedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.ySpeedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.rotateSpeedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.controller = wpilib.XboxController(OP.driver_controller)
        self.addRequirements(drivetrainSubsystem)
        logger.info("driveWithJoystick constructor")
    
    def initialize(self):
        self.drivetrainSub.resetAllEncoders()
        logger.info("driveWithJoystick initiate")

    def execute(self):
        #forward is positive X and left is positive Y.
        self.leftY = XboxController(OP.driver_controller).getLeftY() #This will be xSpeed(front and back)
        xSpeed = (-self.xSpeedLimiter.calculate(wpimath.applyDeadband(self.leftY, 0.08)) * OP.max_speed)
        #xSpeed = -self.leftY * OP.max_speed

        self.leftX = XboxController(OP.driver_controller).getLeftX() #This will be ySpeed(left and right)
        ySpeed = (-self.ySpeedLimiter.calculate(wpimath.applyDeadband(self.leftX, 0.08)) * OP.max_speed)
        #ySpeed = -self.leftX * OP.max_speed

        self.rightX = XboxController(OP.driver_controller).getRightX()#This will be rotation(turn heading left and right)
        rotationSpeed = (-self.rotateSpeedLimiter.calculate(wpimath.applyDeadband(self.rightX, 0.08)) * OP.max_turn_speed)
        #rotationSpeed = -self.rightX * OP.max_speed
        
        # Create Auto Target
        targetYaw = 0.0
        targetVisible = self.visionSub.hasTargets

        if self.controller.getXButton() and targetVisible:
            targetYaw = self.visionSub.getClosestData("Z-Rot")
            rotationSpeed = (-self.rotateSpeedLimiter.calculate(targetYaw) * OP.max_turn_speed)
            # rotationSpeed = (-1.0 * targetYaw * OP.max_turn_speed * VISION_TURN_kP)

        # self.drivetrainSub.drive(xSpeed, ySpeed, rotationSpeed)

        self.drivetrainSub.drive(xSpeed, ySpeed, rotationSpeed, SW.field_relative, 0.02, self.controller.getRawButtonPressed(8))
        self.drivetrainSub.showAbsoluteEncoderValues()
        self.drivetrainSub.showAbsoluteEncoderValuesInRadians()
        self.drivetrainSub.showSteeringSetpoint()
        self.drivetrainSub.showTurnMotorEncoderValues()
        self.drivetrainSub.showDrivingSpeed()
        self.drivetrainSub.showDesiredSpeed()
        # self.drivetrainSub.showHeading()

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.drivetrainSub.drive(0,0,0,SW.field_relative,0.02, self.controller.getRawButtonPressed(8))