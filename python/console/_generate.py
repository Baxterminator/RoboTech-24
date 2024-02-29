from common import State
from common.configs import BinCalibration
from common.utils import generate_grid_pos, EULER_CONV
import numpy as np


def gen_all_pos(bin: BinCalibration) -> None:
    for i in range(bin.ncol * bin.nrow):
        p = generate_grid_pos(bin.origin, bin.drow, bin.dcol, bin.nrow, bin.ncol, i)
        r = p.rot.as_matrix()
        print(f'[{p.x},{p.y},{p.z},{np.array2string(r, separator=",")}],')


def gen_action(state: State, args: dict[str]):
    match args[0]:
        case "input":
            print("[")
            gen_all_pos(state.calib.input_bin)
            print("]")
        case "good":
            print("[")
            gen_all_pos(state.calib.good_bin)
            print("]")
        case "defect":
            print("[")
            gen_all_pos(state.calib.defect_bin)
            print("]")
        case "all":
            print("[")
            gen_all_pos(state.calib.input_bin)
            gen_all_pos(state.calib.good_bin)
            gen_all_pos(state.calib.defect_bin)
            print("]")
