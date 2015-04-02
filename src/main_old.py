#main loop
#include necessary imports
import sound
import gui
import gestures

#global variables
# threshold
# noteCutoffs (the x range (and later z range) in space for each note)

def main():
    # setup the controller
    controller = Leap.Controller()

    # create a blank screen
    screen.blit(background, (0,0))
    pygame.display.update() #this is crucial -- writes the values to the screen

    playing = True
    controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
    while playing:
        background.fill(WHITE)
        #get the current Leap frame
        frame = controller.frame()
        [] = leapControl(frame)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               playing = False
            # quit if Enter is pressed
            elif event.type == KEYDOWN and event.key == K_RETURN:
                playing = False

        # screen.blit(background, (0,0)) #erase screen (return to basic background)
        pygame.display.update() #redraw with new updates

    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()