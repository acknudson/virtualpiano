import pygame
import config
#import math

# initialize pygame and the screen
pygame.init()
screen = pygame.display.set_mode((600, 300)) # width, height values
pygame.display.set_caption("LeaPiano")
screenCenterX = 300
screenY = 300
screenSize = screen.get_size() # (width, height)

#global variables
V_THRESH = config.V_THRESH
NOTE_WIDTH = config.NOTE_WIDTH
X_MIN = config.X_MIN
X_MAX = config.X_MAX
PIANO_HEIGHT = screenSize[1] - 50
BLACK_KEY_HEIGHT = screenSize[1] - 80
#Need to add something that will eventually highlight the keys when they are played
# initialize colors
RED   = (255,   0,   0)
BLUE  = (0,     0, 255)
GREEN = (0,   255,   0)
BLACK = (0,     0,   0)
WHITE = (255, 255, 255)

#this is from the sound class -- I don't know how to access it other than copying it.
blackNotesByIndex = [22,0,25,27,0,
	30,32,34,0,37,39,0,
	42,44,46,0,49,51,0,
	54,56,58,0,61,63,0,
	66,68,70,0,73,75,0,
	78,80,82,0,85,87,0,
	90,92,94,0,97,99,0,
	102,104,106,0]


#make the same type of array -- notes by index, or black key for index. only include the black notes
#just put 0s where there are spaces (no black key) -- the array can represent the skipping with a 0. 

class fingerSprite(pygame.sprite.Sprite): #may want to use the dirty sprite class for better rendering? 
	#https://www.pygame.org/docs/ref/sprite.html
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([8,8]) #hardcoded the width and height values of the sprite's image
		self.image.fill(BLUE) #hardcoded the color of the sprite
		self.rect = self.image.get_rect()

	def update(self, x, y, scale):
		self.rect.x = x
		self.rect.y = y
		w,h = self.image.get_size()
		self.image = pygame.transform.scale(self.image, (scale, scale))

	def updateColor(self, color):
		self.image.fill(color)

# class keySprite(pygame.sprite.Sprite):

# 	def __init__(self, top, left, bottom, right):
# 		pygame.sprite.Sprite.__init__(self)

# 		self.image = pygame.Surface([right-left, bottom-top])
# 		self.rect = self.image.get_rect()
# 		# self.image.fill()

# 		self.rect.top = top
# 		self.rect.left = left
# 		self.rect.bottom = bottom
# 		self.rect.right = right
# 		self.top = self.rect.top
# 		self.left = self.rect.left
# 		self.bottom = self.rect.bottom
# 		self.right = self.rect.right
# 		# self.rect.width = right - left
# 		# self.rect.height = bottom-top

# 	def update(self, isPresssed): #key is pressed or not
# 		if isPresssed:
# 			self.rect.top += 10
# 			self.image.fill(BLUE)

# 		else:
# 			self.rect.top -= 10
# 			self.image.fill(WHITE)


#coordinates of each of the dots on the screen, in order from thumb to pinky
#fingerDots = [(70,80), (85,80), (100,80), (115,80), (130,80)]

def drawPiano():
	#draw piano lines

	#top of keys -- middle horizontal line
	# pygame.draw.line(screen, RED, (X_MIN+screenCenterX, PIANO_HEIGHT), (X_MAX+screenCenterX, PIANO_HEIGHT))
	
	#bottom of keys -- bottom horizontal line
	pygame.draw.line(screen, BLACK, (X_MIN+screenCenterX, PIANO_HEIGHT+20), (X_MAX+screenCenterX-NOTE_WIDTH, PIANO_HEIGHT+20))
	#top of keys -- top horizontal line
	pygame.draw.line(screen, BLACK, (X_MIN+screenCenterX+50, PIANO_HEIGHT-50), (X_MAX+screenCenterX-50, PIANO_HEIGHT-50))

	#add vertical lines for the keys below the middle horizontal line
	note_cutoffs = range(X_MIN,X_MAX, NOTE_WIDTH)
	for i in note_cutoffs:
		pygame.draw.line(screen, BLACK, (screenCenterX+i,PIANO_HEIGHT), (screenCenterX+i, PIANO_HEIGHT+20))
	
	#add horizontal lines for each of the key edges (where the finger plays)
	note_cutoffs2 = range(X_MIN,X_MAX-NOTE_WIDTH, NOTE_WIDTH)
	for i in note_cutoffs2:
		pygame.draw.line(screen, BLACK, (screenCenterX+i,PIANO_HEIGHT), (screenCenterX+i+NOTE_WIDTH, PIANO_HEIGHT))
	

	#pygame.draw.line(screen, RED, (screenCenterX+X_MAX,PIANO_HEIGHT), (screenCenterX+X_MAX, PIANO_HEIGHT+20))
	# keys = drawKeySprites()
	# keys.draw(screen)


	#add the trapezoidal lines above the keys to create the illusion of a keyboard
	numNotes = len(note_cutoffs)
	topnotewidth = ((X_MAX+screenCenterX-50) - (X_MIN+screenCenterX+50)) / (numNotes-1.0)
	for i,noteval in enumerate(note_cutoffs):
		pygame.draw.line(screen, BLACK, (X_MIN+screenCenterX+50+i*topnotewidth,PIANO_HEIGHT-50), (screenCenterX+noteval, PIANO_HEIGHT))
		#draw black keys
		if blackNotesByIndex[i] != 0:
			#polygon points are LeftTop, RightTop, RightBottom, LeftBottom
			pygame.draw.polygon(screen, BLACK, [
				[X_MIN+screenCenterX+50+i*topnotewidth - (topnotewidth/3), PIANO_HEIGHT-50], 
				[X_MIN+screenCenterX+50+i*topnotewidth + (topnotewidth/3), PIANO_HEIGHT-50], 
				[screenCenterX+noteval+NOTE_WIDTH/3, BLACK_KEY_HEIGHT], 
				[abs(X_MIN+50+i*topnotewidth - (topnotewidth/3) - i)/2, BLACK_KEY_HEIGHT]], 0)
			


	# for i in range(len(blackNotesByIndex)):



	#testing drawing polygons
	pygame.draw.polygon(screen, BLACK, [[5, 5], [5, 20], [20, 20], [20, 5]], 0)

