from dataclasses import dataclass

from ..utils._yaml_loader import YAMLFile
from ..utils._custom_logger import LoggingInterface


import os


@dataclass
class ConfigurationFile(YAMLFile):
    calib_file: str = ""

    # Robot
    robot_ip: str = "127.0.0.1"
    robot_port: int = 1500

    # MQTT
    mqtt_ip: str = "127.0.0.1"
    mqtt_port: int = 1883

    def __init__(self):
        super().__init__("Config")

    def _parse_from_data(self, data: dict) -> None:
        if "calibration" in data.keys():
            self.calib_file = data["calibration"]
        if "robot" in data.keys():
            if "ip" in data["robot"].keys():
                self.robot_ip = data["robot"]["ip"]
            if "port" in data["robot"].keys():
                self.robot_port = data["robot"]["port"]
        if "mqtt" in data.keys():
            self.__load_mqtt_config(data["mqtt"])
        if "logger-level" in data.keys():
            LoggingInterface.configure_lvl(data["logger-level"])

    def __load_mqtt_config(self, conf_file: str) -> None:
        if not os.path.exists(conf_file):
            self._warn("MQTT configuration file doesn't exist")
            return
        with open(conf_file, "r") as mqtt_conf:
            l = mqtt_conf.readline()
            while l != "":
                if l.startswith("listener"):
                    args = l.strip().split(" ")[1:]
                    self.mqtt_ip = args[1]
                    self.mqtt_port = int(args[0])
                    break

    def __repr__(self) -> str:
        s = "Configuration:\n"
        s += f"\tCalib file: {self.calib_file}\n"
        s += f"\tRobot: {self.robot_ip}:{self.robot_port}\n"
        s += f"\tMQTT: {self.mqtt_ip}:{self.mqtt_port}"
        return s
