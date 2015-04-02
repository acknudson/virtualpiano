import time
import fluidsynth

#adding a comment

fs = fluidsynth.Synth()
fs.start()

sfid = fs.sfload("YAMAHA DX7Piano.SF2")
fs.program_select(0, sfid, 0, 0)

fs.noteon(0, 60, 30)
fs.noteon(0, 67, 30)
fs.noteon(0, 76, 30)

time.sleep(1.0)

fs.noteoff(0, 60)
fs.noteoff(0, 67)
fs.noteoff(0, 76)

time.sleep(1.0)

seq = (79, 78, 79, 74, 79, 69, 79, 67, 79, 72, 79, 76,
       79, 78, 79, 74, 79, 69, 79, 67, 79, 72, 79, 76,
       79, 78, 79, 74, 79, 72, 79, 76, 79, 78, 79, 74,
       79, 72, 79, 76, 79, 78, 79, 74, 79, 72, 79, 76,
       79, 76, 74, 71, 69, 67, 69, 67, 64, 67, 64, 62,
       64, 62, 59, 62, 59, 57, 64, 62, 59, 62, 59, 57,
       64, 62, 59, 62, 59, 57, 43)

for note in seq:
    fs.noteon(0, note, 100) #0, note, volume/amplitude
    time.sleep(0.1)
    fs.noteoff(0, note)

scale = (60, 62, 64, 65, 67, 69, 71, 72)

for i in scale:
    #print i
    fs.noteon(0, i, 127)
    time.sleep(0.5)
    fs.noteoff(0, i)

for i in reversed(scale):
    fs.noteon(0, i, 127)
    time.sleep(0.5)
    fs.noteoff(0, i)

fs.delete()
