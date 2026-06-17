import sys
from evdev import InputDevice, list_devices, ecodes as e
import socket
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.1.106', 5005)

X_MAX = 1920
Y_MAX = 1080

#starting the tracking at the center
abs_x = X_MAX // 2
abs_y = Y_MAX // 2
btn_right = 0
btn_left = 0

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

print(f"grabing {dev.name} [{dev.path}]")
print(f"The screen maxs{X_MAX},{Y_MAX}")

dev.grab()#this grabs the mouse so we only use the mouse on the mirrored PC

try:
    for event in dev.read_loop():
        if event.type == e.EV_REL:  ##Codes needed for absoloute coordinate findings
            
            if event.code == e.REL_X:
                abs_x += event.value
                if abs_x < 0: abs_x = 0
                elif abs_x > X_MAX: abs_x = X_MAX
                
            elif event.code == e.REL_Y:
                abs_y += event.value
                if abs_y < 0: abs_y = 0
                elif abs_y > Y_MAX: abs_y = Y_MAX
            
        if event.type == e.EV_KEY:
            if event.code == e.BTN_LEFT:
                btn_left = event.value
            elif event.code == e.BTN_RIGHT:
                btn_right = event.value
        if event.type == e.EV_SYN:
            l_bit = 1 if btn_left else 0
            r_bit = 1 if btn_right else 0
            
            button_byte = (r_bit << 1) | l_bit
            packet = struct.pack('!HHB', abs_x, abs_y,button_byte)##was using normal messages before but i was getting too high latency aı offered this kind and with this its only 5 bytes
            client_socket.sendto(packet, server_address)

            sys.stdout.write(f"\rCoordinate {abs_x:<5} | Y: {abs_y:<5}")
            sys.stdout.flush()

    
finally:
    dev.ungrab()