import pygame
import config
#import math

# initialize pygame and the screen
pygame.init()
screen = pygame.display.set_mode((600, 300)) # width, height values
screenSize = screen.get_size() # (width, height)
pygame.display.set_caption("LeaPiano")
screenCenterX = screenSize[0]/2
screenCenterY = screenSize[1]/2.0
screenY = screenSize[1]


#global variables
V_THRESH = config.V_THRESH
NOTE_WIDTH = config.NOTE_WIDTH
X_MIN = config.X_MIN
X_MAX = config.X_MAX
MIDDLE_LINE_HEIGHT = screenSize[1]/2.0
PIANO_HEIGHT_BOTTOM = screenSize[1] - 60
PIANO_HEIGHT_TOP = screenSize[1] - 175
BLACK_KEY_HEIGHT_BOTTOM = PIANO_HEIGHT_BOTTOM - 10
BLACK_KEY_HEIGHT_TOP = PIANO_HEIGHT_TOP - 50
DEPTH_THRESH = config.DEPTH_THRESH
#Need to add something that will eventually highlight the keys when they are played
# initialize colors
RED   = (255,   0,   0)
BLUE  = (0,     0, 255)
GREEN = (0,   255,   0)
BLACK = (0,     0,   0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (175, 175, 175)
DARK_GRAY = (100, 100, 100)

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

def drawPianoBottom(notes, blackNotes):
	
	#add vertical lines for the keys below the middle horizontal line
	numNotes = len(notes)
	blackNoteWidth = ((X_MAX+screenCenterX) - (X_MIN+screenCenterX)) / (numNotes)
	blackKeyXOffset = NOTE_WIDTH/2
	BLACK_KEY_SPACE = blackNoteWidth/5
	for i,noteval in enumerate(range(X_MIN,X_MAX, NOTE_WIDTH)):
		#draw white keys
		top = PIANO_HEIGHT_BOTTOM+20
		left = X_MIN+screenCenterX+i*NOTE_WIDTH
		bottom = PIANO_HEIGHT_BOTTOM
		right = X_MIN+screenCenterX+(i+1)*NOTE_WIDTH
		color = BLUE if notes[i] else WHITE
		pygame.draw.polygon(screen, color, [[left,top], [right, top], [right, bottom], [left,bottom]], 0)

		#draw black keys
		if i < len(blackNotes) and blackNotes[i] != None:
			top = BLACK_KEY_HEIGHT_BOTTOM
			left = blackKeyXOffset+X_MIN+screenCenterX+(i-1)*blackNoteWidth +BLACK_KEY_SPACE
			bottom = top+10
			right = blackKeyXOffset+X_MIN+screenCenterX+(i)*blackNoteWidth -BLACK_KEY_SPACE
			color = BLUE if blackNotes[i] else BLACK
			pygame.draw.polygon(screen, color, [[left,top], [right, top], [right, bottom], [left,bottom]], 0)

	#draw outlines of the keys
	pygame.draw.line(screen, BLACK, (X_MIN+screenCenterX, PIANO_HEIGHT_BOTTOM+20), (X_MAX+screenCenterX, PIANO_HEIGHT_BOTTOM+20))
	pygame.draw.line(screen, BLACK, (X_MIN+screenCenterX,PIANO_HEIGHT_BOTTOM), (X_MAX+ screenCenterX, PIANO_HEIGHT_BOTTOM))
	for i in range(X_MIN,X_MAX+NOTE_WIDTH, NOTE_WIDTH):
		pygame.draw.line(screen, BLACK, (screenCenterX+i,PIANO_HEIGHT_BOTTOM), (screenCenterX+i, PIANO_HEIGHT_BOTTOM+20))
	

def drawPianoTop(notes, blackNotes):
	#draw piano keys top-view

	#bottom of keys -- bottom horizontal line
	pygame.draw.line(screen, BLACK, (X_MIN+screenCenterX, PIANO_HEIGHT_TOP), (X_MAX+screenCenterX, PIANO_HEIGHT_TOP))
	
	#top of keys -- top horizontal line
	pygame.draw.line(screen, BLACK, (X_MIN+screenCenterX, PIANO_HEIGHT_TOP-100), (X_MAX+screenCenterX, PIANO_HEIGHT_TOP-100))

	#draw polygons for the black keys
	numNotes = len(notes)
	blackNoteWidth = ((X_MAX+screenCenterX) - (X_MIN+screenCenterX)) / (numNotes)
	blackKeyXOffset = NOTE_WIDTH/2
	BLACK_KEY_SPACE = blackNoteWidth/5
	for i,noteval in enumerate(range(X_MIN,X_MAX, NOTE_WIDTH)):
		#draw white keys
		whiteLeft = X_MIN+screenCenterX+i*NOTE_WIDTH
		whiteTop = PIANO_HEIGHT_TOP-100
		whiteRight = X_MIN+screenCenterX+i*NOTE_WIDTH + NOTE_WIDTH
		whiteBottom = PIANO_HEIGHT_TOP
		color = BLUE if notes[i] else WHITE
		pygame.draw.polygon(screen, color, [[whiteLeft,whiteTop], [whiteRight, whiteTop], [whiteRight, whiteBottom], [whiteLeft,whiteBottom]], 0)
	

	for i,noteval in enumerate(range(X_MIN,X_MAX, NOTE_WIDTH)):
		#draw black keys on top of white keys
		if i < len(blackNotes) and blackNotes[i] != None:
			#square part of black keys	
			top = PIANO_HEIGHT_TOP-100
			left = blackKeyXOffset+X_MIN+screenCenterX+(i-1)*blackNoteWidth +BLACK_KEY_SPACE
			bottom = BLACK_KEY_HEIGHT_TOP
			right = blackKeyXOffset+X_MIN+screenCenterX+(i)*blackNoteWidth -BLACK_KEY_SPACE
			color = BLUE if blackNotes[i] else BLACK
			pygame.draw.polygon(screen, color, [[left,top], [right, top], [right, bottom], [left,bottom]], 0)

	#draw polygons for the white keys
	for i in range(X_MIN,X_MAX, NOTE_WIDTH):
		whiteLeft = screenCenterX+i
		whiteTop = PIANO_HEIGHT_TOP-100
		whiteRight = screenCenterX+i + NOTE_WIDTH
		whiteBottom = PIANO_HEIGHT_TOP
		pygame.draw.polygon(screen, BLACK, [[whiteLeft,whiteTop], [whiteRight, whiteTop], [whiteRight, whiteBottom], [whiteLeft,whiteBottom]], 1)
	

# initialize background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(WHITE)
screen.blit(background, (0,0))

# create finger sprites for each finger and each keyboard, put into left and right groups
rthumb = fingerSprite()
rindex = fingerSprite()
rmiddle = fingerSprite()
rring = fingerSprite()
rpinky = fingerSprite()

rhSpritesBottom = pygame.sprite.Group()
rhSpritesBottom.add(rthumb, rindex, rmiddle, rring, rpinky)
rhSpriteListBottom = [rthumb, rindex, rmiddle, rring, rpinky]

rthumb2 = fingerSprite()
rindex2 = fingerSprite()
rmiddle2 = fingerSprite()
rring2 = fingerSprite()
rpinky2 = fingerSprite()

rhSpritesTop = pygame.sprite.Group()
rhSpritesTop.add(rthumb2, rindex2, rmiddle2, rring2, rpinky2)
rhSpriteListTop = [rthumb2, rindex2, rmiddle2, rring2, rpinky2]


lthumb = fingerSprite()
lindex = fingerSprite()
lmiddle = fingerSprite()
lring = fingerSprite()
lpinky = fingerSprite()

lhSpritesBottom = pygame.sprite.Group()
lhSpritesBottom.add(lthumb, lindex, lmiddle, lring, lpinky)
lhSpriteListBottom = [lthumb, lindex, lmiddle, lring, lpinky]

lthumb2 = fingerSprite()
lindex2 = fingerSprite()
lmiddle2 = fingerSprite()
lring2 = fingerSprite()
lpinky2 = fingerSprite()

lhSpritesTop = pygame.sprite.Group()
lhSpritesTop.add(lthumb2, lindex2, lmiddle2, lring2, lpinky2)
lhSpriteListTop = [lthumb2, lindex2, lmiddle2, lring2, lpinky2]

#This array of which notes are playing is smaller than the number of notes that are in the
#noteIndexPlaying array. Will need to do some computation to figure out if the key is pressed.


pygame.display.update() #this is crucial -- writes the values to the screen

#TODO: Use the isPlayingList parameter once it's available from main.py
def update(position, notes, blackNotes): #, isPlayingList): #position is all the gesture info from the leap that is needed
	left = position.left
	right = position.right

	#TODO: There is a new threshold variable for playing because of the black keys, so you'll need to change when the finger color is updated
	#TODO: Fix the thresholding to lock the fingers in the screen/keyboard accurately
	#TODO: Notes highlight when being played
	#TODO: Fix the depth thresh -- make sure it's not inverting anything on the screen
	#TODO: Redraw the vertical black lines on top of the polygons for the bottom keyboard so that we can see the outlines when notes are highlighted
	for i in range(len(left)):
		# scale = int(8*(300+left[i].z)/500)
		scale = 4
		if left[i].y -90 >= MIDDLE_LINE_HEIGHT: #make it disappear because it is too high
			lhSpriteListBottom[i].update(left[i].x+screenCenterX, MIDDLE_LINE_HEIGHT, scale)
		else:
			lhSpriteListBottom[i].update(left[i].x+screenCenterX, V_THRESH-left[i].y + PIANO_HEIGHT_BOTTOM, scale)
		
		#update finger colors if playing
		if left[i].notePlaying != None:
			lhSpriteListBottom[i].updateColor(GREEN)
		else:
			lhSpriteListBottom[i].updateColor(BLACK)
		
		#top piano dots
		if BLACK_KEY_HEIGHT_TOP+ DEPTH_THRESH+left[i].z > MIDDLE_LINE_HEIGHT: #lock sprites to bottom of screen section
			lhSpriteListTop[i].update(left[i].x+screenCenterX, MIDDLE_LINE_HEIGHT, scale)
		elif BLACK_KEY_HEIGHT_TOP+ DEPTH_THRESH+left[i].z < PIANO_HEIGHT_TOP-100:
			lhSpriteListTop[i].update(left[i].x+screenCenterX, PIANO_HEIGHT_TOP-100, scale)
		else:
			depth_scale = 100.0/200
			lhSpriteListTop[i].update(left[i].x+screenCenterX, BLACK_KEY_HEIGHT_TOP+ DEPTH_THRESH+left[i].z*depth_scale, scale)

	for i in range(len(right)):
		scale = 4#int(8*(300+right[i].z)/500)
		if right[i].y -90 >= MIDDLE_LINE_HEIGHT:#make it lock to the top because it is too high
			rhSpriteListBottom[i].update(right[i].x+screenCenterX, MIDDLE_LINE_HEIGHT, scale)
		elif right[i].y -90 <= screenY - (PIANO_HEIGHT_BOTTOM +20): #lock sprites to the bottom of the keys
			rhSpriteListBottom[i].update(right[i].x+screenCenterX, PIANO_HEIGHT_BOTTOM+20, scale)
		else:
			rhSpriteListBottom[i].update(right[i].x+screenCenterX, V_THRESH-right[i].y + PIANO_HEIGHT_BOTTOM, scale)

		#update finger colors if playing
		if right[i].notePlaying != None:
			rhSpriteListBottom[i].updateColor(BLUE)
		else:
			rhSpriteListBottom[i].updateColor(RED)
		
		#top piano hands
		if BLACK_KEY_HEIGHT_TOP+ DEPTH_THRESH+right[i].z > MIDDLE_LINE_HEIGHT: #lock sprites to bottom of screen section
			rhSpriteListTop[i].update(right[i].x+screenCenterX, MIDDLE_LINE_HEIGHT, scale)
		elif BLACK_KEY_HEIGHT_TOP+ DEPTH_THRESH+right[i].z < PIANO_HEIGHT_TOP-100:
			rhSpriteListTop[i].update(right[i].x+screenCenterX, PIANO_HEIGHT_TOP-100, scale)
		else:
			depth_scale = 100.0/200
			rhSpriteListTop[i].update(right[i].x+screenCenterX, BLACK_KEY_HEIGHT_TOP+ DEPTH_THRESH+right[i].z*depth_scale, scale)
		

	#screen.blit(background, (0,0)) #erase screen (return to basic background) NEED THIS LINE
	rhSpritesBottom.clear(screen, background)
	rhSpritesBottom.draw(screen)
	lhSpritesBottom.clear(screen, background)
	lhSpritesBottom.draw(screen)
	lhSpritesTop.clear(screen, background)
	lhSpritesTop.draw(screen)
	rhSpritesTop.clear(screen, background)
	rhSpritesTop.draw(screen)
	pygame.draw.line(screen, BLACK, (0, MIDDLE_LINE_HEIGHT), (screenSize[0], MIDDLE_LINE_HEIGHT))
	#TODO: Add this back in once you get the isPlayingList
	#updateNotes(isPlayingList)
	drawPianoBottom(notes, blackNotes)
	drawPianoTop(notes, blackNotes)
	pygame.display.update() # redraw with *new* updates (similar to pygame.display.update())

