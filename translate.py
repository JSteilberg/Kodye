from test import *
from mido import Message, MidiFile, MidiTrack

TRANSLATE_TIME_ON = 256
TRANSLATE_TIME_OFF = 64

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

    print(brainfrick)

	
def brainfrick_to_midi(bf_string):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=0, time=0))

    for bf_char in bf_string:
        onote = internal_bf_to_int(bf_char)
        if onote is -1:
            continue
        track.append(Message('note_on', note=onote, velocity=70, time=TRANSLATE_TIME_OFF))
        track.append(Message('note_off', note=onote, velocity=127, time=TRANSLATE_TIME_ON))
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
