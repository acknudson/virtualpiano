LeaPiano
Aubrey Colter and Lee Gross

Must have pygame, pyfluidsynth, and Leap SDK installed.

Plug in the Leap, make sure it can track hands (we use the visualizer).

To run the LeaPiano, in the terminal navigate to the leapiano/src project folder and type python main.py

A full-screen piano GUI should appear. Check that finger dots appear on the screen and are tracking.

To set up the tables:
Depth placement order: You -> Leap -> shorter table -> taller table (tables should slightly overlap) -> Computer 
There are 4 thresholds relating to the tables.
1. Vertical threshold of white keys
2. Depth threshold of white keys (where the table starts relative to the Leap)
3. Vertical threshold of black keys
4. Depth threshold of black keys

To set 1 and 2, place your right index finger on the front edge of the shorter table and press the ‘w’ key with your left hand.

To set 3 and 4, place your right index finger on the front edge of the taller table and press the ‘q’ key with your left hand.

After following these steps, you should be able to play the LeaPiano.

You may need to recalibrate the thresholds if it doesn’t seem to be working well. Try making your finger more vertical when setting the thresholds because the Leap tracks the last joint on the finger, not the tip.

Note that the tables seem to interfere with the Leap infrared tracking, so if it performing well, reset the thresholds, try playing with no tables, or just play with the shorter table.