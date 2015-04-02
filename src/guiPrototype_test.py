import pygame
from pygame.locals import QUIT, KEYDOWN, K_RETURN
import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import sound

"""
pygame.display.set_mode()
Surface()
image.load()
font.render()
blit()
fill()
set_at()
get_at()
surface = pygame.image.load('foo.png').convert()

pygame.display.update()
pygame.display.update(rect or list of rects)

Blit a piece of the background over the sprite's current location, erasing it.
Append the sprite's current location rectangle to a list called dirty_rects.
Move the sprite
Draw the sprite at its new location.
Append the sprite's new location to my dirty_rects list
Call display.update(dirty_rects)

A Rect is defined by its top left coordinates, and it height and width
To define the area from (10,20) to (40,50), any of the following are acceptable:
rect = pygame.Rect(10,20,30,30)
rect = pygame.Rect((10,20,30,30))
rect = pygame.Rect((10,20), (30,30))
rect = (10,20,30,30)
rect = ((10,20,30,30))

*** https://inventwithpython.com/pygameHelloWorld.py

"""

# initialize necessary sounds/scale
scale = ('C', 'D', 'E', 'F', 'G', 'A', 'B', 'C')
play = [False, False, False, False, False]
snd = sound.Sound()

# initialize colors
RED   = (255,   0,   0)
BLUE  = (0,     0, 255)

# initialize screen
pygame.init()
screen = pygame.display.set_mode((200, 200))
pygame.display.set_caption("LeaPiano")

# initialize background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255,255,255))

# initialize basic GUI
pianoLine = pygame.draw.line(background, RED, (10,100), (190, 100))
rthumb = pygame.draw.circle(background, RED, (70,80), 2)
rindex = pygame.draw.circle(background, RED, (85,80), 2)
rmiddle = pygame.draw.circle(background, RED, (100,80), 2)
rring = pygame.draw.circle(background, RED, (115,80), 2)
rpinky = pygame.draw.circle(background, RED, (130,80), 2)

#coordinates of each of the dots on the screen, in order from thumb to pinky
fingerDots = [(70,80), (85,80), (100,80), (115,80), (130,80)]

# A function that deals with all of the leap finger tracking, and what to do
# when a finger has moved, including updating the GUI and playing a sound.
# frame is the current frame, which the Leap Controller gets
def leapControl(frame):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
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
                            # draw a blue circle for the finger
                            pygame.draw.circle(background, BLUE, fingerDots[finger.type()], 2)
            else:
                    if play[finger.type()] == True:
                            #fs.noteoff(0, scale[finger.type()])
                            snd.noteOff(scale[finger.type()], 4)
                            play[finger.type()] = False
                            # draw a red circle for the finger
                            pygame.draw.circle(background, RED, fingerDots[finger.type()], 2)

def main():
    # setup the controller
    controller = Leap.Controller()

    # create a blank screen
    screen.blit(background, (0,0))
    pygame.display.update() #this is crucial -- writes the values to the screen

    playing = True
    controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
    while playing:
        #get the current Leap frame
        frame = controller.frame()
        leapControl(frame)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               playing = False
            # quit if Enter is pressed
            elif event.type == KEYDOWN and event.key == K_RETURN:
                playing = False

        screen.blit(background, (0,0)) #erase screen (return to basic background)
        pygame.display.flip() #redraw with new updates

    pygame.quit()
    sys.exit()
##    pygame.quit()
    

if __name__ == "__main__":
    main()
