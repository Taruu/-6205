#! /usr/bin/python3
import sys
from PyQt5 import QtGui,uic,QtCore
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QUrl
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt,QThread
import sys
import driver.driver
import time

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)
        met = QtGui.QFontMetrics(QtGui.QFont())


        self.loopTimer = QtCore.QTimer()
        self.loopTimer.timeout.connect(self.updateScreens)
        #Экраны
        self.screenOne = self.findChild(QtWidgets.QTextEdit,"TextEditScreen_1")
        self.screenTwo = self.findChild(QtWidgets.QTextEdit,"TextEditScreen_2")
        self.screenThree = self.findChild(QtWidgets.QTextEdit,"TextEditScreen_3")
        self.screenFour = self.findChild(QtWidgets.QTextEdit,"TextEditScreen_4")
        #таймер
        self.SecondsAutoUpdateLine = self.findChild(QtWidgets.QLineEdit,"SecondsAutoUpdate")
        #выбор экрана
        self.radioButtonOne = self.findChild(QtWidgets.QRadioButton,"radioButtonTake_1")
        self.radioButtonTwo = self.findChild(QtWidgets.QRadioButton,"radioButtonTake_2")
        self.radioButtonThree = self.findChild(QtWidgets.QRadioButton,"radioButtonTake_3")
        self.radioButtonFour = self.findChild(QtWidgets.QRadioButton,"radioButtonTake_4")

        #Кнопки
        self.UpdateButton = self.findChild(QtWidgets.QPushButton,"updateButton")
        self.ClearAll = self.findChild(QtWidgets.QPushButton,"ClearAll")

        self.AutoUpdate = self.findChild(QtWidgets.QCheckBox,"AutoUpdate")

        #Кнопки очистка
        self.ClearScreenOne = self.findChild(QtWidgets.QPushButton, "ClearScreen_1")
        self.ClearScreenTwo = self.findChild(QtWidgets.QPushButton, "ClearScreen_2")
        self.ClearScreenThree = self.findChild(QtWidgets.QPushButton, "ClearScreen_3")
        self.ClearScreenFour = self.findChild(QtWidgets.QPushButton, "ClearScreen_4")

        self.StatusLabel = self.findChild(QtWidgets.QLabel,"StatusLabel")
        #textedit
        self.screenOne.cursorPositionChanged.connect(self.screenNowEdit)
        self.screenTwo.cursorPositionChanged.connect(self.screenNowEdit)
        self.screenThree.cursorPositionChanged.connect(self.screenNowEdit)
        self.screenFour.cursorPositionChanged.connect(self.screenNowEdit)
        #radioButtons
        self.radioButtonOne.toggled.connect(self.screenTake)
        self.radioButtonTwo.toggled.connect(self.screenTake)
        self.radioButtonThree.toggled.connect(self.screenTake)
        self.radioButtonFour.toggled.connect(self.screenTake)
        #Кнопки очистки
        self.ClearScreenOne.clicked.connect(self.clearScreen)
        self.ClearScreenTwo.clicked.connect(self.clearScreen)
        self.ClearScreenThree.clicked.connect(self.clearScreen)
        self.ClearScreenFour.clicked.connect(self.clearScreen)

        self.UpdateButton.clicked.connect(self.updateScreens)

        self.AutoUpdate.stateChanged.connect(self.statusAutoMode)
        self.ClearAll.clicked.connect(self.ClearAllScreens)

        self.SecondsAutoUpdateLine.textChanged.connect(self.updateDelay)
        self.NowScreen = 1
        self.AutoMode = False
        self.nowkey = None
        self.timerSleep = 1
        self.show()
        self.StatusLabel.setText("Connected to serial")
        self.driver = None
        with open("driver/filesScreen/screen1","r") as file:
            self.screenOne.setText(file.read())
        with open("driver/filesScreen/screen2","r") as file:
            self.screenTwo.setText(file.read())
        with open("driver/filesScreen/screen3","r") as file:
            self.screenThree.setText(file.read())
        with open("driver/filesScreen/screen4","r") as file:
            self.screenFour.setText(file.read())
        with open("driver/filesScreen/nowscreen","w") as file:
            file.write(str(self.NowScreen))
        self.driver =driver.driver.MC6205()
        self.thread = Worker(MainWindow=self)
        self.StatusLabel.setText("Wait comands")

    def updateDelay(self):
        if not(self.SecondsAutoUpdateLine.text().isdigit()):
            self.SecondsAutoUpdateLine.undo()
        else:
            self.timerSleep = int(self.SecondsAutoUpdateLine.text())

    def statusAutoMode(self,state):
        if state == 2:
            self.thread.start()
            self.AutoMode = True
        else:
            self.AutoMode = False
            self.thread.stop()

    def ClearAllScreens(self):
        self.screenOne.setText("")
        self.screenTwo.setText("")
        self.screenThree.setText("")
        self.screenFour.setText("")
        self.StatusLabel.setText("Clear All Screen")
        if not(self.AutoMode):
            self.updateScreens()

    def clearScreen(self):
        button = self.sender()
        clearScreenNumber = int(button.objectName().split("_")[-1])
        self.StatusLabel.setText(f"Clear screen {clearScreenNumber}")
        if clearScreenNumber == 1:
            self.screenOne.clear()
        elif clearScreenNumber == 2:
            self.screenTwo.clear()
        elif clearScreenNumber == 3:
            self.screenThree.clear()
        elif clearScreenNumber == 4:
            self.screenFour.clear()
        if not (self.AutoMode):
            self.updateScreens()


    def screenTake(self):
        screenRadiobutton = self.sender()
        if screenRadiobutton.isChecked():
            self.NowScreen = screenRadiobutton.text().split()[-1]
        if not (self.AutoMode):
            self.updateScreens()

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        self.nowkey = event.key()

    def screenNowEdit(self):
        screen = self.sender()
        list_lines = screen.toPlainText().splitlines()
        if len(list_lines) > 10:
            screen.undo()
            return
        if (screen.textCursor().columnNumber() >= 16) and self.nowkey!=Qt.Key_Backspace:
            screen.append("")
        self.StatusLabel.setText(f"Edit screen {screen.objectName().split('_')[1]}")

    #todo cloack demo
    def updateScreens(self):
        print("Updating screens")
        self.StatusLabel.setText(f"Update screen {self.NowScreen}")
        with open("driver/filesScreen/nowscreen", "w") as file:
            file.write(str(self.NowScreen))
        with open("driver/filesScreen/screen1","w") as file:
            file.write(self.screenOne.toPlainText())
        with open("driver/filesScreen/screen2","w") as file:
            file.write(self.screenTwo.toPlainText())
        with open("driver/filesScreen/screen3","w") as file:
            file.write(self.screenThree.toPlainText())
        with open("driver/filesScreen/screen4","w") as file:
            file.write(self.screenFour.toPlainText())
        self.driver.update_monitor()
        self.StatusLabel.setText(f"Wait comands")



class Worker(QThread):
    def __init__(self, MainWindow,parent = None):
        super().__init__()
        self.mainwindow = MainWindow
        print(self.mainwindow.updateScreens)

    def run(self):
        while True:
            time.sleep(self.mainwindow.timerSleep)
            print("loop work")
            self.mainwindow.updateScreens()

    def stop(self):
        self.terminate()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
