from proxies import RobotProxy
from common import State
from common.utils import Vec3, Vec2


def get_action(robot: RobotProxy, state: State, args: dict[str]):
    pass


def set_action(robot: RobotProxy, state: State, args: dict[str]):

    # Bin
    bin = None
    match args[0]:
        case "input":
            bin = state.calib.input_bin
        case "good":
            bin = state.calib.good_bin
        case "defect":
            bin = state.calib.defect_bin
        case _:
            return

    # What
    match args[1]:
        case "origin":
            result = robot.get_tcp_pose(True)
            if result is None:
                print("Null result")
                return
            bin.origin = Vec3(result.x, result.y, result.z)
        case "drow":
            result = robot.get_tcp_pose(True)
            if result is None:
                print("Null result")
                return
            bin.drow = Vec2(
                0 if bin.nrow <= 1 else (result.x - bin.origin.x) / (bin.nrow - 1),
                0 if bin.nrow <= 1 else (result.y - bin.origin.y) / (bin.nrow - 1),
            )
        case "dcol":
            result = robot.get_tcp_pose(True)
            if result is None:
                print("Null result")
                return
            bin.dcol = Vec2(
                0 if bin.ncol <= 1 else (result.x - bin.origin.x) / (bin.ncol - 1),
                0 if bin.ncol <= 1 else (result.y - bin.origin.y) / (bin.ncol - 1),
            )
        case _:
            return

    state.calib.export()


def calib_action(robot: RobotProxy, state: State, args: dict[str]):
    match args[0]:
        case "set":
            set_action(robot, state, args[1:])
        case "get":
            get_action(robot, state, args[1:])
        case _:
            "Possible choices: {set, get} for calib cmd"
