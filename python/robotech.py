from argparse import ArgumentParser
from sequencer import CartridgeSequencer
from robot_proxy import RobotProxy
from robot_console import robot_console

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "action",
        choices=["run", "cmd"],
        required=True,
        help="Use run to use the sequencer, cmd for direction robot console",
    )
    args = parser.parse_args()

    robot = RobotProxy("10.13.15.50", 1500)

    match args.action:
        case "cmd":
            robot_console(robot)
        case "run":
            seq = CartridgeSequencer(robot)
            seq.run()
        case "_":
            print("Unknown command!")
    robot.close_connection()
