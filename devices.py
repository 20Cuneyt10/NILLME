from evdev import list_devices, InputDevice

for path in list_devices():
    try:
        device = InputDevice(path)
        print(f"{device.path:<18} | {device.name}")
    except (PermissionError, OSError):
        print(f"{path:<18} | [permission denied or  busy]")