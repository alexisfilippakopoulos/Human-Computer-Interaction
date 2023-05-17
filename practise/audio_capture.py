import pyaudio
import wave


CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)

frames = []
print('recorded started')
for i in range(0, int(RATE / CHUNK_SIZE * SECONDS)):
    data = stream.read(CHUNK_SIZE)
    frames.append(data)
print('recorded ended')

stream.stop_stream()
stream.close()
p.terminate()

file = wave.open("output.wav", "wb")
file.setnchannels(CHANNELS)
file.setsampwidth(p.get_sample_size(FORMAT))
file.setframerate(RATE)
file.writeframes(b''.join(frames))
file.close()
