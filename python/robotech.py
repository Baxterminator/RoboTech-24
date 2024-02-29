from argparse import ArgumentParser
from python.common.utils._custom_logger import printHeader, printSection
from python.run._sequencer import CartridgeSequencer
from python.proxies._robot_proxy import RobotProxy
from proxies._lector_proxy import LectorProxy
from python.console._console import robot_console
from common.utils._yaml_loader import YAMLLoader
from common.configs._configuration import ConfigurationFile
from common.configs._calibration import CalibrationData

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "action",
        choices=["run", "cmd"],
        help="Use run to use the sequencer, cmd for direction robot console",
    )
    parser.add_argument(
        "-c",
        "--config",
        help="Configuration file path",
        type=str,
        default="config/main.yaml",
    )
    parser.add_argument(
        "-s",
        "--step",
        action="store_true",
        help="Sequencer should move step by step (requires input for next action)",
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

    config = YAMLLoader[ConfigurationFile].from_file(ConfigurationFile(), args.config)
    calib = YAMLLoader[CalibrationData].from_file(CalibrationData(), config.calib_file)
    print(config)
    print(calib)

    # Create proxies
    robot = RobotProxy(config.robot_ip, config.robot_port)
    lector = LectorProxy(config.mqtt_ip, "PLC")

    # Run everything
    match args.action:
        case "cmd":
            printSection("Console")
            robot_console(robot, lector, calib)
        case "run":
            printSection("Sequencer")
            CartridgeSequencer(robot, calib, args.step).run()
        case _:
            print("Unknown command!")
    robot.close_connection()
