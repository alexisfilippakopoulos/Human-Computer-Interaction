from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from start import Starting_Screen 
from first_frame import First_Frame
from assistant_frame import Assistant_Frame
from second_frame import Second_Frame
from third_frame import Third_Frame
from fourth_frame import Fourth_Frame
from fifth_frame import Fifth_Frame
from my_cycle_hour import My_Cycle_Hour_Frame
from my_cycle_temp import My_Cycle_Temp_Frame
from type_frame import Type_Frame
from timer_frame import TimerFrame
from face_rec import Face_Recognition
from speech_rec import Speech_Recognition
from voice_assistant import VoiceAssistance
import threading
import sys
import winsound
import time
import simpleaudio as sa


recomm_flag = False
assistant_flag = True
end_face_flag = False

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Track responses to use as predictors for the recommendation
        self.wave_obj = sa.WaveObject.from_wave_file('assets/jazz.wav')
        self.wave_obj_alarm = sa.WaveObject.from_wave_file('assets/alarm.wav')
        self.play_obj = self.wave_obj.play()
        self.play_obj.stop()
        self.recommendation_choices = []
        self.voice_assistant = VoiceAssistance()
        self.voice_assistant.activation_signal.connect(self.decode_audio)
        # Create a stacked widget and set it as the central widget of the main window
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.frame_dict = {0: self.show_starting_frame, 1: self.show_assistant_frame, 2: self.show_first_frame, 3: self.show_second_frame, 4: self.show_third_frame,
                           5: self.show_fourth_frame, 6: self.show_fifth_frame, 7: self.show_my_cycle_hour_frame, 8: self.show_my_cycle_temp_frame, 
                           9:self.show_my_cycle_type_frame, 10: self.show_timer_frame}
        # Instanciate the screens and add them to the stacked widget
        self.start_screen = Starting_Screen()
        self.first_frame = First_Frame()
        self.second_frame = Second_Frame()
        self.assistant_frame = Assistant_Frame()
        self.third_frame = Third_Frame()
        self.fourth_frame = Fourth_Frame()
        self.fifth_frame = Fifth_Frame()
        self.my_cycle_hour_frame = My_Cycle_Hour_Frame()
        self.my_cycle_temp_frame = My_Cycle_Temp_Frame() 
        self.my_cycle_type_frame = Type_Frame()       
        self.stacked_widget.addWidget(self.start_screen)
        self.stacked_widget.addWidget(self.assistant_frame)
        self.stacked_widget.addWidget(self.first_frame)
        self.stacked_widget.addWidget(self.second_frame)
        self.stacked_widget.addWidget(self.third_frame)
        self.stacked_widget.addWidget(self.fourth_frame)
        self.stacked_widget.addWidget(self.fifth_frame)
        self.stacked_widget.addWidget(self.my_cycle_hour_frame)
        self.stacked_widget.addWidget(self.my_cycle_temp_frame)
        self.stacked_widget.addWidget(self.my_cycle_type_frame)
        # Dictionaries used to evaluate client's verbal input
        self.assist_frame_eval_dict = {'yes' : ['yes', 'yea', 'ye', 'sure', 'help', 'assist'], 'no' : ['no', 'nope', 'not', "n't", "dont"]}
        self.first_frame_eval_dict = {'yes': ['yes', 'recommend', 'sure', 'yeah', 'yea', 'propose'], 'no' : ['no', 'nope', 'not', "n't", "don't", 'own', 'my']}
        self.second_frame_eval_dict = {0: ['first', 'one','sixty', '1', '60', 'less', 'hour'], 1: ['two', '2', 'second', 'less', 'hours'], 2: ['third', 'three', 'more', 'plus', 'hours', 'or']}
        self.third_frame_eval_dict = {'light': ['light', 'white', 'gray', 'soft'], 'dark': ['black', 'dark', 'heavy'], 'mixed': ['mixed', 'both']}
        self.fourth_frame_eval_dict = {'sensitive': ['light', 'sensitive'], 'normal': ['clothes', 'normal', 'plain', 'cotton'], 'heavy': ['heavy', 'jacket']}
        self.fifth_frame_eval_dict = {'small': ['small', 'little'], 'medium': ['medium'], 'large': ['large', 'lot']}
        self.back_exit_xpln_eval_dict = {'back': ['goback', 'back', 'previous', 'last', 'previousquestion', 'lastquestion'], 'exit': ['start', 'over', 'exit', 'beginning', 'startover', 'thestart'], 'explain' : ['explain', 'analyse', 'help', 'further', 'question', 'understand']}
        # Dictionaries used to associate current frame with appropriate evaluation
        self.frame_to_eval_dict = {0: self.back_exit_xpln_eval_dict, 1 : self.assist_frame_eval_dict, 2 : self.first_frame_eval_dict, 3: self.second_frame_eval_dict , 4: self.third_frame_eval_dict, 5: self.fourth_frame_eval_dict, 6: self.fifth_frame_eval_dict}
        self.frame_to_option_eval_dicts = {1 : self.assistant_frame_option_eval, 2 : self.first_frame_option_eval, 3: self.second_frame_option_eval, 4 : self.third_frame_option_eval, 5: self.fourth_frame_option_eval, 6: self.fifth_frame_option_eval}
        # Go to the starting frame
        threading.Thread(target=self.show_starting_frame, args=()).start()


    def show_starting_frame(self):
        """
        Show starting frame and enable face recognition.
        """
        self.starting_screen_functionality()
        self.current_widget_index = self.start_screen.frame_index
        self.stacked_widget.setCurrentWidget(self.start_screen)
        self.play_obj = self.wave_obj.play()
        self.enable_face_rec()

    def show_assistant_frame(self):
        """
        Show second frame, disable face recognition, activate assistant. 
        """
        self.assistant_frame_functionality()
        self.play_obj.stop()
        self.current_widget_index = self.assistant_frame.frame_index
        # Close the camera since we moved from the starting screen
        self.face_rec.detection_event.set()
        self.stacked_widget.setCurrentWidget(self.assistant_frame)
        threading.Thread(target=self.assist_client, args=('intro',)).start()

    def show_first_frame(self):
        """
        Show recommendation question frame, change indexes.
        """
        self.first_frame_functionality()
        self.stacked_widget.setCurrentWidget(self.first_frame)
        self.current_widget_index = self.first_frame.frame_index

    def show_second_frame(self):
        """
        Show first recommendation question frame about time, change indexes.
        """
        self.second_frame_functionality()
        self.stacked_widget.setCurrentWidget(self.second_frame)
        self.current_widget_index = self.second_frame.frame_index

    def show_third_frame(self):
        """
        Show second recommendation question frame about color, change indexes.
        """
        self.third_frame_functionality()
        self.stacked_widget.setCurrentWidget(self.third_frame)
        self.current_widget_index = self.third_frame.frame_index

    def show_fourth_frame(self):
        """
        Show third recommendation question frame about garment type, change indexes.
        """
        self.fourth_frame_functionality()
        self.stacked_widget.setCurrentWidget(self.fourth_frame)
        self.current_widget_index = self.fourth_frame.frame_index

    def show_fifth_frame(self):
        """
        Show fourth recommendation question frame about size, change indexes.
        """
        self.fifth_frame_functionality()
        self.stacked_widget.setCurrentWidget(self.fifth_frame)
        self.current_widget_index = self.fifth_frame.frame_index

    def show_my_cycle_hour_frame(self):
        """
        Show my cycle time presets frame, change indexes.
        """
        self.my_cycle_hour_frame_functionallity()
        self.stacked_widget.setCurrentWidget(self.my_cycle_hour_frame)
        self.current_widget_index = self.my_cycle_hour_frame.frame_index

    def show_my_cycle_temp_frame(self):
        """
        Show my cycle degrees presets frame, change indexes.
        """
        self.my_cycle_temp_frame_functionallity()
        self.stacked_widget.setCurrentWidget(self.my_cycle_temp_frame)
        self.current_widget_index = self.my_cycle_temp_frame.frame_index

    def show_my_cycle_type_frame(self):
        """
        Show my cycle preset type frame, change indexes.
        """
        self.my_cycle_type_frame_functionallity()
        self.stacked_widget.setCurrentWidget(self.my_cycle_type_frame)
        self.current_widget_index = self.my_cycle_type_frame.frame_index

    def show_timer_frame(self):
        """if(int(self.recommendation_choices[0])<60):
            self.timer_frame = TimerFrame(0,int(self.recommendation_choices[0]),0)
        elif(int(self.recommendation_choices[0])==60 or int(self.recommendation_choices[0]) == 120 or int(self.recommendation_choices[0]) == 180):
            self.timer_frame = TimerFrame(int(self.recommendation_choices[0])/60,0,0)
        elif(int(self.recommendation_choices[0])==90):
            self.timer_frame = TimerFrame(1,30,0)"""
        self.timer_frame = TimerFrame(0, 0, 20)
        self.timer_frame.timer_signal.connect(self.timer_frame_functionality)
        self.stacked_widget.addWidget(self.timer_frame)
        self.stacked_widget.setCurrentWidget(self.timer_frame)
        self.current_widget_index = self.timer_frame.frame_index       

    def activate_exit_buttons(self):
        """
        Bind all exit buttons to their appropriate functionality.
        """
        self.first_frame.exit_button.clicked.connect(self.exit_functionality)
        self.assistant_frame.exit_button.clicked.connect(self.exit_functionality)
        self.first_frame.exit_button.clicked.connect(self.exit_functionality)
        self.second_frame.exit_button.clicked.connect(self.exit_functionality)
        self.third_frame.exit_button.clicked.connect(self.exit_functionality)
        self.fourth_frame.exit_button.clicked.connect(self.exit_functionality)
        self.fifth_frame.exit_button.clicked.connect(self.exit_functionality)
        self.my_cycle_hour_frame.exit_button.clicked.connect(self.exit_functionality)
        self.my_cycle_temp_frame.exit_button.clicked.connect(self.exit_functionality)
        self.my_cycle_type_frame.exit_button.clicked.connect(self.exit_functionality)

    def activate_back_buttons(self):
        """
        Bind all back buttons to their appropriate functionality.
        """
        self.first_frame.back_button.clicked.connect(self.back_functionality)
        self.assistant_frame.back_button.clicked.connect(self.back_functionality)
        self.first_frame.back_button.clicked.connect(self.back_functionality)
        self.second_frame.back_button.clicked.connect(self.back_functionality)
        self.third_frame.back_button.clicked.connect(self.back_functionality)
        self.fourth_frame.back_button.clicked.connect(self.back_functionality)
        self.fifth_frame.back_button.clicked.connect(self.back_functionality)
        self.my_cycle_hour_frame.back_button.clicked.connect(self.back_functionality)
        self.my_cycle_temp_frame.back_button.clicked.connect(self.back_functionality)
        self.my_cycle_type_frame.back_button.clicked.connect(self.back_functionality)

    def starting_screen_functionality(self):
        """
        Transition from starting screen to assistant frame using the buttons.
        """
        self.start_screen.pushButton.clicked.connect(self.show_assistant_frame)

    def assistant_frame_functionality(self):
        """
        Transition from recommendation screen to appropriate frame using the buttons.
        """
        self.assistant_frame.yes_button.clicked.connect(self.show_first_frame)
        self.assistant_frame.no_button.clicked.connect(self.show_first_frame)

    def first_frame_functionality(self):
        """
        Transition from assistant to recommendation question using the buttons.
        """
        self.first_frame.recomm_button.clicked.connect(self.show_second_frame)
        self.first_frame.my_button.clicked.connect(self.show_my_cycle_hour_frame)
    
    def second_frame_functionality(self):
        """
        Bind buttons from first recommendation question to second using the buttons.
        """
        self.second_frame.option_0.clicked.connect(lambda: self.second_frame_button_functionality('0'))
        self.second_frame.option_1.clicked.connect(lambda: self.second_frame_button_functionality('1'))
        self.second_frame.option_2.clicked.connect(lambda: self.second_frame_button_functionality('2'))

    def second_frame_button_functionality(self, option):
        """
        Transition from first recommendation question to second and save the choice.
        """
        self.add_choice(option)
        self.show_third_frame()

    def third_frame_functionality(self):
        """
        Bind second question buttons to the function defining their functionality.
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
        self.fourth_frame.normal_button.clicked.connect(lambda: self.fourth_frame_button_functionality('normal'))
        self.fourth_frame.heavy_button.clicked.connect(lambda: self.fourth_frame_button_functionality('heavy'))

    def fourth_frame_button_functionality(self, option):
        """
        Transition from third recommendation question to the next frame using the buttons and append the client's choice.
        """
        self.add_choice(f'{option}')
        self.show_fifth_frame()

    def fifth_frame_functionality(self):
        self.fourth_frame.sens_button.clicked.connect(lambda: self.fifth_frame_button_functionality('small'))
        self.fourth_frame.normal_button.clicked.connect(lambda: self.fifth_frame_button_functionality('medium'))
        self.fourth_frame.heavy_button.clicked.connect(lambda: self.fifth_frame_button_functionality('large'))

    def fifth_frame_button_functionality(self, option):
        """
        Transition from last recommendation question to the next frame using the buttons and append the client's choice.
        """
        self.add_choice(f'{option}')
        # show screen

    def my_cycle_hour_frame_functionallity(self):
        """
        Bind the my cycly hour question buttons to their functionality
        """
        self.my_cycle_hour_frame.option_hour_0.clicked.connect(lambda: self.my_cycle_hour_frame_button_functionallity("30"))
        self.my_cycle_hour_frame.option_hour_1.clicked.connect(lambda: self.my_cycle_hour_frame_button_functionallity("45"))
        self.my_cycle_hour_frame.option_hour_2.clicked.connect(lambda: self.my_cycle_hour_frame_button_functionallity("60"))
        self.my_cycle_hour_frame.option_hour_3.clicked.connect(lambda: self.my_cycle_hour_frame_button_functionallity("90"))
        self.my_cycle_hour_frame.option_hour_4.clicked.connect(lambda: self.my_cycle_hour_frame_button_functionallity("120"))
        self.my_cycle_hour_frame.option_hour_5.clicked.connect(lambda: self.my_cycle_hour_frame_button_functionallity("180"))

    def my_cycle_hour_frame_button_functionallity(self,option):
        """
        Transition from my own cycle hour question to the next frame using the buttons and append the client's choice.
        """
        self.add_choice(option)
        self.show_my_cycle_temp_frame()

    def my_cycle_temp_frame_functionallity(self):
        self.my_cycle_temp_frame.option_temp_0.clicked.connect(lambda: self.my_cycle_temp_frame_button_functionallity("30C"))
        self.my_cycle_temp_frame.option_temp_1.clicked.connect(lambda: self.my_cycle_temp_frame_button_functionallity("60C"))
        self.my_cycle_temp_frame.option_temp_2.clicked.connect(lambda: self.my_cycle_temp_frame_button_functionallity("90C"))

    def my_cycle_temp_frame_button_functionallity(self,option):
        """
        Transition from my own cycle temperature question to the next frame using the buttons and append the client's choice.
        """
        self.add_choice(option)
        self.show_my_cycle_type_frame()

    def my_cycle_type_frame_functionallity(self):
        self.my_cycle_type_frame.type_button_0.clicked.connect(lambda: self.my_cycle_type_frame_button_functionallity("sensitive"))
        self.my_cycle_type_frame.type_button_1.clicked.connect(lambda: self.my_cycle_type_frame_button_functionallity("normal"))
        self.my_cycle_type_frame.type_button_2.clicked.connect(lambda: self.my_cycle_type_frame_button_functionallity("heavy"))

    def my_cycle_type_frame_button_functionallity(self,option):
        self.add_choice(option)
        self.show_timer_frame()

    def timer_frame_functionality(self):
        #Kanei beep, deixnei allo screan p leei oti telos screen, enable camera kai molis pas apo panw kleinei
        global end_face_flag
        end_face_flag = True
        self.enable_face_rec()
        self.current_widget_index = self.start_screen.frame_index
        self.stacked_widget.setCurrentWidget(self.start_screen)
        self.wave_obj_alarm.play()

    def back_functionality(self):
        """
        Back button fucntionality.
        Remove last choice and show previous frame.
        """
        self.recommendation_choices.pop() if len(self.recommendation_choices) != 0 else None
        print(self.recommendation_choices)
        if(self.current_widget_index == 7):
            self.frame_dict[2]()
        else:
            self.frame_dict[self.current_widget_index - 1]()
        global assistant_flag
        self.assist_client(f'{self.current_widget_index + 1}_back_{self.current_widget_index}') if assistant_flag else 0
        if (assistant_flag is False and self.current_widget_index == 1):
            assistant_flag = True
            self.assist_client(f'{self.current_widget_index + 1}_back_{self.current_widget_index}') 

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
        Add client's current choice to a list with his 
        previous ones.
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
        self.face_rec.detection_signal.connect(self.handle_face_signal)
        self.face_rec.start()

    def handle_face_signal(self):
        global end_face_flag
        sys.exit(1) if end_face_flag else self.show_assistant_frame()

    def assist_client(self, prompt):
        """
        Start saying appropriate prompt.
        """
        self.voice_assistant.speak(prompt)


    def enable_speech_rec(self):
        """
        Initiates the speech recognition process by creating a thread that captures the audio and returns a string of it.
        Calls for the response to be evaluated continues the program accordingly.
        """
        global assistant_flag
        if assistant_flag:
            speech_rec = Speech_Recognition()
            speech_rec.start()
            decoded_audio = speech_rec.join()
            decoded_audio = ''.join(decoded_audio.lower().split())
            command_eval = self.evaluate_for_commands(decoded_audio)
            print('Command: ', command_eval)
            # 0 signals that neither back nor exit commands where detected
            if command_eval == '0':
                # Evaluate clients response using the question's dictionary of evaluation
                option_eval = self.evaluate_for_recommendation(decoded_audio)
                print('Option: ', option_eval)
                self.assist_client('repeat') if option_eval == 'None' else self.frame_to_option_eval_dicts[self.current_widget_index](option_eval)
            elif command_eval == 'back':
                self.back_functionality()
            elif command_eval == 'exit':
                self.exit_functionality()
            elif command_eval == 'explain':
                print('Explain: {self.current_widget_index}')
                self.assist_client(f'explain_{self.current_widget_index}') 

    def evaluate_for_commands(self, response):
        """
        Evaluate client's verbal input for the back, exit and explain commands.
        Takes the client's verbal response as a string.
        Uses a dictionary where the keys are the question's options and the values keywords that hint towards it.
        Returns one option based on the highest number of keywords present in the response
        """
        option = '0'
        matches = {}
        for key, value in self.frame_to_eval_dict[0].items():
            matched_words = 0
            for v in value:
                matched_words += 1 if response.__contains__(v) else 0
            matches[key] = matched_words
            print(f'Command: {key} Matched Words: {matched_words}')
            option = key if matched_words > 0 else option
        return option
        
    
    def evaluate_for_recommendation(self, response):
        """
        Takes the client's verbal response as a string.
        Uses a dictionary where the keys are the question's options and the values keywords that hint towards it.
        Returns one option based on the highest number of keywords present in the response
        """
        matches_per_option = {}
        for key, value in self.frame_to_eval_dict[self.current_widget_index].items():
            matched_words = 0
            for v in value:
                matched_words += 1 if response.__contains__(v) else 0
            matches_per_option[key] = matched_words
            print(f'Key: {key} Matched Words: {matched_words}')
        return 'None' if all(value == 0 for value in matches_per_option.values()) else max(matches_per_option, key=matches_per_option.get)   
        
    def assistant_frame_option_eval(self, option):
        """
        Assess client's response on the question presented on the assistant frame.
        Say and show the appropriate message and screen. 
        """
        global assistant_flag
        assistant_flag, prompt = (True, 'answ_1_yes') if option == 'yes' else (False, 'answ_1_no')
        print(f'Assistant Flag: {assistant_flag}')
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
        self.show_third_frame() if option != 'explain' else None
        
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