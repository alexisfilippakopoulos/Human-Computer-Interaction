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

        center_button_style = 'QPushButton { border: 2px solid black; border-radius: 10px; background-color: #72bcd4;}'
        washer_button = self.create_button(QtCore.QRect(70, 110, 261, 360), header_font, '' , 'washer_button', center_button_style)
        dryer_button = self.create_button(QtCore.QRect(470, 110, 261, 360), header_font, '', 'dryer_button', center_button_style)

        washer_button.clicked.connect(self.button_clicked)
        #dryer_button.clicked.connect(self.button_clicked)

        lower_button_style = 'QPushButton { border: 2px solid red; border-radius: 10px; background-color: white;}'
        back_button = self.create_button(QtCore.QRect(70, 500, 261, 61), button_font, 'BACK', 'back_button', lower_button_style)
        exit_button = self.create_button(QtCore.QRect(470, 500, 261, 61), button_font, 'EXIT', 'exit_button', lower_button_style)

        back_button.clicked.connect(self.exit_clickled)
        exit_button.clicked.connect(self.exit_clickled)

        header = self.create_label(QtCore.QRect(230, 20, 360, 41), header_font, 'WASHER OR DRYER ?', 'header')

        washer_label = self.create_label(QtCore.QRect(130, 110, 150, 150), header_font, 'WASHER', 'washer_label')

        dryer_label = self.create_label(QtCore.QRect(545, 110, 150, 150), header_font, 'DRYER', 'dryer_label')

        washer = self.create_label(QtCore.QRect(135, 250, 150, 125), header_font, '', 'washer_img')
        self.bind_label_to_pixmap(washer, 'assets/washer.png')

        dryer = self.create_label(QtCore.QRect(530, 250, 150, 150), header_font, '', 'dryer_img')
        self.bind_label_to_pixmap(dryer, 'assets/dryer1.png')
    
        exit = self.create_label(QtCore.QRect(482, 510, 50, 40), header_font, '', 'exit_img')
        self.bind_label_to_pixmap(exit, 'assets/exit.png')

        back = self.create_label(QtCore.QRect(80, 510, 50, 40), header_font, '', 'back_img')
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

    def button_clicked(self):
        self.parent().setCurrentIndex(2)

