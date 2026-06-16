import socket
import struct
import uinput

BIP = '192.168.1.106'#bind ip
BORT = 5005# bind port
X_MAX = 1920
Y_MAX = 1080

events = (
    uinput.ABS_X + (0, X_MAX, 0, 0),
    uinput.ABS_Y + (0, Y_MAX, 0, 0),
    uinput.BTN_LEFT,
    uinput.BTN_RIGHT,
)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((BIP, BORT))

print(f"Connected {BIP}:{BORT}...")
print(f"mirroring on {X_MAX}x{Y_MAX}")

with uinput.Device(events, name="vmouse_mirror") as device:
    try:
        while True:
            data, addr = server_socket.recvfrom(4)
            
            if len(data) == 4:
                target_x, target_y = struct.unpack('!HH', data)
                
                device.emit(uinput.ABS_X, target_x, syn=False)
                device.emit(uinput.ABS_Y, target_y, syn=True)
                
                print(f" mirrored to {target_x}, Y: {target_y}")
                

    finally:
        server_socket.close()