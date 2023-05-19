from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QMovie, QCursor, QIcon

class My_Cycle_Temp_Frame(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.frame_index = 8
        movie = QMovie("assets\mygif.gif")
        movie_label = QtWidgets.QLabel(self)
        movie_label.setMovie(movie)
        movie_label.setFixedSize(800, 600)
        movie.start()

        center_button_style = 'QPushButton { border: 2px solid black; border-radius: 10px; background-color: #72bcd4;}'
        lower_button_style = 'QPushButton { border: 2px solid red; border-radius: 10px; background-color: white;}'

        font = self.create_font('Arial', 18, True, True, 75)
       
        self.option_temp_0 = self.create_button(QtCore.QRect(70, 100, 180, 360), font, '30C' , '0_button', center_button_style)
        self.option_temp_1 = self.create_button(QtCore.QRect(310, 100, 180, 360), font, '60C', '1_button', center_button_style)
        self.option_temp_2 = self.create_button(QtCore.QRect(550, 100, 180, 360), font, '90C', '2_button', center_button_style)

        self.back_button = self.create_button(QtCore.QRect(70, 500, 301, 61), font, 'BACK', 'back_button', lower_button_style, 'assets/back.png', 50, 40)
        self.exit_button = self.create_button(QtCore.QRect(430, 500, 301, 61), font, 'EXIT', 'exit_button', lower_button_style, 'assets/exit.png', 50, 40)

        header = self.create_label(QtCore.QRect(355, 20, 281, 41), font, "TEMPERATURE", 'header')
        
        
    def create_font(self, family, size, bold: bool, italic: bool, weight):
        font = QtGui.QFont()
        font.setFamily(family)
        font.setPointSize(size)
        font.setBold(bold)
        font.setItalic(italic)
        font.setWeight(weight)
        return font
    
    def create_button(self, geom, font, text, name, style_sheet, icon_path=None, icon_width=None, icon_height=None):
        pushButton = QtWidgets.QPushButton(self)
        pushButton.setGeometry(QtCore.QRect(geom))
        if icon_path is not None:
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

