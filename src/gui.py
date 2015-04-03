import pygame

# initialize colors
RED   = (255,   0,   0)
BLUE  = (0,     0, 255)

#coordinates of each of the dots on the screen, in order from thumb to pinky
fingerDots = [(70,80), (85,80), (100,80), (115,80), (130,80)]

# initialize pygame and the screen
pygame.init()
screen = pygame.display.set_mode((800, 300))
pygame.display.set_caption("LeaPiano")


# initialize background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255,255,255))

def init():

	screen.blit(background, (0,0))

    # initialize basic GUI
	screenSize = screen.get_size()
	pianoLine = pygame.draw.line(background, RED, (10,screenSize[1]/2), (screenSize[0]-10, screenSize[1]/2))

	pygame.display.update() #this is crucial -- writes the values to the screen

def update(play): #rename play to something more descriptive - it's all the gesture info from the leap that is needed
	color = RED
	for i in range(5):
		if play[i]:
			color = BLUE
		else:
			color = RED
		pygame.draw.circle(background, color, fingerDots[i], 2)

	screen.blit(background, (0,0)) #erase screen (return to basic background)
	pygame.display.flip() #redraw with new updates