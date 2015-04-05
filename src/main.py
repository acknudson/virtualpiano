import pygame
from pygame.locals import QUIT, KEYDOWN, K_RETURN
import os, sys, inspect, thread, time


import gestures
import gui
import Processing as p

#thresholds for determining whether a note was played
vertical_threshold = 90
#min x = -150, max x = 150
note_threshold = 20

def main():

    g = gestures.Gestures()
    # create a blank screen
    #gui.init()


    running = True
    while running:
        #get the current Leap frame
        g.leapControl()
        p.position_to_note_played(g.position)
        gui.update(g.position)
        #sound.noteStruck()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
            # quit if Enter is pressed
            elif event.type == KEYDOWN and event.key == K_RETURN:
                running = False
    pygame.quit()
    sys.exit()    

if __name__ == "__main__":
    main()