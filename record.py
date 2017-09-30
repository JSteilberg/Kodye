import pyaudio
import wave

# Sample rate, basically how many times/sec we grab a sound value
RATE = 44100

# Buffer to load
CHUNK = 1024

# Makes a stream from pyaudio
# PyAudio, args -> AudioStream
def mkStream(audio, **args):
    return audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK, **args)

# records audio from the mic
# Int -> [Frame]
def recordAudio(seconds):
    audio = pyaudio.PyAudio()
    # Get the audio as a stream
    stream = mkStream(audio)
    # Divide the stream into frames, sort of like a video
    frames = int(RATE / CHUNK * seconds)
    result = [ stream.read(CHUNK) for _ in range(frames) ] # this is where the magic happens

    # Cleanup
    stream.stop_stream()
    stream.close()
    audio.terminate()
    return result

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
    # Open out file
    wavFile = wave.open(outName, 'wb')

    # Channels basically means instruments. We only have one (for now)
    wavFile.setnchannels(1)
    
    wavFile.setsampwidth(2)
    wavFile.setframerate(RATE)
    wavFile.writeframes(b''.join(frames))
    wavFile.close()

if __name__ == '__main__':
    writeWav(recordAudio(seconds = 5))
