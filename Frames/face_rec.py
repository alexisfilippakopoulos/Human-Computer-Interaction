import threading
import cv2
import cv2.data
from PyQt5 import QtCore


class Face_Recognition(QtCore.QObject, threading.Thread):
    detection_signal = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.detected_counter = 0
        self.cap = cv2.VideoCapture(0)
        self.detection_event = threading.Event()

    def run(self):
        while not self.detection_event.is_set():
            ret, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (fx, fy, fw, fh) in faces:
                eyes = self.eye_cascade.detectMultiScale(gray[fy:fy + fw, fx:fx + fw], 1.3, 5)

            if len(faces) >= 1 and len(eyes) >= 2:
                #print(self.detected_counter)
                self.detected_counter += 1
                if self.detected_counter >= 30:
                    self.detection_signal.emit()
                    self.detected_counter = 0
                    break

            # wait for 1 millisecond for a key event
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def face_detected(self):
        self.detection_event.set()

def main():
    face = Face_Recognition()
    face.start()

if __name__ == '__main__':
    main()