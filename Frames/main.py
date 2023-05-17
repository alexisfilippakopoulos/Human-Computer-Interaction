from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from start import Starting_Screen 
from first_frame import First_Frame
from assistant_frame import Assistant_Frame
from third_frame import Third_Frame
from face_rec import Face_Recognition
from speech_rec import Speech_Recognition
from voice_assistant import VoiceAssistance
import threading
import concurrent.futures

recomm_flag = False
assistant_flag = False

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Track responses to use as predictors for the recommendation
        self.recommendation_choices = []
        self.voice_assistant = VoiceAssistance()
        # create a stacked widget and set it as the central widget of the main window
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # create the screens and add them to the stacked widget
        self.start_screen = Starting_Screen()
        self.first_frame = First_Frame()
        self.assistant_frame = Assistant_Frame()
        self.third_frame = Third_Frame()
        
        self.stacked_widget.addWidget(self.start_screen)
        self.stacked_widget.addWidget(self.assistant_frame)
        self.stacked_widget.addWidget(self.first_frame)
        self.stacked_widget.addWidget(self.third_frame)

        self.assist_frame_eval_dict = {'yes' : ['yes', 'yea', 'ye', 'sure', 'help', 'assist', 'do'], 'no' : ['no', 'nope', 'not', "n't"]}
        self.first_frame_eval_dict = {'yes': ['yes', 'recommend', 'sure', 'do', 'yeah', 'yea', 'propose'], 'no' : ['no', 'nope', 'not', "n't", "don't", 'own', 'my']}
        self.third_frame_eval_dict = {}

        self.frame_to_eval_dict = { 1 : self.assist_frame_eval_dict, 2 : self.first_frame_eval_dict}
        self.frame_to_option_eval_dicts = {1 : self.assistant_frame_option_eval, 2 : self.first_frame_option_eval}
        # Create a ThreadPoolExecutor with the desired number of worker threads
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

        # Submit the function calls to the executor for parallel execution
        executor.submit(self.starting_screen_functionality)
        executor.submit(self.first_frame_functionality)
        executor.submit(self.assistant_frame_functionality)
        executor.submit(self.third_frame_functionality)
        executor.submit(self.activate_exit_buttons)
        executor.submit(self.activate_back_buttons)

        # Wait for all tasks to complete
        executor.shutdown()
        # set the current screen to screen 1
        threading.Thread(target=self.show_starting_frame, args=()).start()

    def show_starting_frame(self):
        self.current_widget_index = self.start_screen.frame_index
        self.stacked_widget.setCurrentWidget(self.start_screen)
        self.enable_face_rec()

    def show_assistant_frame(self):
        self.current_widget_index = self.assistant_frame.frame_index
        # Close the camera since we moved from the starting screen
        self.face_rec.detection_event.set()
        self.stacked_widget.setCurrentWidget(self.assistant_frame)
        threading.Thread(target=self.assist_client, args=('intro',)).start()

    def show_first_frame(self):
        self.stacked_widget.setCurrentWidget(self.first_frame)
        self.current_widget_index = self.first_frame.frame_index

    def show_third_frame(self):
        self.stacked_widget.setCurrentWidget(self.third_frame)
        self.current_widget_index = self.third_frame.frame_index

    def activate_exit_buttons(self):
        self.first_frame.exit_button.clicked.connect(self.exit_functionality)
        self.assistant_frame.exit_button.clicked.connect(self.exit_functionality)
        self.third_frame.exit_button.clicked.connect(self.exit_functionality)

    def activate_back_buttons(self):
        self.first_frame.back_button.clicked.connect(self.back_functionality)
        self.assistant_frame.back_button.clicked.connect(self.back_functionality)
        self.third_frame.back_button.clicked.connect(self.back_functionality)

    def third_frame_functionality(self):
        self.third_frame.light_button.clicked.connect(lambda: self.add_choice('light'))
        self.third_frame.dark_button.clicked.connect(lambda: self.add_choice('dark'))
        self.third_frame.mix_button.clicked.connect(lambda: self.add_choice('mix'))

    def starting_screen_functionality(self):
        # connect the button clicked signal to a method that changes the current widget
        self.start_screen.pushButton.clicked.connect(self.show_assistant_frame)

    def first_frame_functionality(self):
        self.first_frame.recomm_button.clicked.connect(self.show_third_frame)
        self.first_frame.my_button.clicked.connect(self.show_third_frame)

    def assistant_frame_functionality(self):
        self.assistant_frame.yes_button.clicked.connect(self.show_first_frame)
        self.assistant_frame.no_button.clicked.connect(self.show_first_frame)

    def back_functionality(self):
        # Show previous screen and pop last choice
        # Pop last choice
        self.recommendation_choices.pop() if len(self.recommendation_choices) != 0 else None
        print(self.recommendation_choices)
        print(f'Widget index: {self.current_widget_index} Difference: {self.current_widget_index - 1}')
        self.frame_dict[self.current_widget_index - 1]()

    def exit_functionality(self):
        # Clear the list and show starting screen
        self.recommendation_choices.clear()
        print(self.recommendation_choices)
        self.show_starting_frame()
        #threading.Thread(target=self.show_starting_frame, args=()).start()

    def add_choice(self, choice):
        self.recommendation_choices.append(choice)
        print(self.recommendation_choices)

    def decode_audio(self):
        threading.Thread(target=self.enable_speech_rec, args=()).start()

    def enable_face_rec(self):
        # Start the face recognition process
        self.face_rec = Face_Recognition()
        # Restarts the camera capture process
        self.face_rec.detection_event.clear()
        self.face_rec.detection_signal.connect(self.show_assistant_frame)
        self.face_rec.start()

    def assist_client(self, prompt):
        self.voice_assistant.activation_signal.connect(self.decode_audio)
        self.voice_assistant.speak(prompt)

    def enable_speech_rec(self):
        """
        Initiates the speech recognition process by creating a thread that captures the audio and returns a string of it.
        Calls for the response to be evaluated continues the program accordingly.
        """
        self.speech_rec = Speech_Recognition()
        self.speech_rec.start()
        decoded_audio = self.speech_rec.join()
        option = self.evaluate_response(decoded_audio)
        self.frame_to_option_eval_dicts[self.current_widget_index](option)
        
    
    def evaluate_response(self, response):
        """
        Takes the client's verbal response as a string.
        Uses a dictionary where the keys are the question's options and the values keywords that hint towards it.
        Returns one option based on the highest number of keywords present in the response
        """
        print('Dict to be used for eval: ', self.frame_to_eval_dict[self.current_widget_index])
        matches_per_option = {}
        for key, value in self.frame_to_eval_dict[self.current_widget_index].items():
            matched_words = 0
            for v in value:
                matched_words += 1 if response.__contains__(v) else 0
            matches_per_option[key] = matched_words
        return max(matches_per_option, key=matches_per_option.get)
    
    def assistant_frame_option_eval(self, option):
        """
        Assess client's response on the question presented on the assistant frame.
        Say and show the appropriate message and screen. 
        """
        global assistant_flag
        assistant_flag, prompt = (True, 'answ_1_yes') if option == 'yes' else (False, 'answ_1_no')
        assist_thr = threading.Thread(target=self.voice_assistant.speak, args=(prompt,))
        assist_thr.start()
        self.show_first_frame()
    
    def first_frame_option_eval(self, option):
        """
        Assess client's response on the question presented on the first frame.
        Say and show the appropriate message and screen.
        """
        global recomm_flag
        if option == 'yes':
            recomm_flag = True
            # Show appropriate screen
            assist_thr = threading.Thread(target=self.voice_assistant.speak, args=('answ_2_yes',))
            assist_thr.start()
            self.show_third_frame()
        else:
            recomm_flag = False
            # Show appropriate screen



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setApplicationDisplayName('EasyWash')  # Set the display name
    app.setWindowIcon(QIcon('assets/favicon.png'))  # Set the icon
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec_()