from enum import Enum
import paho.mqtt.publish as mqtt_pub
import paho.mqtt.subscribe as mqtt_sub


class BaseMessage(Enum):
    RESET = "0"


class MQTTProxy:

    def __init__(self, broker_ip: str, topic: str) -> None:
        self.broker_ip = broker_ip
        self.topic = topic

    # =========================================================================
    # General Purpose Functions
    # =========================================================================

    def _send_msg(self, msg: str) -> None:
        print(self.broker_ip)
        mqtt_pub.single(self.topic, msg, self.broker_ip)

    def _receive_msg(self) -> str:
        msg = mqtt_sub.simple(self.topic, hostname=self.broker_ip)

        while not msg:
            msg = mqtt_sub.simple(self.topic, hostname=self.broker_ip)
        return msg.payload

    def _reset(self) -> None:
        self._send_msg(BaseMessage.RESET)
