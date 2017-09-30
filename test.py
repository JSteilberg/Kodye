import pyaudio
import wave
import numpy as np
import math
from midiutil.MidiFile import MIDIFile

RATE = 44100
CHUNK = 1024

def mkStream(audio, **args):
    return audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK, **args)

# records audio from the mic
# Int -> [Frame]
def recordAudio(seconds):
    audio = pyaudio.PyAudio()
    stream = mkStream(audio)
    frames = int(RATE / CHUNK * seconds) #maybe long?
    result = [ stream.read(CHUNK) for _ in range(frames) ] # this is where the magic happens
    stream.stop_stream()
    stream.close()
    audio.terminate()
    return result

# plays the audio out loud
# Frame -> ()
def playAudio(frames):
    play = pyaudio.PyAudio()
    stream = mkStream(play, output=True)
    
    for frame in frames:
        stream.write(frame)

    stream.stop_stream()
    stream.close()
    play.terminate()

def genMidi(pitches, seconds):
    if not pitches:
        raise Exception("pitch please")

    midiFile = MIDIFile()
    midiFile.addTempo(0, 0, 60 * len(pitches) / seconds)
    pauses = 0

    for i, pitch in enumerate(pitches):
        if pitch == None:
            pauses += 1
        else:
            midiFile.addNote(0, 0, pitch, i + pauses, 1, 127)

    with open('test.midi', 'wb') as f:
        midiFile.writeFile(f)

def volume(frame):
    count = len(frame) / 2
    shorts = wave.struct.unpack("%dh" % count, frame)
    sumSquares = sum((sample / 32768) ** 2 for sample in shorts)
    return math.sqrt(sumSquares / count)

def rollingMax(frames):
    length = 5
    lists = [ frames[i:] for i in range(length) ]
    maxFrames = []

    for i, tempFrames in enumerate(zip(*lists)):
        if i % length != 0:
            continue

        maxVol = 0
        maxFrame = None

        for frame in tempFrames:
            if volume(frame) >= maxVol:
                maxVol = volume(frame)
                maxFrame = frame

        maxFrames.append(maxFrame)

    return maxFrames

def getPitches(frames):
    pitches = []
    frames = rollingMax(frames)

    for frame in frames:
        if volume(frame) < 0.015:
            pitches.append(None)
            continue
		
        # unpack the data and times by the hamming window
        indata = np.array(wave.struct.unpack(
            "%dh" % (len(frame) / 2), frame)) * .53836 #??
        print(indata)

        fftData = abs(np.fft.rfft(indata)) ** 2 # Take the fft and square each value
        which = fftData[1:].argmax() + 1 # find the maximum

        # use quadratic interpolation around the max
        if which != len(fftData) - 1:
            y0, y1, y2 = np.log(fftData[which - 1 : which + 2 :])
            x1 = (y2 - y0) / (4 * y1 - y2 - y0)
            # find the frequency and output it
            freq = (which + x1) * RATE / CHUNK
        else:
            freq = which * RATE / CHUNK

        # 1334 -> 732

        pitches.append(57 + round(12 * math.log(freq / 440, 2)))
        print("Hertz: %s  Pitch: %s  Volume: %s" % (freq, pitches[-1], volume(frame)))

    return pitches

    # smoothedPitches = []
    # smoothenNum = 5
    # lists = [ pitches[i:] for i in range(smoothenNum) ]

    # for i, tempPitches in enumerate(zip(*lists)):
    #     if i % smoothenNum == 0:

            # from collections import Counter
            # smoothedPitches.append(Counter(tempPitches).most_common(1)[0][0]) # mode
            # smoothedPitches.append(round(sum(tempPitches) / smoothenNum)) # mean

    # return smoothedPitches

if __name__ == '__main__':
    seconds = 15
    audio = recordAudio(seconds = seconds)
    pitches = getPitches(audio)
    genMidi(pitches, seconds)
