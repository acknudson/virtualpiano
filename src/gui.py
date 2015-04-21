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
PIANO_HEIGHT = screenSize[1] - 30
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

def drawPianoBottom():
	#draw piano lines

	#bottom of keys -- bottom horizontal line
	pygame.draw.line(screen, BLACK, (X_MIN+screenCenterX, PIANO_HEIGHT+20), (X_MAX+screenCenterX, PIANO_HEIGHT+20))
	
	#top of keys -- top horizontal line
	#pygame.draw.line(screen, BLACK, (X_MIN+screenCenterX+50, PIANO_HEIGHT-50), (X_MAX+screenCenterX-50, PIANO_HEIGHT-50))

	#add vertical lines for the keys below the middle horizontal line
	note_cutoffs = range(X_MIN,X_MAX+NOTE_WIDTH, NOTE_WIDTH)
	for i in note_cutoffs:
		pygame.draw.line(screen, BLACK, (screenCenterX+i,PIANO_HEIGHT), (screenCenterX+i, PIANO_HEIGHT+20))
	
	#add horizontal lines for each of the key edges (where the finger plays)
	note_cutoffs2 = range(X_MIN,X_MAX, NOTE_WIDTH)
	for i in note_cutoffs2:
		pygame.draw.line(screen, BLACK, (screenCenterX+i,PIANO_HEIGHT), (screenCenterX+i+NOTE_WIDTH, PIANO_HEIGHT))
	

	numNotes = len(note_cutoffs)
	topnotewidth = ((X_MAX+screenCenterX-50) - (X_MIN+screenCenterX+50)) / (numNotes-1.0)
	blackNoteWidth = ((X_MAX+screenCenterX) - (X_MIN+screenCenterX)) / (numNotes-1.0)
	blackKeyXOffset = NOTE_WIDTH/2
	BLACK_KEY_HEIGHT = PIANO_HEIGHT - 10
	BLACK_KEY_SPACE1 = blackNoteWidth/5
	BLACK_KEY_SPACE2 = topnotewidth/5
	for i,noteval in enumerate(note_cutoffs):

		#add the trapezoidal lines above the keys to create the illusion of a keyboard
		# pygame.draw.line(screen, BLACK, (X_MIN+screenCenterX+50+i*topnotewidth,PIANO_HEIGHT-50), (screenCenterX+noteval, PIANO_HEIGHT))

		val = 0
		#draw black keys
		if blackNotesByIndex[i] != 0:
			#square part of black keys	
			# top = PIANO_HEIGHT - 35
			# left = blackKeyXOffset+X_MIN+screenCenterX+i*blackNoteWidth+BLACK_KEY_SPACE1
			# bottom = top+10
			# right = blackKeyXOffset+X_MIN+screenCenterX+(1+i)*blackNoteWidth-BLACK_KEY_SPACE1
			# pygame.draw.polygon(screen, BLACK, [[left,top], [right, top], [right, bottom], [left,bottom]], 0)
			top = BLACK_KEY_HEIGHT
			left = blackKeyXOffset+X_MIN+screenCenterX+i*blackNoteWidth +BLACK_KEY_SPACE1
			bottom = top+10
			right = blackKeyXOffset+X_MIN+screenCenterX+(1+i)*blackNoteWidth -BLACK_KEY_SPACE1
			pygame.draw.polygon(screen, BLACK, [[left,top], [right, top], [right, bottom], [left,bottom]], 0)


			left1 = blackKeyXOffset+X_MIN+screenCenterX+(i)*topnotewidth+BLACK_KEY_SPACE2
			right2 = blackKeyXOffset+X_MIN+screenCenterX+(1+i)*topnotewidth-BLACK_KEY_SPACE2

			#polygon points are LeftTop, RightTop, RightBottom, LeftBottom
			#trapezoidal part of black key
			# topleft2 = [50+X_MIN+screenCenterX+(i)*topnotewidth+BLACK_KEY_SPACE2,PIANO_HEIGHT-50]
			# topright2 = [50+X_MIN+screenCenterX+(1+i)*topnotewidth-BLACK_KEY_SPACE2, PIANO_HEIGHT-50]
			# bottomleft2 = [left,top]
			# bottomright2 = [right, top]
			# pygame.draw.polygon(screen, BLACK, [topleft2, topright2, bottomright2, bottomleft2], 0)


#add middle line for each note based on whether it is or is not playing. 
def updateNotes(isPlayingList):
	note_cutoffs = range(X_MIN,X_MAX, NOTE_WIDTH)
	for i in range(len(note_cutoffs)):
		if isPlayingList[i]:
			pygame.draw.line(screen, BLACK, (screenCenterX+i,PIANO_HEIGHT+10), (screenCenterX+i+NOTE_WIDTH, PIANO_HEIGHT+10))
		else:
			pygame.draw.line(screen, BLACK, (screenCenterX+i,PIANO_HEIGHT), (screenCenterX+i+NOTE_WIDTH, PIANO_HEIGHT))

# IF SPRITES ARE COLLIDING -- either look into the sprites colliding method
#or compare the list of keys to the list of notes being played. 
#draw black keys. and figure out the depth stuff. 

# initialize background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(WHITE)
screen.blit(background, (0,0))

# initialize basic GUI
drawPianoBottom()

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
	drawPianoBottom()
	#TODO: Add this back in once you get the isPlayingList
	#updateNotes(isPlayingList)
	pygame.display.update() # redraw with *new* updates (similar to pygame.display.update())

