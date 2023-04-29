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

        header_font = self.create_font('Arial', 20, True, True, 75)
        button_font = self.create_font('Arial', 15, True, True, 75)

        center_button_style = 'QPushButton { border: 2px solid black; border-radius: 10px; background-color: white;}'
        self.washer_button = self.create_button(QtCore.QRect(70, 110, 261, 360), header_font, '' , 'washer_button', center_button_style, 'assets/washer.png', 150, 125)
        self.dryer_button = self.create_button(QtCore.QRect(470, 110, 261, 360), header_font, '', 'dryer_button', center_button_style, 'assets/dryer1.png', 150, 150)

        lower_button_style = 'QPushButton { border: 2px solid red; border-radius: 10px; background-color: white;}'
        self.back_button = self.create_button(QtCore.QRect(70, 500, 261, 61), button_font, 'BACK', 'back_button', lower_button_style, 'assets/back.png', 50, 40)
        self.exit_button = self.create_button(QtCore.QRect(470, 500, 261, 61), button_font, 'EXIT', 'exit_button', lower_button_style, 'assets/exit.png', 50, 40)

        header = self.create_label(QtCore.QRect(230, 20, 360, 41), header_font, 'WASHER OR DRYER ?', 'header')

        washer_label = self.create_label(QtCore.QRect(130, 110, 150, 150), header_font, 'WASHER', 'washer_label')

        dryer_label = self.create_label(QtCore.QRect(545, 110, 150, 150), header_font, 'DRYER', 'dryer_label')


    def create_font(self, family, size, bold: bool, italic: bool, weight):
        font = QtGui.QFont()
        font.setFamily(family)
        font.setPointSize(size)
        font.setBold(bold)
        font.setItalic(italic)
        font.setWeight(weight)
        return font
    
    def create_button(self, geom, font, text, name, style_sheet, icon_path, icon_width, icon_height):
        pushButton = QtWidgets.QPushButton(self)
        pushButton.setGeometry(QtCore.QRect(geom))
        icon = QtGui.QIcon(icon_path)
        pushButton.setIcon(icon)
        pushButton.setIconSize(QtCore.QSize(icon_width, icon_height))
        pushButton.setFont(font)
        pushButton.setObjectName(name)
        pushButton.setStyleSheet(style_sheet)
        pushButton.setText(text)
        return pushButton
    
    def create_label(self, geom, font, text, name, stylesheet=None):
        label = QtWidgets.QLabel(self)
        label.setGeometry(geom)
        label.setFont(font)
        label.setText(text)
        label.setObjectName(name)
        label.setStyleSheet(stylesheet)
        return label
        
    

