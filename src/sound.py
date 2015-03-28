import time
import fluidsynth

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
fs = fluidsynth.Synth()
fs.start()
sfid = fs.sfload("YAMAHA DX7Piano.SF2")
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
    noteDict = {'A':  [21, 33, 45, 57, 69, 81, 93, 105],
                'As': [22, 34, 46, 58, 70, 82, 94, 106],
                'B':  [23, 35, 47, 59, 71, 83, 95, 107],
                'C':  [0, 24, 36, 48, 60, 72, 84, 96, 108],
                'Cs': [0, 25, 37, 49, 61, 73, 85, 97],
                'D':  [0, 26, 38, 50, 62, 74, 86, 98],
                'Ds': [0, 27, 39, 51, 63, 75, 87, 99],
                'E':  [0, 28, 40, 52, 64, 76, 88, 100],
                'F':  [0, 29, 41, 53, 65, 77, 89, 101],
                'Fs': [0, 30, 42, 54, 66, 78, 90, 102],
                'G':  [0, 31, 43, 55, 67, 79, 91, 103],
                'Gs': [0, 32, 44, 56, 68, 80, 92, 104]
                }

    

    def playNote(self, noteName, octave, volume=100):
        note = self.noteDict[noteName][octave]
        fs.noteon(0, note, volume)

    def noteOff(self, noteName, octave):
        note = self.noteDict[noteName][octave]
        fs.noteoff(0, note)

#Testing method
def testSound():
    s = Sound()
    s.playNote('A', 4)
    s.playNote('Cs', 5)
    s.playNote('E', 5)
    time.sleep(1)
    s.noteOff('A', 4)
    s.noteOff('Cs', 5)
    s.noteOff('E', 5)

#testSound()
