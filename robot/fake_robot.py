import socket
from time import sleep

HOST = "10.13.15.156"  # The server's hostname or IP address
PORT = 1501  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Opening socket!")
    s.connect((HOST, PORT))

    while True:
        data = s.recv(1024)
        # Bad data, close socket
        if not data:
            break
        data = data.decode()
        # If data is empty do nothing
        if len(data) == 0:
            continue

        # Else process cmd
        if data[0] == "#":
            print(data)
            s.sendall("--".encode())
        else:
            print(f'Got cmd: "{data}"')
            if len(data) < 3:
                s.sendall("unknown;".encode())
                continue
            match data[:3]:
                case "gjp":
                    s.sendall("gjp,0,0,0,0,0,0;".encode())
                case "gtp":
                    s.sendall("gtp,0,0,0,0,0,0;".encode())
                case "mvj":
                    s.sendall("mvjok;".encode())
                case "mvl":
                    s.sendall("mvlok;".encode())
                case "gop":
                    s.sendall("gop;".encode())
                case "gcl":
                    s.sendall("gcl;".encode())
                case "std":
                    sleep(2)
                    s.sendall("std;".encode())
                case "stp":
                    s.sendall("stpok;".encode())
                    break
    print("Closing socket !")
