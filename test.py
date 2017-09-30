import translate
import mido
import pyaudio
import wave
import numpy as np
import math
from collections import Counter
from midiutil.MidiFile import MIDIFile
from matplotlib.mlab import find

RATE = 44100
CHUNK = 1024

def mkStream(audio, **args):
    return audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK, **args)

def playMidi(fileName):
    port = mido.open_output()
    midi = mido.MidiFile(fileName)
    for msg in midi.play():
        port.send(msg)

# records audio from the mic
# Int -> [Frame]
def recordAudio(seconds):
    audio = pyaudio.PyAudio()
    stream = mkStream(audio)
    frames = int(RATE / CHUNK * seconds)
    result = [ stream.read(CHUNK) for _ in range(frames) ] # this is where the magic happens
    stream.stop_stream()
    stream.close()
    audio.terminate()
    return result

# plays the audio out loud
# [Frame] -> ()
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

    try:
        os.remove('test.midi')
    except:
        pass

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
    prevExists = True

    for frame in frames:
        if volume(frame) < 0.025:
            if prevExists:
                pitches.append(None)

            prevExists = False
            print("None")
            continue

        # unpack the data and times by the hamming window
        indata = np.array(wave.struct.unpack(
            "%dh" % (len(frame) / 2), frame)) * .53836 #??

        fftData = abs(np.fft.rfft(indata)) ** 2 # Take the fft and square each value
        which = fftData[1:].argmax() + 1 # find the maximum

        # use quadratic interpolation around the max
        if which != len(fftData) - 1:
            y0, y1, y2 = np.log(fftData[which - 1 : which + 2 :])
            x1 = (y2 - y0) / (4 * y1 - y2 - y0)
            freq = (which + x1) * RATE / CHUNK
        else:
            freq = which * RATE / CHUNK

        # 1334 -> 732

        pitch = 69 + round(12 * math.log(freq / 440, 2))

        if 50 < pitch < 80:
            pitch = pitch % 12 + 60
            pitches.append(pitch)
            print("Hertz: %s  Pitch: %s  Volume: %s" % (int(freq), pitch, volume(frame)))
            prevExists = True
        else:
            prevExists = False
            print("Pitch outside range")
            if prevExists:
                pitches.append(None)

    return pitches

def smoothenPitches(pitches, seconds):
    print(pitches)
    secondsPerPitch = 0.5
    # desiredPitches = seconds / secondsPerPitch
    # pitchesPerDesiredPitch = pitches / desiredPitches
    pitchesPerDesiredPitch = int(len(pitches) * secondsPerPitch / seconds)
    print("smoothenNum: %s" % pitchesPerDesiredPitch)
    
    smoothedPitches = []
    lists = [ pitches[i:] for i in range(pitchesPerDesiredPitch) ]

    for i, tempPitches in enumerate(zip(*lists)):
        if i % pitchesPerDesiredPitch == 0:
            mode = Counter(tempPitches).most_common(1)[0][0]
            smoothedPitches.append(mode)

    print(smoothedPitches)
    return smoothedPitches

def writeWav(frames):
    wavFile = wave.open('test.wav', 'wb')
    wavFile.setnchannels(1)
    wavFile.setsampwidth(2)
    wavFile.setframerate(RATE)
    wavFile.writeframes(b''.join(frames))
    wavFile.close()

if __name__ == '__main__':
    seconds = 5
    audio = recordAudio(seconds)
    pitches = smoothenPitches(getPitches(audio), seconds)
    genMidi(pitches, seconds)
    playMidi('test.midi')
    print(translate.convert('test.midi'))
