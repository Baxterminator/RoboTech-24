from enum import Enum
import paho.mqtt.publish as mqtt_pub
import paho.mqtt.subscribe as mqtt_sub
from time import perf_counter


class BaseMessage(Enum):
    RESET = "0"
    PUBLISH = "3"


class MQTTProxy:

    def __init__(self, broker_ip: str, topic: str, timeout: float = 1) -> None:
        self.broker_ip = broker_ip
        self.topic = topic
        self.timeout = timeout

    # =========================================================================
    # General Purpose Functions
    # =========================================================================

    def _send_msg(self, msg: str) -> None:
        """
        Send a message to the MQTT network.
        """
        mqtt_pub.single(self.topic, msg, self.broker_ip)

    def _receive_msg(self) -> bytes:
        """
        Try to receive a message from the MQTT network.
        If timeout, return byte '\ x00'
        """
        msg = mqtt_sub.simple(self.topic, hostname=self.broker_ip)
        start = perf_counter()
        while perf_counter() - start < self.timeout:
            msg = mqtt_sub.simple(self.topic, hostname=self.broker_ip)
            if not msg:
                continue
            return msg.payload
        return b"\x00"

    def _reset(self) -> None:
        self._send_msg(BaseMessage.RESET)

    def _publish(self):
        """
        Ask for data publishing
        """
        self._send_msg(BaseException.PUBLISH)