#add middle line for each note based on whether it is or is not playing. 
def updateNotes(isPlayingList):
	note_cutoffs = range(X_MIN,X_MAX, NOTE_WIDTH)
	for i in range(len(note_cutoffs)):
		if isPlayingList[i]:
			pygame.draw.line(screen, BLACK, (screenCenterX+i,PIANO_HEIGHT+10), (screenCenterX+i+NOTE_WIDTH, PIANO_HEIGHT+10))
		else:
			pygame.draw.line(screen, BLACK, (screenCenterX+i,PIANO_HEIGHT), (screenCenterX+i+NOTE_WIDTH, PIANO_HEIGHT))

# def drawKeySprites():
# 	keySprites = pygame.sprite.Group()
# 	note_cutoffs = range(X_MIN,X_MAX, NOTE_WIDTH)
# 	for i in note_cutoffs:
# 		key = keySprite(PIANO_HEIGHT, screenCenterX+i, PIANO_HEIGHT+20, screenCenterX+i+NOTE_WIDTH)
# 		pygame.draw.polygon(key.image, RED, [[key.top, key.left], [key.top, key.right], [key.bottom, key.right], [key.bottom, key.left]], 5)
# 		keySprites.add(key)

# 	return keySprites

# IF SPRITES ARE COLLIDING -- either look into the sprites colliding method
#or compare the list of keys to the list of notes being played. 
#draw black keys. and figure out the depth stuff. 

# initialize background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(WHITE)
screen.blit(background, (0,0))

# initialize basic GUI
drawPiano()

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

#This array of which notes are playing is smaller than the number of notes that are in the
#noteIndexPlaying array. Will need to do some computation to figure out if the key is pressed.


pygame.display.update() #this is crucial -- writes the values to the screen

#TODO: Use the isPlayingList parameter once it's available from main.py
def update(position): #, isPlayingList): #position is all the gesture info from the leap that is needed
	left = position.left
	right = position.right

	for i in range(len(left)):
		scale = int(8*(300+left[i].z)/500)
		lhspriteList[i].update(left[i].x+screenCenterX, V_THRESH-left[i].y + PIANO_HEIGHT, scale)
		if left[i].notePlaying != None:
			lhspriteList[i].updateColor(GREEN)
		else:
			lhspriteList[i].updateColor(BLACK)
	for i in range(len(right)):
		scale = int(8*(300+right[i].z)/500)
		rhspriteList[i].update(right[i].x+screenCenterX, V_THRESH-right[i].y + PIANO_HEIGHT, scale)
		if right[i].notePlaying != None:
			rhspriteList[i].updateColor(BLUE)
		else:
			rhspriteList[i].updateColor(RED)
	# print right[4].x+screenCenterX

	#screen.blit(background, (0,0)) #erase screen (return to basic background) NEED THIS LINE
	rightHandSprites.clear(screen, background)
	rightHandSprites.draw(screen)
	leftHandSprites.clear(screen, background)
	leftHandSprites.draw(screen)
	drawPiano()
	#TODO: Add this back in once you get the isPlayingList
	#updateNotes(isPlayingList)
	pygame.display.update() # redraw with *new* updates (similar to pygame.display.update())