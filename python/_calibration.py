from dataclasses import dataclass
import math
import yaml
import os

from _custom_types import JointState, Pose, Vec2, Vec3
from _custom_logger import LoggingInterface

DEFAULT_DZ_APPROACH = 0.05


@dataclass
class BinCalibration:
    origin: Vec3
    dz: float = DEFAULT_DZ_APPROACH

    drow: Vec2 = Vec2(0.0, 0.0)
    dcol: Vec2 = Vec2(0.0, 0.0)

    nrow: int = 1
    ncol: int = 1

    @staticmethod
    def from_dict(d: dict) -> "BinCalibration":
        bin = BinCalibration(Vec3(0, 0, 0))

        if "origin" in d.keys() and len(d["origin"]) >= 3:
            # Save origin position and make the right orientation for the tool
            o = d["origin"]
            bin.origin = Vec3(o[0], o[1], o[2])
        if "app_dz" in d.keys():
            bin.dz = d["app_dz"]
        if "drow" in d.keys() and len(d["drow"]) >= 2:
            bin.drow = Vec2(d["drow"][0], d["drow"][1])
        if "dcol" in d.keys() and len(d["dcol"]) >= 2:
            bin.dcol = Vec2(d["dcol"][0], d["dcol"][1])
        if "nrow" in d.keys():
            bin.nrow = d["nrow"]
        if "ncol" in d.keys():
            bin.ncol = d["ncol"]

        return bin

    def __repr__(self) -> str:
        s = "Bin:\n"
        s += f"\t\tOrigin: {self.origin}\n"
        s += f"\t\tDz: {self.dz}\n"
        s += f"\t\tDrow: {self.drow}, Dcol: {self.dcol}\n"
        s += f"\t\tNrow: {self.nrow}, Ncol: {self.ncol}\n"
        return s


@dataclass
class CalibrationData:
    gen_angle_max: float = 15 * math.pi / 180  # In radians
    grabbing_time: float = 0.2

    input_bin: BinCalibration = BinCalibration(Vec3(0, 0, 0))
    good_bin: BinCalibration = BinCalibration(Vec3(0, 0, 0))
    defect_bin: BinCalibration = BinCalibration(Vec3(0, 0, 0))

    checking_approach: JointState = JointState(0, 0, 0, 0, 0, 0)
    qr_checking: JointState = JointState(0, 0, 0, 0, 0, 0)
    defect_checking: JointState = JointState(0, 0, 0, 0, 0, 0)

    @staticmethod
    def load_from_file(f: str) -> "CalibrationData":
        # Check if file exist
        if os.path.exists(f):
            with open(f, "r") as calib_file:
                try:
                    data = dict(yaml.safe_load(calib_file))
                    if "calibration" in data.keys():
                        return CalibrationData._load_from_dict(data["calibration"])
                    return CalibrationData()
                except yaml.YAMLError as e:
                    LoggingInterface.serror("YAML Error when loading calib files")
                    return CalibrationData()
        else:
            LoggingInterface.swarn("Given calib file doesn't exist")
            return CalibrationData()

    @staticmethod
    def _load_from_dict(d: dict) -> "CalibrationData":
        out = CalibrationData()

        # Path Circle Generation Parameters
        if "max-gen-angle" in d.keys():
            out.gen_angle_max = d["max-gen-angle"] * math.pi / 180

        if "grab-time" in d.keys():
            out.grabbing_time = d["grab-time"]

        # Bin calibrations
        if "input" in d.keys():
            out.input_bin = BinCalibration.from_dict(d["input"])
        if "good" in d.keys():
            out.good_bin = BinCalibration.from_dict(d["good"])
        if "defect" in d.keys():
            out.defect_bin = BinCalibration.from_dict(d["defect"])

        # Checking positions
        if "checking-approach" in d.keys():
            cpos = d["checking-approach"]
            out.checking_approach = JointState(
                cpos[0], cpos[1], cpos[2], cpos[3], cpos[4], cpos[5], deg=True
            )

        if "qr-code" in d.keys():
            cpos = d["qr-code"]
            out.qr_checking = JointState(
                cpos[0], cpos[1], cpos[2], cpos[3], cpos[4], cpos[5], deg=True
            )
        if "defect-check" in d.keys():
            cpos = d["defect-check"]
            out.defect_checking = JointState(
                cpos[0], cpos[1], cpos[2], cpos[3], cpos[4], cpos[5], deg=True
            )

        return out

    def __repr__(self) -> str:
        s = "Calibration:\n"
        s += f"\tChecking approach position: {self.checking_approach}\n"
        s += f"\tQR code position: {self.qr_checking}\n"
        s += f"\tDefect position: {self.defect_checking}\n"
        s += f"\tInput: {self.input_bin}"
        s += f"\tGood: {self.good_bin}"
        s += f"\tDefect: {self.defect_bin}"
        return s
