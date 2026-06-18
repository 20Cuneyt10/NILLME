import sys
from evdev import InputDevice, list_devices, ecodes as e
import socket
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.1.106', 5005)

X_MAX = 1920
Y_MAX = 1080

abs_x = X_MAX // 2
abs_y = Y_MAX // 2
btn_right = 0
btn_left = 0
wheelup = 0
wheeldown = 0
middleclick = 0
is_grabbed = False

def find_mouse():
    for path in list_devices():
        try:
            device = InputDevice(path)
            if "G305" in device.name:
                return device
        except (PermissionError, OSError):
            continue
    return None

dev = find_mouse()
if not dev:
    print("mouse not detected")
    print("user might not be in input group")
    sys.exit(1)

print(f"tracking {dev.name} [{dev.path}]")
print(f"The screen maxs{X_MAX},{Y_MAX}")

try:
    for event in dev.read_loop():
        if event.type == e.EV_REL:
            if event.code == e.REL_X:
                abs_x += event.value
                if abs_x < 0: 
                    abs_x = 0
                elif abs_x > (X_MAX * 2): #so we can have values above 1920 or more specifically 2x 1920
                    abs_x = X_MAX * 2
            elif event.code == e.REL_Y:
                abs_y += event.value
                if abs_y < 0: abs_y = 0
                elif abs_y > Y_MAX: abs_y = Y_MAX
            elif event.code == 11:
                if event.value > 1:
                    wheelup = 1
                if event.value < -1:
                    wheeldown = 1
                    
        elif event.type == e.EV_KEY:
            if event.code == e.BTN_LEFT:
                btn_left = event.value
            elif event.code == e.BTN_RIGHT:
                btn_right = event.value
            elif event.code == 274:
                middleclick = event.value
            

        elif event.type == e.EV_SYN:
            if abs_x > X_MAX:
                if not is_grabbed:
                    dev.grab()
                    is_grabbed = True
                    print("\n mouse grab")
            else:
                if is_grabbed:
                    dev.ungrab()
                    is_grabbed = False
                    print("\n mouse release")

            if is_grabbed:
                send_x = abs_x - X_MAX ##Normalizing to 0-1920
                
                l_bit = 1 if btn_left else 0
                r_bit = 1 if btn_right else 0
                button_byte = (middleclick << 4) | (wheeldown << 3) | (wheelup << 2) | (r_bit << 1) | l_bit 
                
                packet = struct.pack('!HHB', send_x, abs_y, button_byte)#only 5 BYTES yippie
                client_socket.sendto(packet, server_address)
            
                wheelup = 0
                wheeldown = 0
                sys.stdout.write(f"\r calculated X: {abs_x:<5} | Sent X: {send_x:<5} | Y: {abs_y:<5}")
                sys.stdout.flush()
finally:
    if is_grabbed:
        dev.ungrab()
#Im giving up bro this stuf aint working