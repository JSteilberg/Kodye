import pyaudio
import wave
import os, sys
import time
from pynput.keyboard import Controller, Listener

# Sample rate, basically how many times/sec we grab a sound value
RATE = 44100

# Buffer to load
CHUNK = 1024

recording = False

# Makes a stream from pyaudio
# PyAudio, args -> AudioStream
def mkStream(audio, **args):
    return audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK, **args)


# records audio from the mic
# Int -> [Frame]
def recordAudio(outName):
    frames = []
    global recording
    recording = True

    def callback(in_data, frame_count, time_info, status):
        if recording:
            frames.append(in_data)
            state = pyaudio.paContinue
        else:
            writeWav(frames, outName)
            state = pyaudio.paComplete

        return (None, state)

    audio = pyaudio.PyAudio()
    stream = mkStream(audio, stream_callback=callback) # Get the audio as a stream
    stream.start_stream()


    def on_press(key):
        global recording
        recording = False
        return False

    Listener(on_press=on_press).start()

    while stream.is_active():
        time.sleep(0.25)

    # Cleanup
    stream.stop_stream()
    stream.close()
    audio.terminate()

# Plays the audio out loud
# [Frame] -> ()
def playAudio(frames):
    play = pyaudio.PyAudio()
    # Make an output stream
    stream = mkStream(play, output=True)

    # Play each frame
    for frame in frames:
        stream.write(frame)

    # Cleanup
    stream.stop_stream()
    stream.close()
    play.terminate()

# Writes a wav file given frames and a name
# [Frame], name -> ()
def writeWav(frames, outName):
    try:
        os.remove(outName)
    except:
        pass

    wavFile = wave.open(outName, 'wb')

    # Channels basically means instruments. We only have one (for now)
    wavFile.setnchannels(1)
    
    wavFile.setsampwidth(2)
    wavFile.setframerate(RATE)
    wavFile.writeframes(b''.join(frames))
    wavFile.close()


if __name__ == '__main__':
    recordAudio('keytest.wav')
