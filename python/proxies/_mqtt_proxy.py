import paho.mqtt.publish as mqtt_pub
import paho.mqtt.subscribe as mqtt_sub
from time import perf_counter
from multiprocessing.pool import ThreadPool


class BaseMessage:
    RESET = "0"
    PUBLISH = "3"


class MQTTProxy:

    def __init__(
        self, broker_ip: str, topic: str, timeout: float = 1, keepalive=1
    ) -> None:
        self.broker_ip = broker_ip
        self.topic = topic
        self.timeout = timeout
        self.keealive = keepalive

    # =========================================================================
    # General Purpose Functions
    # =========================================================================

    def _send_msg(self, msg: str) -> None:
        """
        Send a message to the MQTT network.
        """
        mqtt_pub.single(self.topic, msg, hostname=self.broker_ip)

    def _receive_msg(self) -> bytes:
        """
        Try to receive a message from the MQTT network.
        If timeout, return byte '\ x00'
        """
        msg = mqtt_sub.simple(
            self.topic, hostname=self.broker_ip, keepalive=self.keealive
        )
        return msg.payload

    def _reset(self) -> None:
        self._send_msg(BaseMessage.RESET)

    def _publish(self):
        """
        Ask for data publishing
        """
        self._send_msg(BaseMessage.PUBLISH)
