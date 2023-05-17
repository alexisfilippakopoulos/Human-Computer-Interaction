import pyaudio
import wave
import whisper
import cv2
import cv2.data
import pyttsx3


CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SECONDS = 5

def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,  output_device_index=0, frames_per_buffer=CHUNK_SIZE)

    frames = []
    print('recorded started')
    for i in range(0, int(RATE / CHUNK_SIZE * SECONDS)):
        data = stream.read(CHUNK_SIZE)
        print(data)
        frames.append(data)
    print('recorded ended')

    stream.stop_stream()
    stream.close()
    p.terminate()
    store_input(frames, p, 'input2')

def store_input(frames, p, filepath):
    with wave.open(f"{filepath}.wav", "wb") as file:
        file.setnchannels(CHANNELS)
        file.setsampwidth(p.get_sample_size(FORMAT))
        file.setframerate(RATE)
        file.writeframes(b''.join(frames))
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
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
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
        
        if cv2.waitKey(1) == ord('q'):
            break

        

    cap.release()
    cv2.destroyAllWindows()
    engine.say('Please tell me the degrees you wish')
    engine.runAndWait()
    record_audio()
    #store_input(input, p, 'input1')
    dec_input = decode_input('input1.wav', model=model)
    
    print(f'Decoded Input: {dec_input}')
    engine.say(f"Did you say {dec_input} ?")
    engine.runAndWait()

    record_audio()
    #store_input(input, p, 'input2')
    dec_input = decode_input('input2.wav', model=model)
    print(dec_input)
    if str(dec_input).lower().__contains__('yes'):
        engine.say('Okay !')
        engine.runAndWait()

        

if __name__ == '__main__':
    main()


"""
        if len(faces) >= 1 and len(eyes) >= 2:
            print(detected_counter)
            detected_counter += 1
            if detected_counter >= 30:
                break
"""