import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

publish.single("PLC", "!", hostname="10.13.15.187")


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
