from argparse import ArgumentParser
from _custom_logger import LoggingInterface, printHeader
from _sequencer import CartridgeSequencer
from _robot_proxy import RobotProxy
from _robot_console import robot_console

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "action",
        choices=["run", "cmd"],
        help="Use run to use the sequencer, cmd for direction robot console",
    )
    parser.add_argument(
        "-c", "--config", help="Configuration file path", type=str, default=""
    )
    parser.add_argument(
        "-l",
        "--lvl",
        help="Define the log level",
        choices=["debug", "info", "warn", "error"],
    )
    args = parser.parse_args()

    printHeader(
        [
            ("RoboTech-2024", False),
            ("Python behaviour sequencer v1.0", False),
            ("Geoffrey Côte", True),
            ("Hassan Hotait ", True),
            ("José Duarte Lopes", True),
            ("Paula Campiña Monzón", True),
        ]
    )

    # Configure logger
    LoggingInterface.configure_lvl(args.lvl)

    # Create proxies
    robot = RobotProxy("127.0.0.1", 1500)

    # Run everything
    match args.action:
        case "cmd":
            robot_console(robot)
        case "run":
            CartridgeSequencer(robot, args.config).run()
        case _:
            print("Unknown command!")
    robot.close_connection()
