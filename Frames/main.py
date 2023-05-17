from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from start import Starting_Screen 
from first_frame import First_Frame
from assistant_frame import Assistant_Frame
from second_frame import Second_Frame
from third_frame import Third_Frame
from fourth_frame import Fourth_Frame
from fifth_frame import Fifth_Frame
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
        self.frame_dict = {0: self.show_starting_frame, 1: self.show_assistant_frame, 2: self.show_first_frame, 3: self.show_second_frame, 4: self.show_third_frame}
        # create the screens and add them to the stacked widget
        self.start_screen = Starting_Screen()
        self.first_frame = First_Frame()
        self.second_frame = Second_Frame()
        self.assistant_frame = Assistant_Frame()
        self.third_frame = Third_Frame()
        self.fourth_frame = Fourth_Frame()
        self.fifth_frame = Fifth_Frame()
        
        self.stacked_widget.addWidget(self.start_screen)
        self.stacked_widget.addWidget(self.assistant_frame)
        self.stacked_widget.addWidget(self.first_frame)
        self.stacked_widget.addWidget(self.second_frame)
        self.stacked_widget.addWidget(self.third_frame)
        self.stacked_widget.addWidget(self.fourth_frame)
        self.stacked_widget.addWidget(self.fifth_frame)

        self.assist_frame_eval_dict = {'yes' : ['yes', 'yea', 'ye', 'sure', 'help', 'assist', 'do'], 'no' : ['no', 'nope', 'not', "n't"]}
        self.first_frame_eval_dict = {'yes': ['yes', 'recommend', 'sure', 'do', 'yeah', 'yea', 'propose'], 'no' : ['no', 'nope', 'not', "n't", "don't", 'own', 'my']}
        self.second_frame_eval_dict = {0: ['first', 'one','sixty', '1', '60', 'less', 'hour'], 1: ['two', '2', 'second', 'less', 'hours'], 3: ['third', 'three', 'more', 'plus', 'hours', 'or']}
        self.third_frame_eval_dict = {'light': ['light', 'white', 'gray', 'soft'], 'dark': ['black', 'dark', 'heavy'], 'mixed': ['mixed', 'both']}
        self.fourth_frame_eval_dict = {'sensitive': ['light', 'sensitive'], 'plain': ['clothes', 'plain', 'cotton'], 'heavy': ['heavy', 'jacket']}
        self.fifth_frame_eval_dict = {'small': ['small', 'little'], 'medium': ['medium'], 'large': ['large', 'lot']}
        self.back_exit_eval_dict = {'back': ['back', 'previous', 'last'], 'exit': ['start', 'over', 'exit']}

        self.frame_to_eval_dict = {0: self.back_exit_eval_dict, 1 : self.assist_frame_eval_dict, 2 : self.first_frame_eval_dict, 3: self.second_frame_eval_dict , 4: self.third_frame_eval_dict, 5: self.fourth_frame_eval_dict, 6: self.fifth_frame_eval_dict}
        self.frame_to_option_eval_dicts = {1 : self.assistant_frame_option_eval, 2 : self.first_frame_option_eval, 3: self.second_frame_option_eval, 4 : self.third_frame_option_eval, 5: self.fourth_frame_option_eval, 6: self.fifth_frame_option_eval}
        # Create a ThreadPoolExecutor with the desired number of worker threads
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

        # Submit the function calls to the executor for parallel execution
        executor.submit(self.starting_screen_functionality)
        executor.submit(self.first_frame_functionality)
        executor.submit(self.assistant_frame_functionality)
        executor.submit(self.second_frame_functionality)
        executor.submit(self.third_frame_functionality)
        executor.submit(self.fourth_frame_functionality)
        executor.submit(self.fifth_frame_functionality)
        executor.submit(self.activate_exit_buttons)
        executor.submit(self.activate_back_buttons)

        # Wait for all tasks to complete
        executor.shutdown()
        # set the current screen to screen 1
        threading.Thread(target=self.show_starting_frame, args=()).start()

    def show_starting_frame(self):
        """
        Show starting frame and enable face recognition.
        """
        self.current_widget_index = self.start_screen.frame_index
        self.stacked_widget.setCurrentWidget(self.start_screen)
        self.enable_face_rec()

    def show_assistant_frame(self):
        """
        Show second frame and disable face recognition. 
        Also make assistant say appropriate prompt.
        """
        self.current_widget_index = self.assistant_frame.frame_index
        # Close the camera since we moved from the starting screen
        self.face_rec.detection_event.set()
        self.stacked_widget.setCurrentWidget(self.assistant_frame)
        threading.Thread(target=self.assist_client, args=('intro',)).start()

    def show_first_frame(self):
        """
        Show recommendation question frame .
        """
        self.stacked_widget.setCurrentWidget(self.first_frame)
        self.current_widget_index = self.first_frame.frame_index

    def show_second_frame(self):
        """
        Show first recommendation question frame about time.
        """
        self.stacked_widget.setCurrentWidget(self.second_frame)
        self.current_widget_index = self.second_frame.frame_index

    def show_third_frame(self):
        """
        Show second recommendation question frame about color.
        """
        self.stacked_widget.setCurrentWidget(self.third_frame)
        self.current_widget_index = self.third_frame.frame_index

    def show_fourth_frame(self):
        self.stacked_widget.setCurrentWidget(self.fourth_frame)
        self.current_widget_index = self.fourth_frame.frame_index

    def show_fifth_frame(self):
        self.stacked_widget.setCurrentWidget(self.fifth_frame)
        self.current_widget_index = self.fifth_frame.frame_index

    def activate_exit_buttons(self):
        """
        Bind all exit buttons to their appropriate functionality.
        """
        self.first_frame.exit_button.clicked.connect(self.exit_functionality)
        self.assistant_frame.exit_button.clicked.connect(self.exit_functionality)
        self.second_frame.exit_button.clicked.connect(self.exit_functionality)
        self.third_frame.exit_button.clicked.connect(self.exit_functionality)
        self.fourth_frame.exit_button.clicked.connect(self.exit_functionality)

    def activate_back_buttons(self):
        """
        Bind all back buttons to their appropriate functionality.
        """
        self.first_frame.back_button.clicked.connect(self.back_functionality)
        self.assistant_frame.back_button.clicked.connect(self.back_functionality)
        self.second_frame.back_button.clicked.connect(self.back_functionality)
        self.third_frame.back_button.clicked.connect(self.back_functionality)
        self.fourth_frame.back_button.clicked.connect(self.back_functionality)

    def starting_screen_functionality(self):
        """
        Transition from starting screen to assistant frame using the buttons.
        """
        # connect the button clicked signal to a method that changes the current widget
        self.start_screen.pushButton.clicked.connect(self.show_assistant_frame)

    def assistant_frame_functionality(self):
        """
        Transition from recommendation screen to appropriate frame using the buttons.
        """
        self.assistant_frame.yes_button.clicked.connect(self.show_first_frame)
        self.assistant_frame.no_button.clicked.connect(self.show_first_frame)

    def first_frame_functionality(self):
        """
        Transition from first recommendation question to the next frame using the buttons.
        """
        self.first_frame.recomm_button.clicked.connect(self.show_second_frame)
        self.first_frame.my_button.clicked.connect(self.show_second_frame)
    
    def second_frame_functionality(self):
        """
        Bind second frame buttons to the function defining their fucntionality.
        """
        self.second_frame.option_0.clicked.connect(lambda: self.second_frame_button_functionality('0'))
        self.second_frame.option_1.clicked.connect(lambda: self.second_frame_button_functionality('1'))
        self.second_frame.option_2.clicked.connect(lambda: self.second_frame_button_functionality('2'))

    def second_frame_button_functionality(self, option):
        """
        Transition from third recommendation question to the next frame using the buttons and append the client's choice.
        """
        self.add_choice(option)
        self.show_third_frame()

    def third_frame_functionality(self):
        """
        Bind second frame buttons to the function defining their fucntionality.
        """
        self.third_frame.light_button.clicked.connect(lambda: self.third_frame_button_functionality('light'))
        self.third_frame.dark_button.clicked.connect(lambda: self.third_frame_button_functionality('dark'))
        self.third_frame.mix_button.clicked.connect(lambda: self.third_frame_button_functionality('mix'))

    def third_frame_button_functionality(self, option):
        """
        Transition from third recommendation question to the next frame using the buttons and append the client's choice.
        """
        self.add_choice(option)
        self.show_fourth_frame

    def fourth_frame_functionality(self):
        self.fourth_frame.sens_button.clicked.connect(lambda: self.fourth_frame_button_functionality('sensitive'))
        self.fourth_frame.plain_button.clicked.connect(lambda: self.fourth_frame_button_functionality('plain'))
        self.fourth_frame.heavy_button.clicked.connect(lambda: self.fourth_frame_button_functionality('heavy'))

    def fourth_frame_button_functionality(self, option):
        self.add_choice(f'{option}')
        self.show_fifth_screen()

    def fifth_frame_functionality(self):
        self.fourth_frame.sens_button.clicked.connect(lambda: self.fifth_frame_button_functionality('small'))
        self.fourth_frame.plain_button.clicked.connect(lambda: self.fifth_frame_button_functionality('medium'))
        self.fourth_frame.heavy_button.clicked.connect(lambda: self.fifth_frame_button_functionality('large'))

    def fifth_frame_button_functionality(self, option):
        self.add_choice(f'{option}')
        # show screen


    def back_functionality(self):
        """
        Back button fucntionality.
        Remove last choice and show previous frame.
        """
        self.recommendation_choices.pop() if len(self.recommendation_choices) != 0 else None
        print(self.recommendation_choices)
        print(f'Widget index: {self.current_widget_index} Difference: {self.current_widget_index - 1}')
        self.frame_dict[self.current_widget_index - 1]()

    def exit_functionality(self):
        """
        Exit button functionality.
        Clear client's choices and show starting frame.
        """
        # Clear the list and show starting screen
        self.recommendation_choices.clear()
        print(self.recommendation_choices)
        self.show_starting_frame()
        #threading.Thread(target=self.show_starting_frame, args=()).start()

    def add_choice(self, choice):
        """
        Add client's current choice to a list with his previous ones.
        """
        self.recommendation_choices.append(choice)
        print(self.recommendation_choices)

    def decode_audio(self):
        """
        Start a thread responsible for the speech recognition part
        """
        threading.Thread(target=self.enable_speech_rec, args=()).start()

    def enable_face_rec(self):
        """
        Enable face recognition, by opening the camera and clearing any detection events.
        """
        # Start the face recognition process
        self.face_rec = Face_Recognition()
        # Restarts the camera capture process
        self.face_rec.detection_event.clear()
        self.face_rec.detection_signal.connect(self.show_assistant_frame)
        self.face_rec.start()

    def assist_client(self, prompt):
        """
        Bind action that when assistant stops talking we start recording.
        Start saying appropriate prompt.
        """
        self.voice_assistant.activation_signal.connect(self.decode_audio)
        self.voice_assistant.speak(prompt)

    def enable_speech_rec(self):
        """
        Initiates the speech recognition process by creating a thread that captures the audio and returns a string of it.
        Calls for the response to be evaluated continues the program accordingly.
        """
        speech_rec = Speech_Recognition()
        speech_rec.start()
        decoded_audio = speech_rec.join()
        is_back_exit = self.evaluate_response(decoded_audio, True)
        print('Option with flag: ', is_back_exit)
        if is_back_exit == '0':
            option = self.evaluate_response(decoded_audio)
            self.frame_to_option_eval_dicts[self.current_widget_index](option)
        elif is_back_exit == 'back':
            self.back_functionality()
        elif is_back_exit == 'exit':
            self.exit_functionality()
        
    
    def evaluate_response(self, response, back_exit_flag=False):
        """
        Takes the client's verbal response as a string.
        Uses a dictionary where the keys are the question's options and the values keywords that hint towards it.
        Returns one option based on the highest number of keywords present in the response
        """
        matches_per_option = {}
        print(response)
        if back_exit_flag:
            print('Dict to be used for eval: ', self.frame_to_eval_dict[0])
            option = '0'
            for key, value in self.frame_to_eval_dict[0].items():
                matched_words = 0
                for v in value:
                    matched_words += 1 if response.__contains__(v) else 0
                matches_per_option[key] = matched_words
                print(f'Key: {key} Matched Words: {matched_words}')
                option = key if matched_words > 0 else '0' 
            return option
        else: 
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
        else:
            recomm_flag = False
            assist_thr = threading.Thread(target=self.voice_assistant.speak, args=('answ_2_no',))
            assist_thr.start()
        # Show appropriate screen
        self.show_second_frame()

    def second_frame_option_eval(self, option):
        self.add_choice(option)
        assist_thr = threading.Thread(target=self.voice_assistant.speak, args=(f'answ_3_{option}',))
        assist_thr.start()
        self.show_third_frame()

    def third_frame_option_eval(self, option):
        self.add_choice(f'{option}')
        # Say appropriate message
        assist_thr = threading.Thread(target=self.voice_assistant.speak, args=(f'answ_4_{option}',))
        assist_thr.start()
        # Show appropriate screen
        self.show_fourth_frame()

    def fourth_frame_option_eval(self, option):
        self.add_choice(f'{option}')
        assist_thr = threading.Thread(target=self.voice_assistant.speak, args=(f'answ_5_{option}',))
        assist_thr.start()
        self.show_fifth_frame()

    def fifth_frame_option_eval(self, option):
        self.add_choice(f'{option}')
        assist_thr = threading.Thread(target=self.voice_assistant.speak, args=(f'answ_6_{option}',))
        assist_thr.start()        


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setApplicationDisplayName('EasyWash')  # Set the display name
    app.setWindowIcon(QIcon('assets/favicon.png'))  # Set the icon
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec_()