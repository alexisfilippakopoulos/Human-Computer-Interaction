import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QMovie, QCursor, QIcon
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
import pygame


class TimerFrame(QWidget):
    def __init__(self,hours,minutes,seconds):
        super().__init__()
        self.frame_index = 10
        movie = QMovie("assets\mygif.gif")
        movie_label = QtWidgets.QLabel(self)
        movie_label.setMovie(movie)
        movie_label.setFixedSize(800, 600)
        movie.start()

        center_button_style = 'QPushButton { border: 2px solid black; border-radius: 10px; background-color: #72bcd4;}'
        lower_button_style = 'QPushButton { border: 2px solid red; border-radius: 10px; background-color: white;}'

        font = self.create_font('Arial', 18, True, True, 75)

        header = self.create_label(QtCore.QRect(270, 20, 281, 41), font, "TIME LEFT", 'header')


        timer_font = self.create_font('Arial',50,True,True,75)
        self.label = self.create_label(QtCore.QRect(230, 250, 350, 80), timer_font,"","")


        pygame.init()
        pygame.mixer.music.load("data/jazz.mp3")
        pygame.mixer.music.play(-1)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = QTime(hours,minutes,seconds)
        self.update_label()
        
        self.timer.start(1000)  # Timer fires every 1 second

        
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
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName(name)
        label.setStyleSheet(stylesheet)
        return label
    

    def update_timer(self):
        self.remaining_time = self.remaining_time.addSecs(-1)  # Decrement the time by 1 second
        self.update_label()
        
        if self.remaining_time == QTime(0, 0):  # Timer has reached 0
            self.timer.stop()
            pygame.mixer.music.stop()
            QSound.play('data/alarm.wav')

    def update_label(self):
        self.label.setText(self.remaining_time.toString("hh:mm:ss"))











