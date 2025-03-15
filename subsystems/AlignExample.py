import DrivetrainSubsystem
import wpilib
from photonlibpy import PhotonCamera
from constants import OP

VISION_TURN_kP = 0.01


class MyRobot(wpilib.TimedRobot):
#     def robotInit(self) -> None:
#         """Robot initialization function"""
#         self.controller = wpilib.XboxController(0)
#         self.swerve = DrivetrainSubsystem.drivetrainSubsystemClass()
#         self.cam = PhotonCamera("YOUR CAMERA NAME")

#     def robotPeriodic(self) -> None:
#         self.swerve.updateOdometry()
#         # self.swerve.log()

#     def teleopPeriodic(self) -> None:
#         xSpeed = -1.0 * self.controller.getLeftY() * OP.max_speed
#         ySpeed = -1.0 * self.controller.getLeftX() * OP.max_speed
#         rot = -1.0 * self.controller.getRightX() * OP.max_turn_speed

#         # Get information from the camera
#         targetYaw = 0.0
#         targetVisible = False
#         results = self.cam.getAllUnreadResults()
#         if len(results) > 0:
#             result = results[-1]  # take the most recent result the camera had
#             for target in result.getTargets():
#                 if target.getFiducialId() == 7:
#                     # Found tag 7, record its information
#                     targetVisible = True
#                     targetYaw = target.getYaw()

#         if self.controller.getAButton() and targetVisible:
#             # Driver wants auto-alignment to tag 7
#             # And, tag 7 is in sight, so we can turn toward it.
#             # Override the driver's turn command with an automatic one that turns toward the tag.
#             rot = -1.0 * targetYaw * VISION_TURN_kP * OP.max_turn_speed

        # self.swerve.drive(xSpeed, ySpeed, rot, True, self.getPeriod())
        pass