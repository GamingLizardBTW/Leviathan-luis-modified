import wpilib
from phoenix6 import controls, hardware, configs
import commands2
import wpilib.drive
import wpimath
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.kinematics import (
    SwerveDrive4Kinematics,
    SwerveDrive4Odometry,
    ChassisSpeeds,
    SwerveModuleState,
)
from navx import AHRS

class SwerveModule:
    def __init__(self,
                 driveMotorID: int, 
                 turnMotorID: int, 
                 turnAbsoluteEncoderID: int) -> None:
        
        self.driveMotor = hardware.TalonFX(driveMotorID)
        self.turnMotor = hardware.TalonFX(turnMotorID)

        self.driveMotorOutput = controls.DutyCycleOut(0)
        self.TurnMotoOutput = controls.DutyCycleOut(0)

        self.driveMotor.setNeutralMode(1)
        self.turnMotor.setNeutralMode(1)
        #coast is 0, brake is 1

        self.turnAbsoluteEncoder = wpilib.DutyCycleEncoder(turnAbsoluteEncoderID)
        self.driveMotor.get_velocity

    def getState(self) -> SwerveModuleState:
        
        return SwerveModuleState()


