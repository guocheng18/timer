import enum
import sys

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QColorConstants
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QSpinBox, QTextEdit, QVBoxLayout, QWidget


class TimerStatus(enum.Enum):
    init, counting, paused = 1, 2, 3


class ButtonText:
    start, pause, reset = "Start", "Pause", "Reset"


class TimerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.minutesLabel = QLabel("Minutes:")
        self.minutesSpinBox = QSpinBox()
        self.minutesSpinBox.setFixedSize(60, 23)
        self.minutesSpinBox.setRange(0, 10**9)
        self.minutesSpinBox.setSingleStep(5)
        self.minutesSpinBox.setFocus()
        self.minutesSpinBox.selectAll()
        self.minutesSpinBox.valueChanged.connect(self._edit_event)
        self.startButton = QPushButton(ButtonText.start)
        self.startButton.setFixedSize(50, 23)
        self.startButton.clicked.connect(self._start_event)
        self.resetButton = QPushButton(ButtonText.reset)
        self.resetButton.setFixedSize(50, 23)
        self.resetButton.clicked.connect(self._reset_event)
        self.displayArea = QTextEdit()
        self.displayArea.setTextColor(QColorConstants.DarkBlue)
        self.displayArea.setStyleSheet("border: none")
        self.displayArea.setFontFamily("Arial")
        self.displayArea.setFontPointSize(38)
        self.displayArea.setTextInteractionFlags(Qt.NoTextInteraction)
        self.displayArea.viewport().setCursor(Qt.ArrowCursor)
        self.displayArea.viewport().installEventFilter(self)
        self.setWidgets()
        self._status = TimerStatus.init
        self._left_seconds = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._countdown_and_show)
        self.showTime()

    def eventFilter(self, obj, event):
        if obj is self.displayArea.viewport() and event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.minutesSpinBox.setFocus()
                self.minutesSpinBox.selectAll()
        return super(TimerWidget, self).eventFilter(obj, event)

    def _countdown_and_show(self):
        if self._left_seconds > 0:
            self._left_seconds -= 1
            self.showTime()
        else:
            self.timer.stop()
            self.showTime()
            self.startButton.setText(ButtonText.start)
            self._status = TimerStatus.init
            self._left_seconds = self.minutesSpinBox.value() * 60

    def _start_event(self):
        if (self._status == TimerStatus.init or self._status == TimerStatus.paused) and self._left_seconds > 0:
            self._left_seconds -= 1
            self._status = TimerStatus.counting
            self.showTime()
            self.timer.start(1000)
            self.startButton.setText(ButtonText.pause)
        elif self._status == TimerStatus.counting:
            self.timer.stop()
            self._status = TimerStatus.paused
            self.startButton.setText(ButtonText.start)

    def _reset_event(self):
        self._status = TimerStatus.init
        self._left_seconds = self.minutesSpinBox.value() * 60
        self.startButton.setText(ButtonText.start)
        self.timer.stop()
        self.showTime()

    def _edit_event(self):
        if self._status == TimerStatus.init:
            self._left_seconds = self.minutesSpinBox.value() * 60
            self.showTime()

    def showTime(self):
        total_seconds = min(self._left_seconds, 359940)  # Max time: 99:59:00
        hours = total_seconds // 3600
        total_seconds = total_seconds - (hours * 3600)
        minutes = total_seconds // 60
        seconds = total_seconds - (minutes * 60)
        self.displayArea.setText("{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)))
        self.displayArea.setAlignment(Qt.AlignHCenter)

    def setWidgets(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.minutesLabel)
        hbox.addWidget(self.minutesSpinBox)
        hbox.addWidget(self.startButton)
        hbox.addWidget(self.resetButton)
        hbox.setAlignment(Qt.AlignLeft)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.displayArea)
        self.setLayout(vbox)


class TimerWindow(QMainWindow):
    def __init__(self, x=10, y=10, width=150, height=90):
        super().__init__()
        self.widget = TimerWidget(self)
        self.setCentralWidget(self.widget)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.resize(width, height)
        self.move(x, y)


if __name__ == '__main__':
    appctxt = ApplicationContext()
    window = TimerWindow()
    window.show()
    sys.exit(appctxt.app.exec_())
