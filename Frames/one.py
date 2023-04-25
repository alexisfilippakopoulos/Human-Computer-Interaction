from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QMovie, QCursor, QIcon, QPainter, QColor

class First_Frame(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        movie = QMovie("assets\mygif.gif")
        movie_label = QtWidgets.QLabel(self)
        movie_label.setMovie(movie)
        movie_label.setFixedSize(800, 600)
        movie.start()

        washer_icon = QIcon('assets/washer.png')
        dryer_icon = QIcon('assets/dryer1.png')

        header_font = self.create_font('Arial', 20, True, True, 75)
        button_font = self.create_font('Arial', 10, True, True, 75)

        center_button_style = 'QPushButton { border: 2px solid black; border-radius: 10px; background-color: #72bcd4;}'
        washer_button = self.create_button(QtCore.QRect(70, 150, 261, 360), header_font, 'WASHER' , 'washer_button', center_button_style, washer_icon)
        dryer_button = self.create_button(QtCore.QRect(470, 150, 251, 360), header_font, 'DRYER', 'dryer_button', center_button_style, dryer_icon)

        upper_button_style = 'QPushButton { border: 2px solid red; border-radius: 10px; background-color: white;}'
        back_button = self.create_button(QtCore.QRect(10, 10, 93, 61), button_font, 'BACK', 'back_button', upper_button_style)
        exit_button = self.create_button(QtCore.QRect(700, 10, 93, 61), button_font, 'EXIT', 'exit_button', upper_button_style)

        back_button.clicked.connect(self.exit_clickled)
        exit_button.clicked.connect(self.exit_clickled)

        header = self.create_label(QtCore.QRect(230, 20, 360, 41), header_font, 'WASHER OR DRYER ?', 'header')


    def create_font(self, family, size, bold: bool, italic: bool, weight):
        font = QtGui.QFont()
        font.setFamily(family)
        font.setPointSize(size)
        font.setBold(bold)
        font.setItalic(italic)
        font.setWeight(weight)
        return font
    
    def create_button(self, geom, font, text, name, style_sheet, icon=None):
        pushButton = QtWidgets.QPushButton(self)
        pushButton.setGeometry(QtCore.QRect(geom))
        pushButton.setIcon(icon) if icon != None else None
        pushButton.setFont(font)
        pushButton.setObjectName(name)
        pushButton.setStyleSheet(style_sheet)
        pushButton.setText(text)
        return pushButton
    
    def create_label(self, geom, font, text, name):
        label = QtWidgets.QLabel(self)
        label.setGeometry(geom)
        label.setFont(font)
        label.setText(text)
        label.setObjectName(name)
        return label
    
    def exit_clickled(self):
        self.parent().setCurrentIndex(0)

