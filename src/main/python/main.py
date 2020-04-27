import sys

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColorConstants
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget


class TimerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(TimerWidget())
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.resize(150, 90)
        self.move(10, 10)


class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.minutesLabel = QLabel("Minutes:")
        self.minutesLineEdit = QLineEdit()
        self.startButton = QPushButton("Start")
        self.startButton.setFixedSize(50, 23)
        self.startButton.clicked.connect(self._start_event)
        self.resetButton = QPushButton("Reset")
        self.resetButton.setFixedSize(50, 23)
        self.resetButton.clicked.connect(self._reset_event)
        self.displayArea = QTextEdit()
        self.displayArea.setTextColor(QColorConstants.DarkBlue)
        self.displayArea.setStyleSheet("border: none")
        self.displayArea.setFontPointSize(36)
        self.displayArea.setReadOnly(True)
        self.showTimeLeft("00:00:00")
        self.setWidgets()

    def _start_event(self):
        if self.startButton.text() == "Start":
            self.startButton.setText("Pause")
        else:
            self.startButton.setText("Start")

    def _reset_event(self):
        self.startButton.setText("Start")
        self.showTimeLeft("00:00:00")

    def showTimeLeft(self, timeStr):
        self.displayArea.setText(timeStr)
        self.displayArea.setAlignment(Qt.AlignHCenter)

    def setWidgets(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.minutesLabel)
        hbox.addWidget(self.minutesLineEdit)
        hbox.addWidget(self.startButton)
        hbox.addWidget(self.resetButton)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.displayArea)

        self.setLayout(vbox)


if __name__ == '__main__':
    appctxt = ApplicationContext()
    window = TimerWindow()
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
