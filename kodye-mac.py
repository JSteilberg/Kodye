from record import *
from midi_fixer import fix
from translate import midi_to_brainfrick, brainfrick_to_midi
from subprocess import call

import os, sys

try:
    name = sys.argv[1]
except e:
    print("Usage: python kodye.py [name of output file]")
    print(e)
    exit()
    
# Get sounds from user
#audio_in = recordAudio(seconds)

# Get sounds from user
recordAudio(name + ".wav")

try:
    os.remove(name + '.mid')
except:
    pass

#writeWav(audio_in, name + ".wav")



call(["./libMac/sonic_annotator/sonic-annotator", # mac file change here
     "-d",
     "vamp:mtg-melodia:melodia:melody",
     "./" + name + ".wav",
     "-w",
     "midi"])

fix(name + ".mid", name + "_fixed.mid")

print(midi_to_brainfrick(name + "_fixed.mid"))
