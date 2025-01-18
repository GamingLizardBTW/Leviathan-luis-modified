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

import constants

class SwerveModule:
    def __init__(self,
                 driveMotorID: int, 
                 turnMotorID: int, 
                 turnAbsoluteEncoderID: int) -> None:
        
        self.driveMotor = hardware.TalonFX(driveMotorID)
        self.turnMotor = hardware.TalonFX(turnMotorID)

        self.driveMotorOutput = controls.DutyCycleOut(0)
        self.TurnMotoOutput = controls.DutyCycleOut(0)

        self.driveMotor.setNeutralMode(constants.OP.driveMotor_neutral)
        self.turnMotor.setNeutralMode(1)(constants.OP.steerMotor_neutral)
        #coast is 0, brake is 1

        self.turnAbsoluteEncoder = wpilib.DutyCycleEncoder(turnAbsoluteEncoderID)
        

    def getState(self) -> SwerveModuleState:
        self.swerveModuleMeterPerSecond = (
            self.driveMotor.get_rotor_velocity() / 
            (constants.MECH.swerve_module_driving_gearing_ratio) * 
            (constants.MECH.wheel_circumference_in_inch) * 
            (constants.CVR.meterPerInch)
        )
        return SwerveModuleState(self.swerveModuleMeterPerSecond, self.turnAbsoluteEncoder.get())


