import pygame
import config

#GUI scaling variables
scaleX = config.SCALE_X
scaleY = config.SCALE_Y
scaleYBottom = config.SCALE_Y_BOTTOM


# initialize pygame and the screen
pygame.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h)) #sets the width and height to be full screen based on the monitor
# screen = pygame.display.set_mode((1275, 750)) # width, height values
#LEE SCREEN: 1400,800
#AUBREY FULL SCREEN: 1280, 800
screenSize = screen.get_size() # (width, height)
pygame.display.set_caption("LeaPiano")
screenX, screenY = screenSize[0:2]
screenCenterX = screenX/2
screenCenterY = screenY/2.0


#global variables
V_THRESH = int(config.V_THRESH*scaleYBottom)
BLACK_V_THRESH = int(config.BLACK_V_THRESH*scaleYBottom)
NOTE_WIDTH = int(config.NOTE_WIDTH * scaleX)
X_MIN = int(config.X_MIN * scaleX)
X_MAX = int(config.X_MAX * scaleX)
MIDDLE_LINE_HEIGHT = screenY/2.0
DEPTH_THRESH = int(config.DEPTH_THRESH*scaleY) #cutoff between black and white keys
FRONT_THRESH = int(config.FRONT_THRESH*scaleY) #front z cutoff for white keys

# for calibrating where the white keys' y,z coordinates are on the piano table
def setWhiteThresh(y,z):
	global V_THRESH
	global FRONT_THRESH
	V_THRESH = int(y * scaleYBottom)
	FRONT_THRESH = int(z * scaleY)

# for calibrating where the black keys' y,z coordinates are on the piano table
def setBlackThresh(y,z):
	global BLACK_V_THRESH
	global DEPTH_THRESH
	BLACK_V_THRESH = int(y * scaleYBottom)
	DEPTH_THRESH = int(z * scaleY)

#bottom piano variables
BLACK_KEY_HEIGHT = BLACK_V_THRESH-V_THRESH #this is the length of the black key
WHITE_KEY_HEIGHT = BLACK_KEY_HEIGHT*1.25 #this is the length of the white key
BOTTOM_PIANO_TOP_LINE = MIDDLE_LINE_HEIGHT*3/2 #this is the top of the white keys
BOTTOM_PIANO_BOTTOM_LINE = MIDDLE_LINE_HEIGHT*3/2 + WHITE_KEY_HEIGHT #this is the bottom of the white keys

#top piano variables
TOP_PIANO_LENGTH = int(100*scaleY) #length of the piano
TOP_PIANO_BOTTOM_LINE = MIDDLE_LINE_HEIGHT/2 + TOP_PIANO_LENGTH/2 #this is the bottom of the piano
TOP_PIANO_TOP_LINE = MIDDLE_LINE_HEIGHT/2 - TOP_PIANO_LENGTH/2 #top of the piano
TOP_PIANO_BLACK_KEY_LENGTH = TOP_PIANO_LENGTH*1/2 #length of the black keys
TOP_PIANO_BLACK_KEY_BOTTOM = TOP_PIANO_BOTTOM_LINE - TOP_PIANO_BLACK_KEY_LENGTH #bottom of the black keys (top of the black keys is the same as the top of the white keys)


SPRITE_SIZE = 5*scaleX


