-NILLME — README

About NILLME
- NILLME (Naver's Inefficient Linux-to-Linux Mouse Extender) mirrors a physical mouse from one Linux machine (host) to another (client) over a LAN.
- It reads low-level input on the host with `evdev`, packs position, button and wheel state into a compact 5-byte UDP packet, and the client recreates those events with `uinput`.
- Design goals: minimal packet size (5 bytes), low latency, and simple coordinate translation when crossing a screen boundary. Current features: absolute X/Y mirroring, left/right/middle buttons, and scroll wheel. Keyboard support is not implemented(because i couldnt figure it out bro thats also why ım ending this project here i searched for like 5 hours for eyboard related documentation none worked).

Demo
- A short demo video of the project in action is included as `Combinedvideo.mp4`.

<video controls src="Combinedvideo.mp4" title="NILLME demo"></video>

This shows the host mouse crossing the edge and the client receiving/reflecting movement with clicks and scrolls.

**Purpose**
This README documents the two working scripts in this repo: `test2.py` (host) and `Test2client.py` (client). Use these two files as-is to mirror mouse input from a host machine to a client machine over LAN.

**Files**
- `test2.py` — host: reads the physical mouse with `evdev`, detects when the cursor crosses the host screen edge, grabs the device, packs a 5-byte UDP packet, and sends it to the client.
- `Test2client.py` — client: binds a UDP socket, receives 5-byte packets, unpacks them, and emits events through `uinput` to simulate a mouse on the client.

**Packet format (used by both scripts)**
- 5 bytes total: `struct.pack('!HHB', x, y, flags)`
  - Bytes 0-1: X coordinate (unsigned short, network byte order)
  - Bytes 2-3: Y coordinate (unsigned short)
  - Byte 4: flags bitfield (buttons & wheel)

Flags bitfield mapping (byte 4)
- Bit 0: left button
- Bit 1: right button
- Bit 2: wheel up
- Bit 3: wheel down
- Bit 4: middle click

**How the two scripts interact (concrete)**
- `test2.py` monitors `/dev/input/event*` for a device whose name contains "G305" (see `find_mouse()`); change that string if your mouse name differs.
- When `abs_x` grows beyond `X_MAX`, `dev.grab()` is called and the host begins sending normalized X coordinates (`send_x = abs_x - X_MAX`) to the client IP/port set in `server_address`.
- `Test2client.py` must be listening on the bind IP/port (`BIP`, `BORT`) and will map incoming `target_x`/`target_y` to the virtual device created with `uinput`.

**Configuration**
- Set `server_address` in `test2.py` to the client's IP and port (default in the scripts: `192.168.1.106:5005`).
- Set `BIP`/`BORT` in `Test2client.py` to the host IP and the same port.
- Match `X_MAX`/`Y_MAX` to the host/client coordinate ranges. `test2.py` uses `X_MAX = 1920` and allows `abs_x` up to `X_MAX * 2` so it can cross the boundary.

**Permissions**
- Both scripts generally need elevated privileges to access input devices and to create uinput devices. Run with `sudo` or add appropriate udev rules.

**Run commands (example)**
```bash
# on client (the machine that will receive/emit the mouse):
sudo python3 Test2client.py

# on host (the machine with the physical mouse):
sudo python3 test2.py
```

**Notes, gotchas, and quick suggestions**
- `test2.py` currently looks for device names containing "G305" — change that to match your device or remove the filter to pick the first available device.
- Wheel handling in `test2.py` uses a numeric code check (`event.code == 11`); consider replacing with `e.REL_WHEEL` or printing codes to confirm the correct code for your device.
- Middle button is matched against literal `274` in `test2.py`; prefer `e.BTN_MIDDLE` for readability and portability.
- `Test2client.py` emits `uinput.ABS_X` twice: first with `target_x-1920` then with `target_x`. If you intended an offset, change or remove the extra emit; otherwise keep only the correct mapped value.
- UDP is low-latency but unreliable; if you see dropped or out-of-order packets, add a sequence number or switch to a reliable transport.

**Troubleshooting**
- If the host prints "mouse not detected", run `python3 -c "from evdev import list_devices, InputDevice; print([InputDevice(p).name for p in list_devices()])"` with sudo to list devices and names.
- If the virtual mouse does not move on the client, verify `uinput` is installed and the script runs with sufficient privileges.
- If the host's cursor remains grabbed, ensure `test2.py` calls `dev.ungrab()` in finally/cleanup (the file includes an ungrab on exit but confirm it triggers on exceptions).

