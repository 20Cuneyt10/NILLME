#NILLME
This is NILLME Naver's Inefficient Linux to Linux Mouse extender application 


A video down below shows the scritps working with a bit of latency because i couldnt sync up the videos
[<img src="https://img.youtube.com/vi/RC8_hjuneoU/maxresdefault.jpg" width="100%">](https://youtu.be/RC8_hjuneoU)
These scripts utilize the evdev,uinput and the UDP library to essentially combine 2 linux computers as one big monitor while keeping them seperate(you will understand it when i explain down below)


**Main Code Logic**
First we have our sender computer lets call this the host computer in the host computer there are a few things we need to accomplish before doing anything:
- Importing the libraries
- Set up the UDP connection
- Get the mouse event device (so we can use it to get the coordinates whilst sending it to the other computer)
- Set values like X_MAX,YMAX and all other values that need to be setup before the loop starts 
- Finding out which event device our mouse is and assigning it.
- Setting our mouse to the middle of the s


After we have done all that we can get to knowing where our mouse is so we can add our logic and we basically do that by telling the user to move their mouse to the bottom left corner(this is easier than the other solutions which is duplicating the mouse event,grabbing it then fixing it to the middle for a while)

Now that we know the mouse will start at 0,1080 we can use that value and the relative coordinate changes we get from the relative coordinate changes we get from the mouse hardware.

By tracking event.value, we can update a virtual coordinate tracker (abs_x, abs_y). Once the mouse crosses the X_MAX threshold (moving past the edge of the host screen), the script grabs the hardware device. This hides it from the host OS and starts sending the coordinates over UDP to the receiver machine.

To keep performance fast, the script packs the data into a tight, 5-byte package using some quick bit shifts for mouse clicks and scroll wheels, then sends it over to the second machine.
**Receiver Code Logic**

Once the sender flings those 5-byte UDP packets across the network, the receiver machine needs a way to catch them and turn them back into actual cursor movements. Here is how the receiver handles it:

- Socket Binding: We set up a UDP socket and bind it to the receiver's local IP and port 5005, waiting for packets to come in.

- Virtual Device Creation: Using Python's uinput library, we make a  virtual mouse inside the Linux kernel. We set it up to handle Absolute X/Y movements (ABS_X, ABS_Y), left/right/middle clicks, and scroll wheel events.

- Reading the Clicks: Every incoming packet has a button_byte. The receiver reads the binary numbers to figure out the states for every click and scroll event.

- Checking for Changes: To prevent spamming the OS with duplicate inputs, the script keeps track of the previous state of the buttons (like left_last and right_last) and only triggers a click if something actually changed.

- Moving the Mouse: The positions and button states are passed directly to uinput.Device. By calling syn=True only at the very end of the loop, we ensure the mouse updates cleanly on screen all at once.

Future TO-DOs (Because I threw my hands up on this)

Look, it sort of works, but it's held together by duct tape, hope, and prayer. Here is what needs to be fixed before this is actually usable without losing your sanity:

-   [ ] Ditch the Bottom-Left Calibration: Asking the user to manually slam their mouse into the corner at launch is hilarious but terrible UX. Need to implement a proper automatic way to find the starting position.

-   [ ] Fix the Sync Delay & Latency: UDP is fast, but handling individual packet loops sequentially creates noticeable stuttering(you will see if you try it). Need a better way to poll data.
-    [ ] Graceful Failures: If the network hiccups, the host computer currently traps the mouse in an exclusive dev.grab() state, leaving you stranded. Need a global escape key combo to instantly drop the grab and free the host mouse(after my 5h research with the keyboard i dont think i will do this anytime soon).

-   [ ] Dynamic Screen Resolutions: Hardcoding 1920x1080 means anyone on a different monitor setup is going to have a bad time. Need to detect screen size automatically.

-   [ ] Bi-directional Crossing: Right now it's a one-way street from Host to Receiver. Need to support moving the mouse back across the border from the receiver side seamlessly(you will see if you change the y value whilst coming back from the client computer the y wont update bcus we arent talking back).
