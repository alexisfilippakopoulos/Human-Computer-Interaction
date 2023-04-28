from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QMovie, QCursor, QIcon

class Starting_Screen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        movie = QMovie("assets\mygif.gif")
        movie_label = QtWidgets.QLabel(self)
        movie_label.setMovie(movie)
        movie_label.setFixedSize(1000, 600)
        movie.start()

        header_font = self.create_font('Times New Roman', 40, True, True)
        button_font = self.create_font('Arial', 30, True, True)

        pushButton = self.create_button(QtCore.QRect(0, 70, 800, 600), button_font, '\nPRESS TO START', 'pushButton')
        pushButton.setStyleSheet('background-color: transparent;')
        pushButton.clicked.connect(self.clicked)

        header = self.create_label(QtCore.QRect(260, 10, 290, 100), header_font, 'EasyWash', 'header')
        logo = self.create_label(QtCore.QRect(330, 150, 150, 150), header_font, '', 'logo')
        pixmap = QPixmap('assets/favicon.png')
        pixmap = pixmap.scaled(logo.size(), aspectRatioMode=True)
        logo.setPixmap(pixmap)

    def create_font(self, family, size, bold: bool, italic: bool):
        font = QtGui.QFont()
        font.setFamily(family)
        font.setPointSize(size)
        font.setBold(bold)
        font.setItalic(italic)
        return font

    def create_button(self, geom, font, text, name, icon=None):
        pushButton = QtWidgets.QPushButton(self)
        pushButton.setGeometry(QtCore.QRect(geom))
        pushButton.setIcon(icon) if icon != None else None
        pushButton.setFont(font)
        pushButton.setText(text)
        pushButton.setObjectName(name)
        pushButton.setStyleSheet("background-color: #D3D3D3;")
        return pushButton
    
    def create_label(self, geom, font, text, name):
        label = QtWidgets.QLabel(self)
        label.setGeometry(geom)
        label.setFont(font)
        label.setText(text)
        label.setObjectName(name)
        return label
    
    
    
    def clicked(self):
        self.parent().setCurrentIndex(1)