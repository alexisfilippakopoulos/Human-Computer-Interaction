from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from start import Starting_Screen 
from one import First_Frame
from second import Second_Frame

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Track responses to use as predictors for the recommendation
        self.choices = []
        # create a stacked widget and set it as the central widget of the main window
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # create the screens and add them to the stacked widget
        self.start_screen = Starting_Screen()
        self.first_frame = First_Frame()
        self.second_frame = Second_Frame()

        self.stacked_widget.addWidget(self.start_screen)
        self.stacked_widget.addWidget(self.first_frame)
        self.stacked_widget.addWidget(self.second_frame)

        # set the current screen to screen 1
        self.stacked_widget.setCurrentWidget(self.start_screen)

        # connect the button clicked signal to a method that changes the current widget
        self.start_screen.pushButton.clicked.connect(self.show_first_frame)
        self.first_frame.washer_button.clicked.connect(self.show_second_frame)
        self.second_frame_functionality()
        # Exit Buttons
        self.activate_exit_buttons()
        # Back Buttons
        self.activate_back_buttons()


    def show_starting_frame(self):
        self.stacked_widget.setCurrentWidget(self.start_screen)

    def show_first_frame(self):
        self.stacked_widget.setCurrentWidget(self.first_frame)

    def show_second_frame(self):
        self.stacked_widget.setCurrentWidget(self.second_frame)

    def activate_exit_buttons(self):
        self.first_frame.exit_button.clicked.connect(self.exit_functionality)
        self.second_frame.exit_button.clicked.connect(self.exit_functionality)

    def activate_back_buttons(self):
        self.first_frame.back_button.clicked.connect(lambda: self.back_functionality(self.stacked_widget.currentIndex()))
        self.second_frame.back_button.clicked.connect(lambda: self.back_functionality(self.stacked_widget.currentIndex()))

    def second_frame_functionality(self):
        self.second_frame.light_button.clicked.connect(lambda: self.add_choice('light'))
        self.second_frame.dark_button.clicked.connect(lambda: self.add_choice('dark'))
        self.second_frame.mix_button.clicked.connect(lambda: self.add_choice('mix'))

    def back_functionality(self, widget_index):
        # Show previous screen and pop last choice
        self.stacked_widget.setCurrentIndex(widget_index - 1)
        self.choices.pop() if len(self.choices) != 0 else None

    def exit_functionality(self):
        # Clear the list and show starting screen
        self.choices.clear()
        self.show_starting_frame()

    def add_choice(self, choice):
        self.choices.append(choice)
        print(self.choices)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setApplicationDisplayName('EasyWash')  # Set the display name
    app.setWindowIcon(QIcon('assets/favicon.png'))  # Set the icon
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec_()