import socket

# Initialize UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.1.106', 5005)

try:
    message = b"Ping"
    print(f"Sending: {message.decode()}")
    client_socket.sendto(message, server_address)
    
    # Wait for server ACK (Blocks until received)
    data, server = client_socket.recvfrom(1024)
    print(f"Server response: {data.decode()}")

finally:
    client_socket.close()