# initialize colors
RED   = (255,   0,   0)
BLUE  = (0,   128, 255)
GREEN = (0,   255,   0)
BLACK = (0,     0,   0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY =  (175, 175, 175)

BLACK_KEY_OUTLINE_COLOR = DARK_GRAY
WHITE_KEY_OUTLINE_COLOR = DARK_GRAY


class fingerSprite(pygame.sprite.Sprite): 
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([SPRITE_SIZE,SPRITE_SIZE]) #hardcoded the width and height values of the sprite's image
		self.image.fill(DARK_GRAY) #hardcoded the color of the sprite
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
	for i in range(numNotes):
		#draw white keys
		top = BOTTOM_PIANO_TOP_LINE
		left = X_MIN+screenCenterX+i*NOTE_WIDTH
		bottom = BOTTOM_PIANO_BOTTOM_LINE
		right = X_MIN+screenCenterX+(i+1)*NOTE_WIDTH
		color = WHITE
		if notes[i]: #if it's playing, change key to blue
			color = BLUE 
		elif noteHovering[i]: #if finger is above key, change key to gray
			color = LIGHT_GRAY
		pygame.draw.polygon(screen, color, [[left,top], [right, top], [right, bottom], [left,bottom]], 0) 
		pygame.draw.polygon(screen, WHITE_KEY_OUTLINE_COLOR, [[left,top], [right, top], [right, bottom], [left,bottom]], 1) #key outline

		#draw black keys
		if blackNotes[i] != None:
			top = BOTTOM_PIANO_TOP_LINE-BLACK_KEY_HEIGHT
			left = blackKeyXOffset+X_MIN+screenCenterX+(i-1)*blackNoteWidth +BLACK_KEY_SPACE
			bottom = BOTTOM_PIANO_TOP_LINE
			right = blackKeyXOffset+X_MIN+screenCenterX+(i)*blackNoteWidth -BLACK_KEY_SPACE
			if blackNotes[i]:
				color = BLUE 
			elif blackNoteHovering[i]:
				color = LIGHT_GRAY
			else:
				color = BLACK
			pygame.draw.polygon(screen, color, [[left,top], [right, top], [right, bottom], [left,bottom]], 0)
			pygame.draw.polygon(screen, BLACK_KEY_OUTLINE_COLOR, [[left,top], [right, top], [right, bottom], [left,bottom]], 1) #key outline

	#outline bottom piano
	top = BOTTOM_PIANO_TOP_LINE
	bottom = BOTTOM_PIANO_BOTTOM_LINE
	left = X_MIN+screenCenterX
	right = X_MAX+screenCenterX
	pygame.draw.polygon(screen, BLACK, [[left,top], [right, top], [right, bottom], [left,bottom]], 1)
	

def drawPianoTop(notes, blackNotes, noteHovering, blackNoteHovering):
	#draw piano keys top-view

	#draw polygons for the black keys
	numNotes = len(notes)
	blackNoteWidth = ((X_MAX+screenCenterX) - (X_MIN+screenCenterX)) / (numNotes)
	blackKeyXOffset = NOTE_WIDTH/2
	BLACK_KEY_SPACE = blackNoteWidth/5
	color = WHITE
	for i in range(numNotes):
		#draw white keys
		whiteLeft = X_MIN+screenCenterX+i*NOTE_WIDTH
		whiteTop = TOP_PIANO_TOP_LINE
		whiteRight = X_MIN+screenCenterX+i*NOTE_WIDTH + NOTE_WIDTH
		whiteBottom = TOP_PIANO_BOTTOM_LINE
		color = WHITE
		if notes[i]:
			color = BLUE 
		elif noteHovering[i]:
			color = LIGHT_GRAY
		pygame.draw.polygon(screen, color, [[whiteLeft,whiteTop], [whiteRight, whiteTop], [whiteRight, whiteBottom], [whiteLeft,whiteBottom]], 0)
		pygame.draw.polygon(screen, WHITE_KEY_OUTLINE_COLOR, [[whiteLeft,whiteTop], [whiteRight, whiteTop], [whiteRight, whiteBottom], [whiteLeft,whiteBottom]], 1) #outline keys

	for i in range(numNotes):
		#draw black keys on top of white keys
		if blackNotes[i] != None:
			#key part of black keys	
			top = TOP_PIANO_TOP_LINE
			left = blackKeyXOffset+X_MIN+screenCenterX+(i-1)*blackNoteWidth +BLACK_KEY_SPACE
			bottom = TOP_PIANO_BLACK_KEY_BOTTOM
			right = blackKeyXOffset+X_MIN+screenCenterX+(i)*blackNoteWidth -BLACK_KEY_SPACE
			if blackNotes[i]:
				color = BLUE 
			elif blackNoteHovering[i]:
				color = LIGHT_GRAY
			else:
				color = BLACK
			pygame.draw.polygon(screen, color, [[left,top], [right, top], [right, bottom], [left,bottom]], 0)
			pygame.draw.polygon(screen, BLACK_KEY_OUTLINE_COLOR, [[left,top], [right, top], [right, bottom], [left,bottom]], 1) #outline keys

	#outline top piano
	top = TOP_PIANO_TOP_LINE
	bottom = TOP_PIANO_BOTTOM_LINE
	left = X_MIN+screenCenterX
	right = X_MAX+screenCenterX
	pygame.draw.polygon(screen, BLACK, [[left,top], [right, top], [right, bottom], [left,bottom]], 1)


def updateFingers(position):
	hands = [position.left, position.right]

	for h,hand in enumerate(hands):
		for i in range(len(hand)):			
			#draw top piano fingers
			depth_scale = (TOP_PIANO_BOTTOM_LINE - TOP_PIANO_BLACK_KEY_BOTTOM *1.0)/(FRONT_THRESH-DEPTH_THRESH)
			shift = (TOP_PIANO_BOTTOM_LINE*DEPTH_THRESH - FRONT_THRESH* TOP_PIANO_BLACK_KEY_BOTTOM*1.0)/(DEPTH_THRESH-FRONT_THRESH )
			top_x = hand[i].x*scaleX+screenCenterX
			top_y = hand[i].z*scaleY*depth_scale+shift
			if top_y > MIDDLE_LINE_HEIGHT:
				top_y = MIDDLE_LINE_HEIGHT-SPRITE_SIZE #snap to bottom of top half
			elif top_y < 0:
				top_y = 0 #snap to top of screen
			spriteGroups[1][h][i].update(top_x, top_y)


			#draw bottom piano fingers
			bottom_x = hand[i].x*scaleX+screenCenterX
			bottom_y = V_THRESH-hand[i].y*scaleYBottom + BOTTOM_PIANO_TOP_LINE
			if bottom_y < MIDDLE_LINE_HEIGHT:
				bottom_y = MIDDLE_LINE_HEIGHT+ SPRITE_SIZE #snap finger to top of bototm half
			elif bottom_y > screenY:
				bottom_y = screenY - SPRITE_SIZE #snap finger to the bottom of the screen
			else:
				if top_y < TOP_PIANO_BLACK_KEY_BOTTOM: #if finger is above black keys
					if bottom_y > BOTTOM_PIANO_TOP_LINE: #if finger is below end of black keys
						bottom_y = BOTTOM_PIANO_TOP_LINE- SPRITE_SIZE #snap finger to the bottom of black keys

			spriteGroups[0][h][i].update(bottom_x, bottom_y)
	

# initialize background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(LIGHT_GRAY)
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

spriteGroups = [[lhSpriteListBottom, rhSpriteListBottom],[lhSpriteListTop, rhSpriteListTop]]

pygame.display.update() #this is crucial -- writes the values to the screen

#position is all the gesture info from the leap
#notes is a list of booleans that indicates if the white key at an index is being played
#blackNotes is a list of booleans that indicates if the black key at an index is being played
#noteHovering is a list of booleans that indicates if the white key at an index is being hovered over by a finger
#blackNoteHovering is a list of booleans that indicates if the black key at an index is being hovered over by a finger
def update(position, notes, blackNotes, noteHovering, blackNoteHovering): 
	drawPianoBottom(notes, blackNotes, noteHovering, blackNoteHovering)
	drawPianoTop(notes, blackNotes, noteHovering, blackNoteHovering)

	updateFingers(position)

	rhSpritesBottom.clear(screen, background)
	rhSpritesBottom.draw(screen)
	lhSpritesBottom.clear(screen, background)
	lhSpritesBottom.draw(screen)

	lhSpritesTop.clear(screen, background)
	lhSpritesTop.draw(screen)
	rhSpritesTop.clear(screen, background)
	rhSpritesTop.draw(screen)

	pygame.draw.line(screen, BLACK, (0, MIDDLE_LINE_HEIGHT), (screenX, MIDDLE_LINE_HEIGHT))
	pygame.display.update() # redraw everything on the screen

