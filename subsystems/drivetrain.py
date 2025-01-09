import wpilib
import commands2
import wpilib.drive
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.kinematics import (
    SwerveDrive4Kinematics,
    SwerveDrive4Odometry,
    ChassisSpeeds,
    SwerveModuleState,
)
from navx import AHRS
from phoenix6.hardware import TalonFX
from phoenix6.controls import DutyCycleOut

class DrivetrainSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        self.drivesMotor = 