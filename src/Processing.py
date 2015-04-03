import sound

# initialize necessary sounds/scale
scale = ('C', 'D', 'E', 'F', 'G', 'A', 'B', 'C')
play = [False, False, False, False, False]
snd = sound.Sound()

V_THRESH = 90
NOTE_THRESH = 20

def position_to_note_played(pos):

	for finger in pos.right:
		if finger.y < V_THRESH:
			# snd.playNote(scale[0], 4)
			if finger.x > -150 and finger.x < 150:
				note_cutoffs = range(-160,160, 40)
				for i in range(1,len(note_cutoffs)):
					if finger.x > note_cutoffs[i-1] and finger.x < note_cutoffs[i]:
						if (i-1) < len(scale):
							startPlaying(finger, (scale[i-1], 4))
						else:
							startPlaying(finger, (scale[(i-1)%len(scale)], 4))
			else:
				stopPlaying(finger)
		else:
			stopPlaying(finger)

	for finger in pos.left:
		if finger.y < V_THRESH:
			# snd.playNote(scale[0], 4)
			if finger.x > -150 and finger.x < 150:
				note_cutoffs = range(-160,160, 40)
				for i in range(1,len(note_cutoffs)):
					if finger.x > note_cutoffs[i-1] and finger.x < note_cutoffs[i]:
						if (i-1) < len(scale):
							startPlaying(finger, (scale[i-1], 4))
						else:
							startPlaying(finger, (scale[(i-1)%len(scale)], 4))
			else:
				stopPlaying(finger)
		else:
			stopPlaying(finger)

	return play

def startPlaying(finger, note):
	if finger.notePlaying != None and note != finger.notePlaying:
		snd.noteOff(finger.notePlaying[0], finger.notePlaying[1])
	finger.notePlaying = note
	snd.playNote(finger.notePlaying[0], finger.notePlaying[1])

def stopPlaying(finger):
	if finger.notePlaying != None:
		snd.noteOff(finger.notePlaying[0], finger.notePlaying[1])
	finger.notePlaying = None



