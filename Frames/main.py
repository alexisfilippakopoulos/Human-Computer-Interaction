from PyQt5 import QtWidgets
from start import Starting_Screen 
from one import First_Frame

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # create a stacked widget and set it as the central widget of the main window
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # create the screens and add them to the stacked widget
        self.start_screen = Starting_Screen()
        self.first_frame = First_Frame()

        self.stacked_widget.addWidget(self.start_screen)
        self.stacked_widget.addWidget(self.first_frame)

        # set the current screen to screen 1
        self.stacked_widget.setCurrentWidget(self.start_screen)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec_()