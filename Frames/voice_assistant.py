import pyttsx3
from PyQt5 import QtCore

class VoiceAssistance(QtCore.QObject):
    activation_signal = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.assistant = pyttsx3.init()
        self.assistant.setProperty('rate', 170)
        self.assistant.setProperty('voice', self.assistant.getProperty('voices')[1].id)
        self.prompt_dict = self.load_prompts()

    def speak(self, prompt: str):
        self.assistant.say(self.prompt_dict[prompt])
        self.assistant.runAndWait()
        self.activation_signal.emit()
        return

    def load_prompts(self):
        with open('frames/prompts.txt', 'r') as file:
            prompts = file.readlines()
        prompts = [line.strip() for line in prompts]
        prompt_dict = {}
        for pr in prompts:
            key, value = pr.split(':')
            prompt_dict[key.strip()] = value.strip()
        return prompt_dict



