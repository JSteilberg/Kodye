import mido
import midiutil
import os, sys

def fix(fileName):
    inFile = mido.MidiFile(fileName)
    outFile = midiutil.MIDIFile()
    events = list(inFile)

    currentTime = 0
    smoothNotes = []
    currentNote = None # [pitch, duration, startTime]

    for event, nextEvent in zip(events, events[1:]):
        # print(event)
        if event.type == "note_on" and currentNote is None:
            # start a new note
            currentNote = [event.note, event.time, currentTime]

        elif event.type == "note_off" and nextEvent.type == "note_on" \
                and event.note == nextEvent.note and event.time < 0.01:
            # merge next note into current note
            currentNote[1] += nextEvent.time

        elif event.type == "note_off":
            # finish current note
            pitch, duration, startTime = currentNote

            if duration > 0.1:
                outFile.addNote(0, 0, pitch=pitch, duration=2*duration, time=2*startTime, volume=127)

            currentNote = None

        currentTime += event.time

    try:
        os.remove('out.mid')
    except:
        pass

    with open('out.mid', 'wb') as f:
        outFile.writeFile(f)

if __name__ == '__main__':
    fix(sys.argv[1])