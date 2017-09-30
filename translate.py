from test import *
from mido import Message, MidiFile, MidiTrack


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

	
def brainfrick_to_midi(bf_string):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=12, time=0))

    for bf_char in bf_string:
        onote = internal_bf_to_int(bf_char)
        if onote is -1:
            continue
        track.append(Message('note_on', note=onote, velocity=70, time=32))
        track.append(Message('note_off', note=onote, velocity=127, time=32))
        print(onote)
    
    mid.save('new_song.mid')
    
def internal_bf_to_int(bf_string):
    return {
        "+" : 60,
        "-" : 61,
        "<" : 62,
        ">" : 64,
        "[" : 65,
        "]" : 67,
        "." : 69,
        "," : 71
        }.get(bf_string, -1)
