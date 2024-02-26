from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from typing import Iterator

from _calibration import CalibrationData
from _custom_types import Pose, JointState


class Step(Enum):
    IDLE = 0
    MV_INPUT = 1
    CHECK_QR = 2
    CHECK_ANOMALIES = 3
    MV_GOOD_BIN = 4
    MV_BAD_BIN = 5
    END_CARTRIDGE = 6
    DONE = 7


@dataclass
class State:
    calib: CalibrationData
    input_idx: int = 0
    step: Step = Step.IDLE

    def n_cells(self) -> int:
        return self.calib.input_bin.ncol * self.calib.input_bin.nrow

    def is_done(self) -> bool:
        return self.n_cells() <= self.input_idx

    # =========================================================================
    # Input move position computations
    # =========================================================================
    def get_input_grabbing_pos(self) -> Pose:
        """
        Get the input grabbing position for the state's cartridge.
        Goes with row first, then col.
        """
        p = deepcopy(self.calib.input_bin.origin)
        return Pose(p.x, p.y, p.z, p.rx, p.ry, p.rz)

    def get_input_grabbing_approach_pos(self) -> Pose:
        """
        Get the input grabbing approaching position for the state's cartridge.
        Goes with row first, then col.
        """
        p = self.get_input_grabbing_pos()
        p.z += self.calib.input_bin.dz
        return p

    # =========================================================================
    # Good Output position computations
    # =========================================================================
    def get_good_dropping_pos(self) -> Pose:
        """
        Get the good output bin dropping position for the state's cartridge.
        Goes with row first, then col.
        """
        p = deepcopy(self.calib.good_bin.origin)
        return Pose(p.x, p.y, p.z, p.rx, p.ry, p.rz)

    def get_good_dropping_approach_pos(self) -> Pose:
        """
        Get the good output bin dropping approaching position for the state's cartridge.
        Goes with row first, then col.
        """
        p = self.get_good_dropping_pos()
        p.z += self.calib.good_bin.dz
        return p

    # =========================================================================
    # Bad Output position computations
    # =========================================================================
    def get_defect_middle_pos(self) -> Iterator[Pose]:
        """
        Get the good output bin dropping position for the state's cartridge.
        Goes with row first, then col.
        """
        p = self.get_good_dropping_approach_pos()
        return Pose(0, p.y, p.z, p.rx, p.ry, p.rz)

    def get_defect_dropping_pos(self) -> Pose:
        """
        Get the good output bin dropping position for the state's cartridge.
        Goes with row first, then col.
        """
        p = deepcopy(self.calib.defect_bin.origin)
        return Pose(p.x, p.y, p.z, p.rx, p.ry, p.rz)

    def get_defect_dropping_approach_pos(self) -> Pose:
        """
        Get the good output bin dropping approaching position for the state's cartridge.
        Goes with row first, then col.
        """
        p = self.get_defect_dropping_pos()
        p.z += self.calib.defect_bin.dz
        return p

    # =========================================================================
    # Calibration positions
    # =========================================================================
    def get_checking_approach_pos(self) -> Pose:
        """
        Get the checking approaching position.
        """
        p = deepcopy(self.calib.checking_approach)
        return Pose(p.x, p.y, p.z, 0, 0, 0)

    def get_qr_checking_pos(self) -> JointState:
        """
        Get the position of to check the QR code on the cartridge.
        """
        return self.calib.qr_checking

    def get_defect_checking_pos(self) -> JointState:
        """
        Get the position of to check the defects on the cartridge.
        """
        return self.calib.defect_checking
