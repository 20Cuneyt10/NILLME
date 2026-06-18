import socket
import struct
import uinput

BIP = '192.168.1.106'#bind ip
BORT = 5005# bind port
X_MAX = 1920
Y_MAX = 1080
left_last = 0
right_last = 0
events = (
    uinput.BTN_LEFT,
    uinput.BTN_RIGHT,
    uinput.REL_WHEEL,
    uinput.BTN_MIDDLE,
    uinput.ABS_X + (0, 1920, 0, 0),
    uinput.ABS_Y + (0, 1080, 0, 0),
)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((BIP, BORT))

print(f"Connected {BIP}:{BORT}...")
print(f"mirroring on {X_MAX}x{Y_MAX}")

with uinput.Device(events, name="Virtual Mouse") as ui:
    try:
        while True:
            data, addr = server_socket.recvfrom(5)
            
            if len(data) == 5:
                target_x, target_y, button_byte = struct.unpack('!HHB', data)
                left_state = button_byte & 1
                right_state = (button_byte >> 1) & 1
                wheel_up_state = (button_byte >> 2) & 1
                wheel_down_state = (button_byte >> 3) & 1
                middleclk_state = (button_byte >> 4) & 1
                ui.emit(uinput.ABS_X, target_x-1920, syn=False)
                ui.emit(uinput.ABS_Y, target_y, syn=False)
                if left_state != left_last:
                    ui.emit(uinput.BTN_LEFT, left_state, syn=False)
                    left_last = left_state
                if right_state != right_last:
                    ui.emit(uinput.BTN_RIGHT, right_state, syn=False)
                    right_last = right_state
                ui.emit(uinput.BTN_MIDDLE, middleclk_state, syn=False)
                ui.emit(uinput.REL_WHEEL, wheel_up_state - wheel_down_state, syn=False)
                ui.emit(uinput.ABS_X, target_x, syn=False)
                ui.emit(uinput.ABS_Y, target_y, syn=True)
                print(f" mirrored to {target_x}, Y: {target_y} and button states: left={left_state}, right={right_state}, wheel_up={wheel_up_state}, wheel_down={wheel_down_state}, middleclk={middleclk_state}")

    finally:
        server_socket.close()