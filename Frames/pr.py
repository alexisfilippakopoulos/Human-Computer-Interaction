import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Button with Icon Example")
        self.setGeometry(100, 100, 400, 300)

        # Set up the button
        self.button = QtWidgets.QPushButton(self)
        self.button.setGeometry(100, 100, 100, 100)
        self.button.setText("Click me")
        icon = QtGui.QIcon("assets/washer.png")
        self.button.setIcon(icon)
        self.button.setIconSize(QtCore.QSize(64, 64)) # Set the icon size

        # Set up the label
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(100, 220, 200, 30)
        self.label.setText("No button clicked yet")

        # Connect the button to a method that updates the label
        self.button.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        self.label.setText("Button clicked")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
