import evdev
device = evdev.InputDevice('/dev/input/event7')
print(device)

device.capabilities()

print(device.capabilities(verbose=True))