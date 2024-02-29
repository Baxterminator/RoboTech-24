

import socket

def read_from_tcp_server(ip, port):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((ip, port))
        print("Connected to the server")
        
        # Receive data from the serve
        print("Trying to receive data...")
        data = client_socket.recv(1024)  # Adjust buffer size as needed
        print("Received:", data.decode("utf-8"))  # Assuming data is encoded in UTF-8
    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Close the socket
        client_socket.close()

# Example usage
server_ip = '10.13.15.6'  # Replace with the server's IP address
server_port = 5000  # Replace with the server's port
read_from_tcp_server(server_ip, server_port)