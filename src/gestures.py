import sound
import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


# initialize necessary sounds/scale
scale = ('C', 'D', 'E', 'F', 'G', 'A', 'B', 'C')
play = [False, False, False, False, False]
snd = sound.Sound()

class Gestures():


    def __init__(self):
        # setup the controller
        self.controller = Leap.Controller()

    # A function that deals with all of the leap finger tracking, and what to do
    # when a finger has moved, including updating the GUI and playing a sound.
    # frame is the current frame, which the Leap Controller gets
    def leapControl(self):
        finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
        state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

        frame = self.controller.frame()
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"

            # Get fingers
            for finger in hand.fingers:
                bone = finger.bone(3)
                if bone.next_joint[1] < 90:
                        print finger_names[finger.type()]
                        if play[finger.type()] == False:
                                play[finger.type()] = True
                                #fs.noteon(0, scale[finger.type()], 127)
                                snd.playNote(scale[finger.type()], 4)
                else:
                        if play[finger.type()] == True:
                                #fs.noteoff(0, scale[finger.type()])
                                snd.noteOff(scale[finger.type()], 4)
                                play[finger.type()] = False

        return play


