import pygame

# initialize colors
RED   = (255,   0,   0)
BLUE  = (0,     0, 255)

#coordinates of each of the dots on the screen, in order from thumb to pinky
fingerDots = [(70,80), (85,80), (100,80), (115,80), (130,80)]

# initialize pygame and the screen
pygame.init()
screen = pygame.display.set_mode((800, 300)) # width, heigh values
pygame.display.set_caption("LeaPiano")


# initialize background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255,255,255))

def init():

	screen.blit(background, (0,0))

    # initialize basic GUI
	screenSize = screen.get_size() # (width, height)
	pianoLine = pygame.draw.line(background, RED, (10,screenSize[1]/2), (screenSize[0]-10, screenSize[1]/2))

	# create finger sprites for each finger, put into left and right groups
	


	pygame.display.update() #this is crucial -- writes the values to the screen

def update(play): #rename play to something more descriptive - it's all the gesture info from the leap that is needed
	color = RED
	for i in range(5):
		if play[i]:
			color = BLUE
		else:
			color = RED
		pygame.draw.circle(background, color, fingerDots[i], 2)

	pygame.display.flip() #redraw with *new* updates (similar to pygame.display.update())


class fingerSprite(pygame.sprite.Sprite): #may want to use the dirty sprite class for better rendering? 
	#https://www.pygame.org/docs/ref/sprite.html
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# self.x = x
		# self.y = y
		# self.z = z
		self.image = pygame.Surface([3,3]) #hardcoded the width and height values of the sprite's image
		self.image.fill(BLUE) #hardcoded the color of the sprite
		self.rect = self.image.get_rect()

	def update(self, x, y, z):
		self.rect.x = x
		self.rect.y = y