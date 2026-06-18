from evdev import list_devices, InputDevice

print("Scanning all system input devices...\n")
print(f"{'Device Path':<18} | {'Device Name'}")
print("-" * 50)

for path in list_devices():
    try:
        device = InputDevice(path)
        print(f"{device.path:<18} | {device.name}")
    except (PermissionError, OSError):
        print(f"{path:<18} | [Permission Denied / Busy]")