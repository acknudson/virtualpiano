import pygame
from pygame.locals import QUIT, KEYDOWN, K_RETURN
import os, sys, inspect, thread, time


import gestures
import gui
import Processing as p
import sound



def main():

    g = gestures.Gestures()

    running = True
    while running:
        #get the current Leap frame
        g.leapControl()
        (notesPlaying, blackNotesPlaying) = p.position_to_note_played(g.position) #this would need sound
        #TODO: Add the isPlayingList to this method signature when it's ready
        gui.update(g.position, notesPlaying, blackNotesPlaying) #, isPlayingList)  #this would need sound
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