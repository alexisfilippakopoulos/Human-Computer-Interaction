import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel, QVBoxLayout, QMainWindow
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Washing Machine")
        self.setFixedSize(QSize(400, 300))

        # Create the main layout for the window
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Add buttons, labels, and other UI elements to the layout

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap("splash.png"))
        self.setFixedSize(QSize(400, 300))
        self.setMask(self.pixmap().mask())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the splash screen
    splash = SplashScreen()
    splash.show()

    # Create the main window
    main_window = MainWindow()
    main_window.show()

    # Hide the splash screen after 5 seconds
    timer = QTimer()
    timer.setInterval(5000)
    timer.timeout.connect(splash.close)
    timer.start()

    sys.exit(app.exec_())
