import simpleaudio as sa
from pydub import AudioSegment
import time

class Music_Player():
    def __init__(self, filepath):
        self.stop_flag = False
        self.filepath = filepath

    def play_song(self):
        wave_obj = sa.WaveObject.from_wave_file(self.filepath)
        play_obj = wave_obj.play()
        time.sleep(5)
        # Stop the audio playback when flag is raised
        play_obj.stop()
        time.sleep(5)

        play_obj = wave_obj.play()
        time.sleep(5)
        play_obj.stop()

    def stop_audio(self):
        self.stop_flag = True

# Path to your song file
song_file = "data/jazz.wav"

media = Music_Player(song_file)
media.play_song()


# Rest of your program...
