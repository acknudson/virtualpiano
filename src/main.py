import pygame
from pygame.locals import QUIT, KEYDOWN, K_RETURN, K_q, K_w
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
        (notesPlaying, blackNotesPlaying, noteHovering, blackNoteHovering) = p.position_to_note_played(g.position)
        gui.update(g.position, notesPlaying, blackNotesPlaying, noteHovering, blackNoteHovering)
        #sound.noteStruck()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
            # quit if Enter is pressed
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    running = False
                elif event.key == K_q: #set black key thresholds from piano table
                    y,z = g.getIndexFingerYZ()
                    gui.setBlackThresh(y,z)
                    p.setBlackThresh(y,z)
                elif event.key == K_w: #set white key thresholds from piano table
                    y,z = g.getIndexFingerYZ()
                    gui.setWhiteThresh(y,z)
                    p.setWhiteThresh(y,z)


    pygame.quit()
    sys.exit()    

if __name__ == "__main__":
    main()



# def position_to_note_played(pos):

#     snd.currentHoveringNote = [False]*len(snd.currentNotesPlaying)
#     for hand in pos.right, pos.left:
#         for finger in hand:
#             if finger.z > DEPTH_THRESH: #play white notes
#                 if finger.x > X_MIN and finger.x < X_MAX:
#                     for i in range(1,len(note_cutoffs)):
#                         if finger.x > note_cutoffs[i-1]+padding and finger.x < note_cutoffs[i]-padding:
#                             if i-1 < len(snd.currentHoveringNote):
#                                 snd.currentHoveringNote[i-1] = True
#                             if finger.y < V_THRESH:
#                                 startPlaying(finger, i-1)
#                             else:
#                                 stopPlaying(finger)
#                                 stopPlayingBlack(finger)
#                 else:
#                     stopPlaying(finger)
#                     stopPlayingBlack(finger)

#             else: #play black notes
#                 if finger.x > X_MIN and finger.x < X_MAX:
#                     for i in range(1,len(note_cutoffs)):
#                         if finger.x > (note_cutoffs[i-1]-NOTE_WIDTH/2)+padding and finger.x < (note_cutoffs[i]-NOTE_WIDTH/2)-padding:
#                             if finger.y < BLACK_V_THRESH:
#                                 startPlayingBlack(finger, i-1)
#                             else:
#                                 stopPlaying(finger)
#                                 stopPlayingBlack(finger)
#                 else:
#                     stopPlaying(finger)
#                     stopPlayingBlack(finger)
#     return (snd.currentNotesPlaying, snd.currentBlackNotesPlaying, snd.currentHoveringNote, snd.currentHoveringBlackNote)

