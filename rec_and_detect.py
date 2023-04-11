import pyaudio
import wave
import whisper
import cv2
import cv2.data


CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SECONDS = 5

def record_audio(p):
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

    return frames

def store_input(frames, p, filepath):
    file = wave.open(f"{filepath}.wav", "wb")
    file.setnchannels(CHANNELS)
    file.setsampwidth(p.get_sample_size(FORMAT))
    file.setframerate(RATE)
    file.writeframes(b''.join(frames))
    file.close()
    print('recording stored')
    return

def decode_input(filepath, model):
    input = whisper.load_audio(file=filepath)
    input = whisper.pad_or_trim(input)
    mel = whisper.log_mel_spectrogram(input).to(model.device)
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model=model, mel=mel, options=options)
    
    return result.text
    

def main():
    p = pyaudio.PyAudio()
    model = whisper.load_model('base')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    detected_counter = 0
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (fx, fy , fw, fh) in faces:
            #roi_gray = gray[fy:fy+fw, fx:fx+fw]
            eyes = eye_cascade.detectMultiScale(gray[fy:fy+fw, fx:fx+fw], 1.3, 5)
        
        if len(faces) >= 1 and len(eyes) >= 2:
            print(detected_counter)
            detected_counter += 1
            if detected_counter >= 30:
                break
        
        

        

    cap.release()
    cv2.destroyAllWindows()
    input = record_audio(p)
    store_input(input, p, 'input1')
    dec_input = decode_input('input1.wav', model=model)
    print(f'Decoded Input: {dec_input}')

        

if __name__ == '__main__':
    main()


"""
        if len(faces) >= 1 and len(eyes) >= 2:
            print(detected_counter)
            detected_counter += 1
            if detected_counter >= 30:
                break
"""