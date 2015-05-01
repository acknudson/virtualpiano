import sound
import config
import math

snd = sound.Sound()

V_THRESH = config.V_THRESH
BLACK_V_THRESH = config.BLACK_V_THRESH
DEPTH_THRESH = config.DEPTH_THRESH
NOTE_WIDTH = config.NOTE_WIDTH
X_MIN = config.X_MIN
X_MAX = config.X_MAX
PIANO_CENTER=24 #center the keyboard at middle C #len(snd.notesByIndex)/2 
padding = NOTE_WIDTH/7
BLACK_NOTE_WIDTH = config.BLACK_NOTE_WIDTH
FRONT_THRESH = config.FRONT_THRESH

# for calibrating where the white keys' y,z coordinates are on the piano table
val = 2
def setWhiteThresh(y,z):
	global V_THRESH
	global FRONT_THRESH
	V_THRESH = int(y)+val
	FRONT_THRESH = int(z)+val

# for calibrating where the black keys' y,z coordinates are on the piano table
def setBlackThresh(y,z):
	global BLACK_V_THRESH
	global DEPTH_THRESH
	BLACK_V_THRESH = int(y)+val
	DEPTH_THRESH = int(z)+val

note_cutoffs = range(X_MIN,X_MAX+NOTE_WIDTH, NOTE_WIDTH)
piano_size = len(note_cutoffs)
snd.setCurrentPiano(PIANO_CENTER-piano_size/2, PIANO_CENTER+piano_size/2)


def position_to_note_played(pos):

	snd.currentHoveringNote = [False]*len(snd.currentHoveringNote)
	snd.currentHoveringBlackNote = [False]*len(snd.currentHoveringBlackNote)

	for hand in pos.right, pos.left:
		for finger in hand:
			if finger.z > DEPTH_THRESH and finger.z < FRONT_THRESH: #play white notes
				if finger.y < V_THRESH:
					if finger.x > X_MIN and finger.x < X_MAX:
						for i in range(1,len(note_cutoffs)):
							if finger.x > note_cutoffs[i-1]+padding and finger.x < note_cutoffs[i]-padding:
								startPlaying(finger, i-1)
					else:
						stopPlaying(finger)
						stopPlayingBlack(finger)
				elif finger.x > X_MIN and finger.x < X_MAX:
					for i in range(1,len(note_cutoffs)):
						if finger.x > note_cutoffs[i-1]+padding and finger.x < note_cutoffs[i]-padding:
							snd.currentHoveringNote[i-1] = True
					stopPlaying(finger)
					stopPlayingBlack(finger)

				else:
					stopPlaying(finger)
					stopPlayingBlack(finger)

			elif finger.z < DEPTH_THRESH: #play black notes
				if finger.y < BLACK_V_THRESH:
					if finger.x > X_MIN and finger.x < X_MAX:
						for i in range(1,len(note_cutoffs)):
							if finger.x > (note_cutoffs[i-1]-NOTE_WIDTH/2)+padding and finger.x < (note_cutoffs[i]-NOTE_WIDTH/2)-padding:
								startPlayingBlack(finger, i-1)
					else:
						stopPlaying(finger)
						stopPlayingBlack(finger)
				elif finger.x > X_MIN and finger.x < X_MAX:
					for i in range(1,len(note_cutoffs)):
						if finger.x > (note_cutoffs[i-1]-NOTE_WIDTH/2)+padding and finger.x < (note_cutoffs[i]-NOTE_WIDTH/2)-padding:
							snd.currentHoveringBlackNote[i-1] = True
					stopPlaying(finger)
					stopPlayingBlack(finger)
				else:
					stopPlaying(finger)
					stopPlayingBlack(finger)
			else:
				stopPlaying(finger)
				stopPlayingBlack(finger)
	return (snd.currentNotesPlaying, snd.currentBlackNotesPlaying, snd.currentHoveringNote, snd.currentHoveringBlackNote)



def startPlaying(finger, note):
	if finger.notePlaying != None and note != finger.notePlaying:
		snd.noteOffByIndex(finger.notePlaying)
	finger.notePlaying = note
	snd.playNoteByIndex(finger.notePlaying)

def stopPlaying(finger):
	if finger.notePlaying != None:
		snd.noteOffByIndex(finger.notePlaying)
	finger.notePlaying = None

def startPlayingBlack(finger, note):
	if finger.notePlayingBlack != None and note != finger.notePlayingBlack:
		snd.blackNoteOffByIndex(finger.notePlayingBlack)
	finger.notePlayingBlack = note
	snd.playBlackNoteByIndex(finger.notePlayingBlack)

def stopPlayingBlack(finger):
	if finger.notePlayingBlack != None:
		snd.blackNoteOffByIndex(finger.notePlayingBlack)
	finger.notePlayingBlack = None


