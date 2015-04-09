import sound
import config
import math

# initialize necessary sounds/scale
scale = ('C', 'D', 'E', 'F', 'G', 'A', 'B', 'C')
snd = sound.Sound()

V_THRESH = config.V_THRESH
NOTE_WIDTH = config.NOTE_WIDTH
X_MIN = config.X_MIN
X_MAX = config.X_MAX
PIANO_CENTER=len(snd.notesByIndex)/2 

def position_to_note_played(pos):

	for hand in pos.right, pos.left:
		for finger in hand:
			if finger.y < V_THRESH:
				# snd.playNote(scale[0], 4)
				if finger.x > X_MIN and finger.x < X_MAX:
					note_cutoffs = range(X_MIN,X_MAX+NOTE_WIDTH, NOTE_WIDTH)
					midpoint = int(math.ceil(len(note_cutoffs)/2))
					for i in range(1,len(note_cutoffs)):
						if finger.x > note_cutoffs[i-1] and finger.x < note_cutoffs[i]:
							# if (i-1) < len(scale):
							# 	startPlaying(finger, (scale[i-1], 4))
							# else:
							# 	startPlaying(finger, (scale[(i-1)%len(scale)], int(4+round((i-1)/len(scale)))))
							if i-1 > midpoint:
								startPlaying(finger,PIANO_CENTER+(i-1-midpoint))
							else:
								startPlaying(finger, PIANO_CENTER-(midpoint-(i-1)))
				else:
					stopPlaying(finger)
			else:
				stopPlaying(finger)


# def startPlaying(finger, note):
# 	if finger.notePlaying != None and note != finger.notePlaying:
# 		snd.noteOff(finger.notePlaying[0], finger.notePlaying[1])
# 	finger.notePlaying = note
# 	snd.playNote(finger.notePlaying[0], finger.notePlaying[1])

# def stopPlaying(finger):
# 	if finger.notePlaying != None:
# 		snd.noteOff(finger.notePlaying[0], finger.notePlaying[1])
# 	finger.notePlaying = None

def startPlaying(finger, note):
	if finger.notePlaying != None and note != finger.notePlaying:
		snd.noteOffByIndex(finger.notePlaying)
	finger.notePlaying = note
	snd.playNoteByIndex(finger.notePlaying)

def stopPlaying(finger):
	if finger.notePlaying != None:
		snd.noteOffByIndex(finger.notePlaying)
	finger.notePlaying = None



