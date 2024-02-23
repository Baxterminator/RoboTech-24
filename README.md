# RoboTech Challenge 2024 Code

This repository contains both the Python server and the UR3e client program for communication and challenge behavior computations.

## Run the server

To run the python server: 

```shell
python3 python/robotech.py {run, cmd}
```

There are actually two options to run the server:

- **run** to run the sequencer
- **cmd** to open a console to speak directly with the UR3e client

## PLC <-> Python Communication

We are using MQTT protocol. 

1. Start the mosquitto broker

```shell
mosquitto -v -c mqtt/mosquitto.conf
```

2. To monitor nodes/topics use node-red

```shell
node-red
```

3. That's it, you can now publish and subscribe to topics in Python and PLC!

(tomorrow I'll post some pictures from PLC)
