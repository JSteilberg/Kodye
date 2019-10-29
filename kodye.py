from record import *
from midi_fixer import fix
from translate import midi_to_brainfrick, brainfrick_to_midi
from subprocess import call

import os, sys

try:
    name = sys.argv[1]
except:
    print("Usage: python kodye.py [name of output file]")
    exit()
    
# Get sounds from user
recordAudio(name + ".wav")

try:
    os.remove(name + '.mid')
except:
    pass

call(["sonic-annotator",
     "-d",
     "vamp:mtg-melodia:melodia:melody",
     "./" + name + ".wav",
     "-w",
     "midi"])

fix(name + ".mid", name + "_fixed.mid")

print(midi_to_brainfrick(name + "_fixed.mid"))
