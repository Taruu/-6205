#! /usr/bin/python3
import sys
from PyQt5 import QtGui,uic,QtCore
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QUrl
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import sys
import driver.driver


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)
        met = QtGui.QFontMetrics(QtGui.QFont())
        width = met.width(str("                "))


        self.loopTimer = QtCore.QTimer()
        self.loopTimer.timeout.connect(self.updateScreens)
        #Экраны
        self.screenOne = self.findChild(QtWidgets.QTextEdit,"TextEditScreen_1")
        self.screenTwo = self.findChild(QtWidgets.QTextEdit,"TextEditScreen_2")
        self.screenThree = self.findChild(QtWidgets.QTextEdit,"TextEditScreen_3")
        self.screenFour = self.findChild(QtWidgets.QTextEdit,"TextEditScreen_4")
        #выбор экрана
        self.radioButtonOne = self.findChild(QtWidgets.QRadioButton,"radioButtonTake_1")
        self.radioButtonTwo = self.findChild(QtWidgets.QRadioButton,"radioButtonTake_2")
        self.radioButtonThree = self.findChild(QtWidgets.QRadioButton,"radioButtonTake_3")
        self.radioButtonFour = self.findChild(QtWidgets.QRadioButton,"radioButtonTake_4")

        #Кнопки
        self.UpdateButton = self.findChild(QtWidgets.QPushButton,"updateButton")
        self.ClearAll = self.findChild(QtWidgets.QPushButton,"ClearAll")

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



        self.NowScreen = 1
        self.AutoMode = False
        self.nowkey = None

        self.show()
        self.StatusLabel.setText("Подключение к serial")
        self.driver = driver.driver.MC6205()
        print(self.driver)
        self.StatusLabel.setText("Ждем команд")
        with open("driver/filesScreen/screen1","r") as file:
            self.screenOne.setText(file.read())
        with open("driver/filesScreen/screen2","r") as file:
            self.screenTwo.setText(file.read())
        with open("driver/filesScreen/screen3","r") as file:
            self.screenThree.setText(file.read())
        with open("driver/filesScreen/screen4","r") as file:
            self.screenFour.setText(file.read())


    def clearScreen(self):
        button = self.sender()
        clearScreenNumber = int(button.objectName().split("_")[-1])
        if clearScreenNumber == 1:
            self.screenOne.setText("")
        elif clearScreenNumber == 2:
            self.screenTwo.setText("")
        elif clearScreenNumber == 3:
            self.screenThree.setText("")
        elif clearScreenNumber == 4:
            self.screenFour.setText("")
        if not(self.AutoMode):
            with open("driver/filesScreen/nowscreen", "w") as file:
                file.write(clearScreenNumber)
            self.driver.clearScreen()

    def screenTake(self):
        screenRadiobutton = self.sender()
        if screenRadiobutton.isChecked():
            self.NowScreen = screenRadiobutton.text().split()[-1]
        if not (self.AutoMode):
            with open("driver/filesScreen/nowscreen", "w") as file:
                file.write(self.NowScreen)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        self.nowkey = event.key()

    def screenNowEdit(self):
        screen = self.sender()
        list_lines = screen.toPlainText().splitlines()
        try:
            charNow = chr(self.nowkey)
        except:
            charNow = False
        if len(list_lines) > 10:
            screen.undo()
            return
        if (screen.textCursor().columnNumber() >= 16) and self.nowkey!=Qt.Key_Backspace:
            screen.append("")
        elif not(charNow in self.driver.dictionaryLetter) and self.nowkey!=Qt.Key_Backspace:
            screen.undo()


    def updateScreens(self):
        self.driver.update_monitor()
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
