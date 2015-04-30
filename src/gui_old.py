import pygame
import config


# initialize pygame and the screen
pygame.init()
screen = pygame.display.set_mode(int(300*scaleX), int(300*scaleY))) # width, height values
screenSize = screen.get_size() # (width, height)
pygame.display.set_caption("LeaPiano")
screenX, screenY = screenSize[0:2]
screenCenterX = screenX/2
screenCenterY = screenY/2.0


#global variables
V_THRESH = config.V_THRESH
BLACK_V_THRESH = config.BLACK_V_THRESH
NOTE_WIDTH = int(config.NOTE_WIDTH * scaleX)
X_MIN = int(config.X_MIN * scaleX)
X_MAX = int(config.X_MAX * scaleX)
MIDDLE_LINE_HEIGHT = screenY/2.0

#bottom piano variables
DISTANCE_FROM_SCREEN_BOTTOM = int(60*scaleY)
BOTTOM_PIANO_TOP_LINE = screenY - DISTANCE_FROM_SCREEN_BOTTOM

WHITE_KEY_HEIGHT = int(20*scaleY)
BOTTOM_PIANO_BOTTOM_LINE = BOTTOM_PIANO_TOP_LINE + WHITE_KEY_HEIGHT
BLACK_KEY_HEIGHT_BOTTOM = BOTTOM_PIANO_TOP_LINE
BLACK_KEY_HEIGHT = int((BLACK_V_THRESH-V_THRESH) * scaleY)

#top piano variables
DISTANCE_FROM_MIDDLE_LINE = int(20*scaleY)
TOP_PIANO_BOTTOM_LINE = screenY - MIDDLE_LINE_HEIGHT - DISTANCE_FROM_MIDDLE_LINE
TOP_PIANO_TOP_LINE = TOP_PIANO_BOTTOM_LINE - int(100*scaleY)
TOP_PIANO_BLACK_KEY_HEIGHT = int(50*scaleY)
TOP_PIANO_BLACK_KEY_TOP = TOP_PIANO_BOTTOM_LINE - TOP_PIANO_BLACK_KEY_HEIGHT
DEPTH_THRESH = config.DEPTH_THRESH
Z_TOP_THRESH = -180
Z_BOTTOM_THRESH = -20
Z_BLACK_KEY_THRESH = -100



