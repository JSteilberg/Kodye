import pyaudio
import wave
import os, sys

RATE = 44100
CHUNK = 1024

def mkStream(audio, **args):
    return audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK, **args)

# records audio from the mic
# Int -> [Frame]
def recordAudio(seconds):
    audio = pyaudio.PyAudio()
    stream = mkStream(audio, stream_callback=callback)
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

def writeWav(frames, outName):
    try:
        os.remove(outName)
    except:
        pass

    wavFile = wave.open(outName, 'wb')
    wavFile.setnchannels(1)
    wavFile.setsampwidth(2)
    wavFile.setframerate(RATE)
    wavFile.writeframes(b''.join(frames))
    wavFile.close()


if __name__ == '__main__':
    writeWav(recordAudio(seconds = 5))
