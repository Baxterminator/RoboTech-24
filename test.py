import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import time

# HOSTNAME = "172.21.222.200"  # test one
HOSTNAME = "10.13.15.156"  # nne wifi one


def send_msg_plc(msg):
    publish.single("PLC", msg, hostname=HOSTNAME)


def wait_msg_plc():
    msg = subscribe.simple("PLC", hostname=HOSTNAME)
    while not msg:
        msg = subscribe.simple("PLC", hostname=HOSTNAME)
    return msg.payload


def get_qr_code():
    send_msg_plc("0")  # reset
    time.sleep(0.100)
    send_msg_plc("1")  # trigon
    time.sleep(0.200)
    send_msg_plc("0")  # resetV
    time.sleep(0.100)
    send_msg_plc("2")  # trigoff
    time.sleep(0.1)
    send_msg_plc("3")  # publish
    qr = wait_msg_plc()
    send_msg_plc("0")
    return qr


def get_faulty_status():
    # TODO
    pass


if __name__ == "__main__":
    # print(wait_msg_plc())
    print(get_qr_code())
# # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, reason_code, properties):
#     print(f"Connected with result code {reason_code}")
#     # Subscribing in on_connect() means that if we lose the connection and
#     # reconnect then subscriptions will be renewed.
#     client.subscribe("PLC")
#
#
# # The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     print(msg.topic + " " + str(msg.payload))
#
#
# mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# mqttc.on_connect = on_connect
# mqttc.on_message = on_message
#
# mqttc.connect("10.13.15.187", 1883, 60)
#
# # Blocking call that processes network traffic, dispatches callbacks and
# # handles reconnecting.
# # Other loop*() functions are available that give a threaded interface and a
# # manual interface.
# mqttc.loop_forever()
