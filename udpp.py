import socket

# Initialize UDP socket (SOCK_DGRAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('192.168.1.106', 5005))

print("UDP Server listening on port 5005...")

while True:
    # Buffer size is 1024 bytes
    data, addr = server_socket.recvfrom(1024)
    print(f"Received message: {data.decode()} from {addr}")
    
    # Optional: Send response back to client
    server_socket.sendto(b"ACK", addr)