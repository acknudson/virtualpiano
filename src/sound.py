import time
import fluidsynth

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
fs = fluidsynth.Synth()
fs.start()
sfid = fs.sfload("AJH_Piano.sf2")
    #"jeuxdorgues.sf2")
    #"Claudio_Piano.SF2")
#AJH_Piano.sf2")#YAMAHA DX7Piano.SF2")
fs.program_select(0, sfid, 0, 0)
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Sound():
    """
    A dictionary that maps note names to a list of MIDI numbers. The MIDI values
    are arranged based on octave. The lowest is an A0, 27.5 Hz. The highest value
    is C8 or 4186 Hz. Middle C is C4 261.63 Hz. A4 is an A440.
    The values from C-G are padded with a 0 at the beginning to keep indexing
    consistent. Otherwise, a C4 would be found at C[3], while an A4 is A[4].
    The black keys are all sharps, or there would be a lot of duplicates, indicated
    by a small s next to the note name. 
    """

    noteIndexPlaying = [False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, False, False, 
    False, False, False, False, False]

    hoveringNote = [False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, False, False, 
    False, False, False, False, False]

    notesByIndex = [21,23,24,26,28,29,31,
        33,35,36,38,40,41,43,
        45,47,48,50,52,53,55,
        57,59,60,62,64,65,67,
        69,71,72,74,76,77,79,
        81,83,84,86,88,89,91,
        93,95,96,98,100,101,103,
        105,107,108]

    BlackNoteIndexPlaying = [None, False, None, False, False, None,
    False, False, False, None, False, False, None,
    False, False, False, None, False, False, None, 
    False, False, False, None, False, False, None, 
    False, False, False, None, False, False, None, 
    False, False, False, None, False, False, None, 
    False, False, False, None, False, False, None, 
    False, False, False, None]

    hoveringBlackNote = [None, False, None, False, False, None,
    False, False, False, None, False, False, None,
    False, False, False, None, False, False, None, 
    False, False, False, None, False, False, None, 
    False, False, False, None, False, False, None, 
    False, False, False, None, False, False, None, 
    False, False, False, None, False, False, None, 
    False, False, False, None]

    blackNotesByIndex = [0, 22,0,25,27,0,
        30,32,34,0,37,39,0,
        42,44,46,0,49,51,0,
        54,56,58,0,61,63,0,
        66,68,70,0,73,75,0,
        78,80,82,0,85,87,0,
        90,92,94,0,97,99,0,
        102,104,106,0]

    # print "blackkeys", len(blackNotesByIndex)
    # print "notesindex", len(notesByIndex)
    def __init__(self):
        self.currentPiano = self.notesByIndex
        self.currentNotesPlaying = self.noteIndexPlaying
        self.currentHoveringNote = self.hoveringNote

        self.currentBlackPiano = self.blackNotesByIndex
        self.currentBlackNotesPlaying = self.BlackNoteIndexPlaying
        self.currentHoveringBlackNote = self.hoveringBlackNote


    #play note based on index
    #ignores shaps
    def playNoteByIndex(self, noteIndex, volume=100):
        if not self.currentNotesPlaying[noteIndex]:
            note = self.currentPiano[noteIndex]
            fs.noteon(0, note, volume)
            self.currentNotesPlaying[noteIndex] = True

    def noteOffByIndex(self, noteIndex, volume=100):
        if self.currentNotesPlaying[noteIndex]:
            note = self.currentPiano[noteIndex]
            fs.noteoff(0, note)
            self.currentNotesPlaying[noteIndex] = False

    def playBlackNoteByIndex(self, noteIndex, volume=100):
        if self.currentBlackNotesPlaying[noteIndex] == None:
            return
        if self.currentBlackNotesPlaying[noteIndex] == False:
            note = self.currentBlackPiano[noteIndex]
            fs.noteon(0, note, volume)
            self.currentBlackNotesPlaying[noteIndex] = True

    def blackNoteOffByIndex(self, noteIndex, volume=100):
        if self.currentBlackNotesPlaying[noteIndex] == None:
            return
        if self.currentBlackNotesPlaying[noteIndex] == True:
            note = self.currentBlackPiano[noteIndex]
            fs.noteoff(0, note)
            self.currentBlackNotesPlaying[noteIndex] = False

    def setCurrentPiano(self, start, end):
        self.currentPiano = self.notesByIndex[start:end]
        self.currentNotesPlaying = self.noteIndexPlaying[start:end]
        self.currentHoveringNote = self.hoveringNote[start:end]

        self.currentBlackPiano = self.blackNotesByIndex[start:end+1]
        self.currentBlackNotesPlaying = self.BlackNoteIndexPlaying[start:end+1]
        self.currentHoveringBlackNote = self.hoveringBlackNote[start:end+1]

#Testing method
def testSound1():
    s = Sound()
##    s.playNote('A', 4)
##    s.playNote('Cs', 5)
    s.playNote('E',4)
    time.sleep(1)
##    s.noteOff('A', 4)
##    s.noteOff('Cs', 5)
    s.noteOff('E',4)

    s.playNote('F', 4)
    time.sleep(1)
    s.noteOff('F', 4)

def testSound2():
    s = Sound()
    # for i in range(len(s.notesByIndex)):
    #     s.playNoteByIndex(i)
    #     time.sleep(.05)
    #     s.noteOffByIndex(i)
    for i in range(18,35):
        s.playNoteByIndex(i)
        time.sleep(.5)
        s.noteOffByIndex(i)
        s.playBlackNoteByIndex(i)
        time.sleep(.5)
        s.blackNoteOffByIndex(i)

def testSound3():
    s = Sound()
    print len(s.blackNotesByIndex)
    print len(s.notesByIndex)

def testSound4():
    fs.noteon(0,45,100)
    time.sleep(.5)
    fs.noteoff(0,45)
    fs.noteon(0,0,100)
    time.sleep(.5)
    fs.noteoff(0,0) 
    fs.noteon(0,45,100)
    time.sleep(.5)
    fs.noteoff(0,45)


def testSound5():
    s = Sound()
    for i in range(len(s.blackNotesByIndex)):
        if s.blackNotesByIndex[i] != 0:
            s.playBlackNoteByIndex(i)
            time.sleep(.20)
            s.blackNoteOffByIndex(i)


# testSound5()
