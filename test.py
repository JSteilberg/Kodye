import pyaudio
 
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
 

def recordAudio(seconds):
    # start Recording
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = int(RATE / CHUNK * seconds)
    result = [ stream.read(CHUNK) for _ in range(frames) ] # this is where the magic happens
    stream.stop_stream()
    stream.close()
    audio.terminate()
    return result

def playAudio(frames):
    play = pyaudio.PyAudio()
    stream = play.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, output=True)

    for frame in frames:
        stream.write(frame)

    stream.stop_stream()
    stream.close()
    play.terminate()

if __name__ == '__main__':
    audio = recordAudio(seconds = 5)
    playAudio(audio)
