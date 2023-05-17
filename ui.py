import pyttsx3
from PyQt5 import QtCore

class VoiceAssistance(QtCore.QObject):
    activation_signal = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.assistant = pyttsx3.init()
        self.assistant.setProperty('voice', self.assistant.getProperty('voices')[1].id)
        self.assistant.setProperty('rate', 165)

    def speak(self, prompt: str):
        self.assistant.say(prompt)
        self.assistant.runAndWait()


