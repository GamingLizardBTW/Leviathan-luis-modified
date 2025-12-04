# import wpilib
# import wpimath
# import wpimath.filter
# import commands2
# import logging
# from subsystems.DrivetrainSubsystem import drivetrainSubsystemClass
# from constants import OP, SW

# logger = logging.getLogger("Drivetrain Logger")

# VISION_TURN_kP = 0.01

# class driveWithJoystickCommand(commands2.CommandBase):
#     """
#     Default command for the swerve drivetrain.
#     Uses one persistent XboxController and updates swerve modules every execute cycle.
#     """
    
#     def __init__(self, drivetrainSubsystem: drivetrainSubsystemClass) -> None:
#         super().__init__()
#         self.drivetrainSub = drivetrainSubsystem
#         self.addRequirements(drivetrainSubsystem)

#         # Single persistent XboxController instance
#         self.controller = wpilib.XboxController(OP.driver_controller)

#         # Slew rate limiters for smooth motion
#         self.xSpeedLimiter = wpimath.filter.SlewRateLimiter(3)
#         self.ySpeedLimiter = wpimath.filter.SlewRateLimiter(3)
#         self.rotateSpeedLimiter = wpimath.filter.SlewRateLimiter(3)

#         logger.info("driveWithJoystickCommand initialized")

#     def execute(self):
#         # ----------------------------
#         # Read joystick inputs
#         # ----------------------------
#         leftY = self.controller.getLeftY()  # Forward/backward
#         leftX = self.controller.getLeftX()  # Left/right
#         rightX = self.controller.getRightX()  # Rotation

#         # Apply deadband and slew rate, then scale by max speed
#         xSpeed = -self.xSpeedLimiter.calculate(wpimath.applyDeadband(leftY, 0.08)) * OP.max_speed
#         ySpeed = -self.ySpeedLimiter.calculate(wpimath.applyDeadband(leftX, 0.08)) * OP.max_speed
#         rotationSpeed = -self.rotateSpeedLimiter.calculate(wpimath.applyDeadband(rightX, 0.08)) * OP.max_turn_speed

#         # ----------------------------
#         # Override rotation if buttons pressed
#         # ----------------------------
#         if self.drivetrainSub.shouldFlipPath() is False:
#             rotateAroundReef = self.drivetrainSub.rotateToBlueReef()
#         else:
#             rotateAroundReef = self.drivetrainSub.rotateToRedReef()

#         if self.controller.getRawButton(4):
#             rotationSpeed = self.drivetrainSub.rotateToBarge()
#         elif self.controller.getRawButton(3):
#             rotationSpeed = self.drivetrainSub.rotateToLeftHuman()
#         elif self.controller.getRawButton(2):
#             rotationSpeed = self.drivetrainSub.rotateToRightHuman()
#         elif self.controller.getRawButton(1):
#             rotationSpeed = rotateAroundReef
#         # else: rotationSpeed already set from rightX

#         # ----------------------------
#         # Drive the robot
#         # ----------------------------
#         self.drivetrainSub.drive(
#             xSpeed, 
#             ySpeed, 
#             rotationSpeed, 
#             SW.field_relative, 
#             0.02, 
#             self.controller.getRawButtonPressed(8)
#         )

#         # ----------------------------
#         # Optional: debug values on dashboard
#         # ----------------------------
#         self.drivetrainSub.showAbsoluteEncoderValues()
#         self.drivetrainSub.showAbsoluteEncoderValuesInRadians()
#         self.drivetrainSub.showSteeringSetpoint()
#         self.drivetrainSub.showTurnMotorEncoderValues()
#         self.drivetrainSub.showDrivingSpeed()
#         self.drivetrainSub.showDesiredSpeed()

#     def isFinished(self) -> bool:
#         return False

#     def end(self, interrupted: bool) -> None:
#         # Stop the robot when command ends
#         self.drivetrainSub.drive(0, 0, 0, SW.field_relative, 0.02, self.controller.getRawButtonPressed(8))
