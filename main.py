from evdev import InputDevice, categorize, ecodes as e,UInput

dev = InputDevice('/dev/input/event4')

cap = {
    e.EV_REL: [e.REL_X,e.REL_Y],
    e.EV_KEY: [e.BTN_LEFT,e.BTN_RIGHT]
}
ui = UInput(events=cap, name="virtmos")

print(dev)
#dev.capabilities(verbose=True)
for event in dev.read_loop():
    if event.type == e.EV_REL:
        print(event)
    ui.write(e.EV_REL, event.code, event.value + 1)
    ui.syn()


