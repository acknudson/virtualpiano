import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class Gestures():


    def __init__(self):
        # setup the controller
        self.controller = Leap.Controller()
        self.position = Position()

    # A function that deals with all of the leap finger tracking, and what to do
    # when a finger has moved, including updating the GUI and playing a sound.
    # frame is the current frame, which the Leap Controller gets
    def leapControl(self):
        finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
        state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

        frame = self.controller.frame()
        for hand in frame.hands:
            handType = "LEFT" if hand.is_left else "RIGHT"

            # Get fingers
            for finger in hand.fingers:
                bone = finger.bone(3)
                adjust_y = 0
                if finger.type() ==0:
                    adjust_y = -10
  
                x = bone.next_joint[0]
                y = bone.next_joint[1] + adjust_y
                z = bone.next_joint[2]
                self.position.update(handType, finger.type(), x,y,z)
        #if one or more hands are out of the leap range, set their values to be 
        #above the piano so that they don't get stuck where they were last detected
        if len(frame.hands)==0:
            x = 400
            y = 400
            z = 400
            for finger_index in range(5):
                self.position.update("LEFT", finger_index, x,y,z)
                self.position.update("RIGHT", finger_index, x,y,z)
        elif len(frame.hands)==1:
            x = 400
            y = 400
            z = 400
            handType = "RIGHT" if frame.hands[0].is_left else "LEFT"
            for finger_index in range(5):
                self.position.update(handType, finger_index, x,y,z)


class Position():

    def __init__(self):
        #position of fingers in each hand
        #[thumb, index, middle, ring, pinky]
        self.left = [Finger(0),Finger(1),Finger(2),Finger(3),Finger(4)]
        self.right = [Finger(0),Finger(1),Finger(2),Finger(3),Finger(4)]

    #hand is a string, "LEFT" or "RIGHT"
    #finger index in an integer, ranging from 0 to 4
    def update(self, hand, finger_index, x, y, z):
        if hand == "LEFT":
            self.left[finger_index].x = x
            self.left[finger_index].y = y
            self.left[finger_index].z = z
        if hand == "RIGHT":
            self.right[finger_index].x = x
            self.right[finger_index].y = y
            self.right[finger_index].z = z

class Finger():

    finger_types = ["Thumb", "Index", "Middle", "Ring", "Pinky"]

    def __init__(self, i):
        self.x = 0
        self.y = 0
        self.z = 0
        self.index = i
        self.type = self.finger_types[i]
        self.notePlaying = None #note is a tuple of (NoteName, Octave)
        self.notePlayingBlack = None