# initialize colors
RED   = (255,   0,   0)
BLUE  = (0,   128, 255)
GREEN = (0,   255,   0)
BLACK = (0,     0,   0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY =  (175, 175, 175)


class fingerSprite(pygame.sprite.Sprite): #may want to use the dirty sprite class for better rendering? 
	#https://www.pygame.org/docs/ref/sprite.html
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([5*scaleX,5*scaleY]) #hardcoded the width and height values of the sprite's image
		self.image.fill(BLACK) #hardcoded the color of the sprite
		self.rect = self.image.get_rect()

	def update(self, x, y):
		self.rect.x = x
		self.rect.y = y

	def updateColor(self, color):
		self.image.fill(color)

def drawPianoBottom(notes, blackNotes, noteHovering, blackNoteHovering):

	#add vertical lines for the keys below the middle horizontal line
	numNotes = len(notes)
	blackNoteWidth = ((X_MAX+screenCenterX) - (X_MIN+screenCenterX)) / (numNotes)
	blackKeyXOffset = NOTE_WIDTH/2
	BLACK_KEY_SPACE = blackNoteWidth/5
	color = WHITE
	for i,noteval in enumerate(range(X_MIN,X_MAX, NOTE_WIDTH)):
		#draw white keys
		top = BOTTOM_PIANO_TOP_LINE
		left = X_MIN+screenCenterX+i*NOTE_WIDTH
		bottom = BOTTOM_PIANO_BOTTOM_LINE
		right = X_MIN+screenCenterX+(i+1)*NOTE_WIDTH
		if i < numNotes:
			if notes[i]:
				color = BLUE 
			elif noteHovering[i]:
				color = LIGHT_GRAY
		# pygame.draw.polygon(screen, color, [[left,top], [right, top], [right, bottom], [left,bottom]], 0)

		#draw black keys
		if i < len(blackNotes) and blackNotes[i] != None:
			top = BLACK_KEY_HEIGHT_BOTTOM-BLACK_KEY_HEIGHT
			left = blackKeyXOffset+X_MIN+screenCenterX+(i-1)*blackNoteWidth +BLACK_KEY_SPACE
			bottom = BLACK_KEY_HEIGHT_BOTTOM
			right = blackKeyXOffset+X_MIN+screenCenterX+(i)*blackNoteWidth -BLACK_KEY_SPACE
			if blackNotes[i]:
				color = BLUE 
			elif blackNoteHovering[i]:
				color = LIGHT_GRAY
			else:
				color = BLACK
			pygame.draw.polygon(screen, color, [[left,top], [right, top], [right, bottom], [left,bottom]], 0)

	#draw outlines of the keys
	pygame.draw.line(screen, BLACK, (X_MIN+screenCenterX, BOTTOM_PIANO_TOP_LINE), (X_MAX+screenCenterX, BOTTOM_PIANO_TOP_LINE))
	pygame.draw.line(screen, BLACK, (X_MIN+screenCenterX,BOTTOM_PIANO_BOTTOM_LINE), (X_MAX+ screenCenterX, BOTTOM_PIANO_BOTTOM_LINE))
	for i in range(X_MIN,X_MAX+NOTE_WIDTH, NOTE_WIDTH):
		pygame.draw.line(screen, BLACK, (screenCenterX+i,BOTTOM_PIANO_TOP_LINE), (screenCenterX+i, BOTTOM_PIANO_BOTTOM_LINE))

	for i,noteval in enumerate(range(X_MIN,X_MAX, NOTE_WIDTH)):
		#draw black key outlines
		if i < len(blackNotes) and blackNotes[i] != None:
			top = BLACK_KEY_HEIGHT_BOTTOM-BLACK_KEY_HEIGHT
			left = blackKeyXOffset+X_MIN+screenCenterX+(i-1)*blackNoteWidth +BLACK_KEY_SPACE
			bottom = BLACK_KEY_HEIGHT_BOTTOM
			right = blackKeyXOffset+X_MIN+screenCenterX+(i)*blackNoteWidth -BLACK_KEY_SPACE
			pygame.draw.polygon(screen, BLACK, [[left,top], [right, top], [right, bottom], [left,bottom]], 1)	
	

def drawPianoTop(notes, blackNotes, noteHovering, blackNoteHovering):
	#draw piano keys top-view

	#draw polygons for the black keys
	numNotes = len(notes)
	blackNoteWidth = ((X_MAX+screenCenterX) - (X_MIN+screenCenterX)) / (numNotes)
	blackKeyXOffset = NOTE_WIDTH/2
	BLACK_KEY_SPACE = blackNoteWidth/5
	color = WHITE
	for i,noteval in enumerate(range(X_MIN,X_MAX, NOTE_WIDTH)):
		#draw white keys
		whiteLeft = X_MIN+screenCenterX+i*NOTE_WIDTH
		whiteTop = TOP_PIANO_TOP_LINE
		whiteRight = X_MIN+screenCenterX+i*NOTE_WIDTH + NOTE_WIDTH
		whiteBottom = TOP_PIANO_BOTTOM_LINE
		if i < numNotes:
			if notes[i]:
				color = BLUE 
			elif noteHovering[i]:
				color = LIGHT_GRAY
		pygame.draw.polygon(screen, color, [[whiteLeft,whiteTop], [whiteRight, whiteTop], [whiteRight, whiteBottom], [whiteLeft,whiteBottom]], 0)
	
	#draw outlines for the white keys
	for i in range(X_MIN,X_MAX, NOTE_WIDTH):
		whiteLeft = screenCenterX+i
		whiteTop = TOP_PIANO_TOP_LINE
		whiteRight = screenCenterX+i + NOTE_WIDTH
		whiteBottom = TOP_PIANO_BOTTOM_LINE
		pygame.draw.polygon(screen, BLACK, [[whiteLeft,whiteTop], [whiteRight, whiteTop], [whiteRight, whiteBottom], [whiteLeft,whiteBottom]], 1)
	

	for i,noteval in enumerate(range(X_MIN,X_MAX, NOTE_WIDTH)):
		#draw black keys on top of white keys
		if i < len(blackNotes) and blackNotes[i] != None:
			#key part of black keys	
			top = TOP_PIANO_TOP_LINE
			left = blackKeyXOffset+X_MIN+screenCenterX+(i-1)*blackNoteWidth +BLACK_KEY_SPACE
			bottom = TOP_PIANO_BLACK_KEY_TOP
			right = blackKeyXOffset+X_MIN+screenCenterX+(i)*blackNoteWidth -BLACK_KEY_SPACE
			if blackNotes[i]:
				color = BLUE 
			elif blackNoteHovering[i]:
				color = LIGHT_GRAY
			else:
				color = BLACK
			pygame.draw.polygon(screen, color, [[left,top], [right, top], [right, bottom], [left,bottom]], 0)

	#draw black outline
	for i,noteval in enumerate(range(X_MIN,X_MAX, NOTE_WIDTH)):
		if i < len(blackNotes) and blackNotes[i] != None:
			top = TOP_PIANO_TOP_LINE
			left = blackKeyXOffset+X_MIN+screenCenterX+(i-1)*blackNoteWidth +BLACK_KEY_SPACE
			bottom = TOP_PIANO_BLACK_KEY_TOP
			right = blackKeyXOffset+X_MIN+screenCenterX+(i)*blackNoteWidth -BLACK_KEY_SPACE
			pygame.draw.polygon(screen, BLACK, [[left,top], [right, top], [right, bottom], [left,bottom]], 1)

	

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

#position is all the gesture info from the leap
#notes is a list of booleans that indicates if the white key at an index is being played
#blackNotes is a list of booleans that indicates if the black key at an index is being played
#noteHovering is a list of booleans that indicates if the white key at an index is being hovered over by a finger
#blackNoteHovering is a list of booleans that indicates if the black key at an index is being hovered over by a finger
def update(position, notes, blackNotes, noteHovering, blackNoteHovering): 
	left = position.left
	right = position.right
	for i in range(len(left)):
		# if i == 1:
		# 	print left[i].y
		# 	print V_THRESH-left[i].y#+BOTTOM_PIANO_TOP_LINE
		# 	print "bottomline", BOTTOM_PIANO_BOTTOM_LINE - BOTTOM_PIANO_TOP_LINE
		#Bottom Piano Finger Position Dots
		if V_THRESH-left[i].y*scaleY+ BOTTOM_PIANO_TOP_LINE <= MIDDLE_LINE_HEIGHT: 
			#make it lock to the middle line because the finger is too high
			lhSpriteListBottom[i].update(left[i].x*scaleX+screenCenterX, MIDDLE_LINE_HEIGHT)
		elif V_THRESH-left[i].y*scaleY >= BOTTOM_PIANO_BOTTOM_LINE - BOTTOM_PIANO_TOP_LINE:
			if left[i].z*scaleZ <= Z_BLACK_KEY_THRESH:
				#lock on a black key if the finger is playing a black key
				lhSpriteListBottom[i].update(left[i].x*scaleX+screenCenterX, BOTTOM_PIANO_TOP_LINE-5) # -5 accounts for the size of the sprite
			else:
				#make it lock to the bottom of the keys because the finger is too low
				lhSpriteListBottom[i].update(left[i].x*scaleX+screenCenterX, BOTTOM_PIANO_BOTTOM_LINE-5) # -5 accounts for the size of the sprite
		else:
			lhSpriteListBottom[i].update(left[i].x*scaleX+screenCenterX, V_THRESH-left[i].y*scaleY + BOTTOM_PIANO_TOP_LINE)
		
		#Top Piano Finger Position Dots
		#if TOP_PIANO_BLACK_KEY_TOP+left[i].z > TOP_PIANO_BOTTOM_LINE:
		if left[i].z*scaleZ <= Z_TOP_THRESH:
			#lock sprites to the top of the top piano's screen section
			lhSpriteListTop[i].update(left[i].x*scaleX+screenCenterX, TOP_PIANO_TOP_LINE) 
		elif left[i].z*scaleZ >= Z_BOTTOM_THRESH:
			#lock sprites to bottom of the top piano's screen section
			lhSpriteListTop[i].update(left[i].x*scaleX+screenCenterX, TOP_PIANO_BOTTOM_LINE)
		else:
			depth_scale = abs(TOP_PIANO_TOP_LINE-TOP_PIANO_BOTTOM_LINE) /200.0
			lhSpriteListTop[i].update(left[i].x*scaleX+screenCenterX, TOP_PIANO_BOTTOM_LINE+left[i].z*depth_scale*scaleZ)

	for i in range(len(right)):
		if V_THRESH-right[i].y*scaleY + BOTTOM_PIANO_TOP_LINE <= MIDDLE_LINE_HEIGHT:
			# print V_THRESH-right[i].y + BOTTOM_PIANO_TOP_LINE 
			#make it lock to the top of the bottom piano's screen because the finger is too high
			rhSpriteListBottom[i].update(right[i].x*scaleX+screenCenterX, MIDDLE_LINE_HEIGHT)
		elif V_THRESH-right[i].y*scaleY >= BOTTOM_PIANO_BOTTOM_LINE - BOTTOM_PIANO_TOP_LINE:
			if right[i].z*scaleZ <= Z_BLACK_KEY_THRESH:
				#lock on a black key if the finger is playing a black key
				rhSpriteListBottom[i].update(right[i].x*scaleX+screenCenterX, BOTTOM_PIANO_TOP_LINE-5) # -5 accounts for the size of the sprite
			#make it lock to the bottom of the keys because the finger is too low
			else:
				rhSpriteListBottom[i].update(right[i].x*scaleX+screenCenterX, BOTTOM_PIANO_BOTTOM_LINE-5) # -5 accounts for the size of the sprite
		else:
			rhSpriteListBottom[i].update(right[i].x*scaleX+screenCenterX, V_THRESH-right[i].y*scaleY + BOTTOM_PIANO_TOP_LINE)
		
		#top piano hands
		if right[i].z*scaleZ <= Z_TOP_THRESH: #lock sprites to bottom of screen section
			rhSpriteListTop[i].update(right[i].x*scaleX+screenCenterX, TOP_PIANO_TOP_LINE)
		elif right[i].z*scaleZ >= Z_BOTTOM_THRESH:
			rhSpriteListTop[i].update(right[i].x*scaleX+screenCenterX, TOP_PIANO_BOTTOM_LINE)
		else:
			depth_scale = abs(TOP_PIANO_TOP_LINE-TOP_PIANO_BOTTOM_LINE) /200.0
			rhSpriteListTop[i].update(right[i].x*scaleX+screenCenterX, TOP_PIANO_BOTTOM_LINE+right[i].z*depth_scale*scaleZ)
		

	# drawPianoBottom(notes, blackNotes, noteHovering, blackNoteHovering)
	drawPianoTop(notes, blackNotes, noteHovering, blackNoteHovering)

	rhSpritesBottom.clear(screen, background)
	rhSpritesBottom.draw(screen)
	lhSpritesBottom.clear(screen, background)
	lhSpritesBottom.draw(screen)

	lhSpritesTop.clear(screen, background)
	lhSpritesTop.draw(screen)
	rhSpritesTop.clear(screen, background)
	rhSpritesTop.draw(screen)

	pygame.display.update() # redraw everything on the screen

