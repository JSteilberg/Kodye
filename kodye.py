from record import *
from midi_fixer import fix
from translate import midi_to_brainfrick, brainfrick_to_midi
from subprocess import call

import sys

try:
    seconds = int(sys.argv[1])
    name = sys.argv[2]
except e:
    print("Usage: python kodeye.py [duration] [name]")
    print(e)
    exit()
# Get sounds from user
audio_in = recordAudio(seconds)

writeWav(audio_in, name + ".wav")

call(["./lib/sonic_annotator/sonic-annotator.exe",
     "-d",
     "vamp:mtg-melodia:melodia:melody",
     "./" + name + ".wav",
     "-w",
     "midi"])

fix(name + ".mid", name + "_fixed.mid")

print(midi_to_brainfrick(name + "_fixed.mid"))
