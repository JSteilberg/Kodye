import mido
import midiutil
import os, sys

class Note:
    def __init__(self, pitch, start, duration):
        self.pitch = pitch
        self.start = start
        self.duration = duration

# note = [pitch, duration, startTime]

def getNotes(events):
    notes = []
    currentTime = 0

    for event in events:
        if event.type == "note_on":
            notes.append(Note(event.note, currentTime, event.time))

        currentTime += event.time
    return notes

def mergeSameNotes(notes):
    mergedNotes = []
    current = None

    for note in notes:
        if current is None:
            # start a new note
            current = note

        elif note.pitch == current.pitch and current.start + current.duration - note.start < 0.01:
            # merge next note into current note
            current.duration = note.start + note.duration - current.start

        else:
            # finish current note
            mergedNotes.append(current)
            current = note

    return mergedNotes

def fixAdjacentNotes(notes):
    for note1, note2, note3 in zip(notes, notes[1:], notes[2:]):
        dStart = note2.start - (note1.start + note1.duration)
        dEnd   = note3.start - (note2.start + note2.duration)

        if note1.pitch == note3.pitch and abs(note1.pitch - note2.pitch) == 1 \
                and dStart < 0.01 and dEnd < 0.01 and note2.duration < 0.05:
            note2.pitch = note1.pitch

    return notes


def fix(fileName, outName):
    outFile = midiutil.MIDIFile()
    notes = getNotes(mido.MidiFile(fileName))
    notes = mergeSameNotes(notes)
    notes = fixAdjacentNotes(notes)
    notes = mergeSameNotes(notes)

    for note in notes:
        if note.duration > 0.1 and 40 < node.pitch < 90:
            outFile.addNote(0, 0, pitch=note.pitch, duration=2*note.duration, time=2*note.start, volume=127)

    try:
        os.remove(outName)
    except:
        pass

    with open(outName, 'wb') as f:
        outFile.writeFile(f)

if __name__ == '__main__':
    fix(sys.argv[1])
