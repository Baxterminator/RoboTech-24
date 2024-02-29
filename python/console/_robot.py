from typing import List
from proxies import RobotProxy
from common import State


def move_to(state: State, prox: RobotProxy, args: List[str]):
    match args[0]:
        case "input":
            state.input_idx = int(args[1])
            prox.movej(state.get_input_grabbing_approach_pos())
        case "good":
            state.read_idx = int(args[1])
            prox.movej(state.get_good_dropping_approach_pos())
        case "defect":
            state.defect_idx = int(args[1])
            prox.movej(state.get_defect_dropping_approach_pos)


def robot_action(robot: RobotProxy, state: State, args: dict[str]):
    match args[0]:
        case "move":
            move_to(state, robot, args[1:])
        case _:
            result = robot.send(args[0])
    if not result:
        return True
    else:
        robot._info(f"Response: {result}")
        return False
