import pygame

#Need to add something that will eventually highlight the keys when they are played

class fingerSprite(pygame.sprite.Sprite): #may want to use the dirty sprite class for better rendering? 
	#https://www.pygame.org/docs/ref/sprite.html
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.x = None
		self.y = None
		# self.z = z
		self.image = pygame.Surface([3,3]) #hardcoded the width and height values of the sprite's image
		self.image.fill(BLUE) #hardcoded the color of the sprite
		self.rect = self.image.get_rect()

	def update(self, x, y):
		self.rect.x = x
		self.rect.y = y

	def updateColor(self, color):
		self.image.fill(color)

# initialize colors
RED   = (255,   0,   0)
BLUE  = (0,     0, 255)
GREEN = (0,   255,   0)
BLACK = (0,     0,   0)

#coordinates of each of the dots on the screen, in order from thumb to pinky
#fingerDots = [(70,80), (85,80), (100,80), (115,80), (130,80)]

# initialize pygame and the screen
pygame.init()
screen = pygame.display.set_mode((600, 300)) # width, height values
pygame.display.set_caption("LeaPiano")
screenCenterX = 300
screenY = 300
V_THRESH = 90 #from processing class


# initialize background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255,255,255))

#def init():

screen.blit(background, (0,0))

# initialize basic GUI
screenSize = screen.get_size() # (width, height)
#draw piano line
pygame.draw.line(screen, RED, (10,screenY-V_THRESH), (screenSize[0]-10, screenY-V_THRESH))

#add vertical lines for the keys

# create finger sprites for each finger, put into left and right groups
rthumb = fingerSprite()
rindex = fingerSprite()
rmiddle = fingerSprite()
rring = fingerSprite()
rpinky = fingerSprite()


rightHandSprites = pygame.sprite.Group()
rightHandSprites.add(rthumb, rindex, rmiddle, rring, rpinky)
rhspriteList = [rthumb, rindex, rmiddle, rring, rpinky]

lthumb = fingerSprite()
lindex = fingerSprite()
lmiddle = fingerSprite()
lring = fingerSprite()
lpinky = fingerSprite()


leftHandSprites = pygame.sprite.Group()
leftHandSprites.add(lthumb, lindex, lmiddle, lring, lpinky)
lhspriteList = [lthumb, lindex, lmiddle, lring, lpinky]

#rightHandSprites.draw(screen)
#leftHandSprites.draw(screen)
pygame.display.update() #this is crucial -- writes the values to the screen

def update(position): # position is all the gesture info from the leap that is needed
	left = position.left
	right = position.right

	for i in range(len(left)):
		lhspriteList[i].update(left[i].x+screenCenterX, screenY-left[i].y)

		if left[i].notePlaying != None:
			lhspriteList[i].updateColor(GREEN)
		else:
			lhspriteList[i].updateColor(BLACK)
	for i in range(len(right)):
		rhspriteList[i].update(right[i].x+screenCenterX, screenY-right[i].y)
		if right[i].notePlaying != None:
			rhspriteList[i].updateColor(BLUE)
		else:
			rhspriteList[i].updateColor(RED)
	print right[4].x+screenCenterX

	#screen.blit(background, (0,0)) #erase screen (return to basic background) NEED THIS LINE
	rightHandSprites.clear(screen, background)
	rightHandSprites.draw(screen)
	leftHandSprites.clear(screen, background)
	leftHandSprites.draw(screen)
	#piano line
	pygame.draw.line(screen, RED, (10,screenY-V_THRESH), (screenSize[0]-10, screenY-V_THRESH))
	pygame.display.update() # redraw with *new* updates (similar to pygame.display.update())