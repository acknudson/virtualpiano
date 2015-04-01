import pygame

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

"""

import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

pygame.init()
screen = pygame.display.set_mode((200, 200))

#http://stackoverflow.com/questions/23431209/python-pygame-error-video-system-not-initialized

def main():

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."

    pygame.display.set_caption("LeaPiano")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255,255,255))
    screen.blit(background, (0,0))

    playing = True
    
    try:
        while playing:
##            event = pygame.event.wait()
##            if event.type == pygame.QUIT:
##                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   playing = False
            pygame.display.flip()
            sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
##    pygame.quit()
    

if __name__ == "__main__":
    main()
