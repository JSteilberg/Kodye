from test import *
from mido import MidiFile


def to_brainfrick(note_num):
    return {
        60 : "+",
        61 : "-",
        62 : "<",
        64 : ">",
        65 : "[",
        67 : "]",
        69 : ".",
        71 : ","
        }.get(note_num, "oops!")

mid = MidiFile("./audio_samples/scale.mid")
for i, track in enumerate(mid.tracks):
    print("Track {}: {}".format(i, track.name))

    brainfrick = ""
    for msg in track:
        if msg.is_meta or msg.type == "note_off":
            continue
        brainfrick += to_brainfrick((msg.bytes()[1] % 12) + 60)

    print(brainfrick)
