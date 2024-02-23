from dataclasses import dataclass
import yaml
import os

from _custom_types import Vec3, JointState
from _custom_logger import LoggingInterface

DEFAULT_DZ_APPROACH = 0.05


@dataclass
class BinCalibration:
    origin: Vec3
    dz: float = DEFAULT_DZ_APPROACH

    drow: float = 0.0
    dcol: float = 0.0

    nrow: int = 1
    ncol: int = 1


@dataclass
class CalibrationData:
    input_bin: BinCalibration = BinCalibration(Vec3(0, 0, 0))
    good_bin: BinCalibration = BinCalibration(Vec3(0, 0, 0))
    defect_bin: BinCalibration = BinCalibration(Vec3(0, 0, 0))

    checking_approach: Vec3 = Vec3(0, 0, 0)
    qr_checking: JointState = JointState(0, 0, 0, 0, 0, 0)
    defect_checking: JointState = JointState(0, 0, 0, 0, 0, 0)

    @staticmethod
    def load_from_file(f: str) -> "CalibrationData":
        # Check if file exist
        if os.path.exists(f):
            with open(f, "r") as calib_file:
                try:
                    data = yaml.safe_load(calib_file)
                    print(data)
                    return CalibrationData()
                except yaml.YAMLError as e:
                    LoggingInterface.serror("YAML Error when loading calib files")
                    return CalibrationData()
        else:
            LoggingInterface.swarn("Given calib file doesn't exist")
            return CalibrationData()
