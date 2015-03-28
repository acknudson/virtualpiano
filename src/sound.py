import time
import fluidsynth

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

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
fs = fluidsynth.Synth()
fs.start()
sfid = fs.sfload("YAMAHA DX7Piano.SF2")
fs.program_select(0, sfid, 0, 0)
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

def playNote(noteName, octave, duration, volume=100):
    note = noteDict[noteName][octave]
    fs.noteon(0, note, volume)
    #time.sleep(duration)
    #fs.noteoff(0, note)

def noteOff(noteName, octave):
    note = noteDict[noteName][octave]
    fs.noteoff(0, note)


#Testing the functions
playNote('A', 4, 0.5)
playNote('Cs', 5, 0.5)
playNote('E', 5, 0.5)
time.sleep(1)
noteOff('A', 4)
noteOff('Cs', 5)
noteOff('E', 5)
