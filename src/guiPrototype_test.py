import pygame
from pygame.locals import QUIT, KEYDOWN, K_RETURN
import os, sys, inspect, thread, time


import gestures
import gui


def main():

    g = gestures.Gestures()
    # create a blank screen
    gui.init()


    running = True
    while running:
        #get the current Leap frame
        play = g.leapControl()
        gui.update(play)
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