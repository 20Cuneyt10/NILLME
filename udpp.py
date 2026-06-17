import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('192.168.1.106', 5005))

print("Server listening on port 5005")

while True:
    data, addr = server_socket.recvfrom(1024)
    print(f"message: {data.decode()} from {addr}")
    