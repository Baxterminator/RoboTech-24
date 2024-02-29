from dataclasses import dataclass
from enum import Enum
import math
from typing import Iterator
from scipy.spatial.transform.rotation import Rotation

from _calibration import CalibrationData
from _custom_types import Pose, JointState, EULER_CONV
from _path_utils import generate_grid_pos, gen_circle_path


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

    # Current working state
    input_idx: int = 0
    read_idx: int = 0
    defect_idx: int = 0
    step: Step = Step.IDLE

    def n_cells(self) -> int:
        return self.calib.input_bin.ncol * self.calib.input_bin.nrow

    def is_done(self) -> bool:
        return self.n_cells() <= self.input_idx

    def cpath(self, fr: Pose, to: Pose) -> Iterator[Pose]:
        for p in gen_circle_path(fr, to, self.calib.gen_angle_max):
            yield p

    # =========================================================================
    # Input move position computations
    # =========================================================================
    def _get_input_pos(self) -> Pose:
        """
        Get the input position for the current cartridge index.
        """
        return generate_grid_pos(
            self.calib.input_bin.origin,
            self.calib.input_bin.drow,
            self.calib.input_bin.dcol,
            self.calib.input_bin.nrow,
            self.calib.input_bin.ncol,
            self.input_idx,
        )

    def get_safe_input_pos(self) -> JointState:
        """
        Get the safe position for moving between bins
        """
        return self.calib.input_bin.safe

    def get_input_grabbing_pos(self) -> Pose:
        """
        Get the input grabbing position for the state's cartridge.
        Goes with row first, then col.
        """
        p = self._get_input_pos()

        # Rotate 45°
        RPY = p.rot.as_euler(EULER_CONV)
        # RPY[2] += math.pi / 2

        return Pose(p.x, p.y, p.z, Rotation.from_euler(EULER_CONV, RPY))

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
    def _get_good_pos(self) -> Pose:
        """
        Get the good bin position for the current cartridge index.
        """
        return generate_grid_pos(
            self.calib.good_bin.origin,
            self.calib.good_bin.drow,
            self.calib.good_bin.dcol,
            self.calib.good_bin.nrow,
            self.calib.good_bin.ncol,
            self.read_idx,
        )

    def get_safe_good_pos(self) -> JointState:
        """
        Get the safe position for moving between bins
        """
        return self.calib.good_bin.safe

    def get_good_dropping_pos(self) -> Pose:
        """
        Get the good output bin dropping position for the state's cartridge.
        Goes with row first, then col.
        """
        p = self._get_good_pos()

        # Rotate 45°
        RPY = p.rot.as_euler(EULER_CONV)
        # RPY[2] += math.pi / 2

        return Pose(p.x, p.y, p.z, Rotation.from_euler(EULER_CONV, RPY))

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
    def _get_defect_pos(self) -> Pose:
        """
        Get the good bin position for the current cartridge index.
        """
        return generate_grid_pos(
            self.calib.defect_bin.origin,
            self.calib.defect_bin.drow,
            self.calib.defect_bin.dcol,
            self.calib.defect_bin.nrow,
            self.calib.defect_bin.ncol,
            self.read_idx,
        )

    def get_safe_defect_pos(self) -> JointState:
        """
        Get the safe position for moving between bins
        """
        return self.calib.defect_bin.safe

    def get_defect_dropping_pos(self) -> Pose:
        """
        Get the good output bin dropping position for the state's cartridge.
        Goes with row first, then col.
        """
        p = self._get_defect_pos()

        # Rotate 45°
        RPY = p.rot.as_euler(EULER_CONV)
        # RPY[2] += math.pi / 2

        return Pose(p.x, p.y, p.z, Rotation.from_euler(EULER_CONV, RPY))

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
    def get_checking_approach_pos(self) -> JointState:
        """
        Get the checking approaching position.
        """
        return self.calib.checking_approach

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

    def get_defect_checking_pos2(self) -> JointState:
        """
        Get the position of to check the defects on the cartridge.
        """
        return self.calib.defect_checking2
