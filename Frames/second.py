from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QMovie, QCursor, QIcon

class Second_Frame(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        movie = QMovie("assets\mygif.gif")
        movie_label = QtWidgets.QLabel(self)
        movie_label.setMovie(movie)
        movie_label.setFixedSize(800, 600)
        movie.start()

        center_button_style = 'QPushButton { border: 2px solid black; border-radius: 10px; background-color: #72bcd4;}'
        lower_button_style = 'QPushButton { border: 2px solid red; border-radius: 10px; background-color: white;}'

        header_font = self.create_font('Arial', 15, True, True, 75)
        button_font = self.create_font('Arial', 10, True, True, 75)

        light_button = self.create_button(QtCore.QRect(70, 100, 180, 360), header_font, 'LIGHT' , 'light_button', center_button_style)
        dark_button = self.create_button(QtCore.QRect(310, 100, 180, 360), header_font, 'DARK', 'dark_button', center_button_style)
        mix_button = self.create_button(QtCore.QRect(550, 100, 180, 360), header_font, 'MIXED', 'mix_button', center_button_style)
        back_button = self.create_button(QtCore.QRect(70, 500, 301, 61), header_font, 'BACK', 'back_button', lower_button_style)
        exit_button = self.create_button(QtCore.QRect(430, 500, 301, 61), header_font, 'EXIT', 'exit_button', lower_button_style)

        back_button.clicked.connect(self.back_clicked)
        exit_button.clicked.connect(self.exit_clickled)

        header = self.create_label(QtCore.QRect(180, 20, 471, 41), header_font, "WHAT'S THE COLOR OF YOUR LOAD ?", 'header')

        exit = self.create_label(QtCore.QRect(440, 505, 50, 50), header_font, '', 'exit_img')
        self.bind_label_to_pixmap(exit, 'assets/exit.png')

        back = self.create_label(QtCore.QRect(80, 507.5, 45, 45), header_font, '', 'back_img')
        self.bind_label_to_pixmap(back, 'assets/back.png')
        
        


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
    
    def bind_label_to_pixmap(self, label, img_path):
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaled(label.size(), aspectRatioMode=True)
        label.setPixmap(pixmap)
        
    def exit_clickled(self):
        self.parent().setCurrentIndex(0)

    def back_clicked(self):
        self.parent().setCurrentIndex(1)

