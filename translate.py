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
        }.get(note_num, "_")

def convert(fileName):
    midi = MidiFile('test.midi')
    
    for track in midi.tracks:
        brainfrick = ''

        for msg in track:
            if not msg.is_meta and msg.type != 'note_off':
                brainfrick += to_brainfrick((msg.bytes()[1] % 12) + 60)

    return brainfrick

# mid = MidiFile("test.midi")
# for i, track in enumerate(mid.tracks):
#     print("Track {}: {}".format(i, track.name))

#     brainfrick = ""
#     for msg in track:
#         if msg.is_meta or msg.type == "note_off":
#             continue
#         brainfrick += to_brainfrick((msg.bytes()[1] % 12) + 60)

#     print(brainfrick)
if __name__ == '__main__':
    print(convert('test.midi'))
