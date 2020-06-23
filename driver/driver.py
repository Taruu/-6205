import serial
import time
import copy
import os




def PA(args): #функция отрисовки матрицы на экран
    if not args:
        return None
    result = ""
    result += "\t" + "\t".join([str(x) for x in range(len(args[0]))]) + "\n" + "\n"
    for i in range(len(args)):
        add = [str(x) for x in args[i]]
        result += str(i) + "\t" + "\t".join(add) + "\n"
    return result

class MC6205:
    def __init__(self):
        self.dictionaryLetter = list(
            "█ПЯРСТУЖВЬЫЗШЭЩЧЮАБЦДЕФГХИЙКЛМНО" + "PQRSTUVWXYZ[⌄]^-$ABCDEFGHIJKLMNO" + '0123456789:;<=>? !"#§%&' + "'()*+,_./")
        self.matrixScreen = [[80 for col in range(16)] for row in range(10)]
        self.matrixScreenOld1 = [[80 for col in range(16)] for row in range(10)]
        self.matrixScreenOld2 = [[80 for col in range(16)] for row in range(10)]
        self.matrixScreenOld3 = [[80 for col in range(16)] for row in range(10)]
        self.matrixScreenOld4 = [[80 for col in range(16)] for row in range(10)]
        self.AllMatrixArray = []
        self.allScreenOld = [self.matrixScreenOld1, self.matrixScreenOld2, self.matrixScreenOld3, self.matrixScreenOld4]
        self.ser = serial.Serial("/dev/ttyACM0")
        self.ser.baudrate = 115200
        self.ser.timeout = 40
        self.nowScreen = 1
        if not self.ser.is_open:
            self.ser.open()
        time.sleep(1)
        res = ""
        while True:
            try:
                res = self.ser.readline()
                print(res)
                if res.decode()[0] == "r":
                    break
            except:
                pass
        self.clearAllScreens()
        time.sleep(1)
        self.takeScreen(1)
        time.sleep(1)
        self.startPos()

    # TODO class Screen
    def strToCodeList(self,word: str):
        """Convert character to post byte code"""
        listnumBytes = []
        for letter in word.upper():
            if letter in self.dictionaryLetter:
                listnumBytes.append(self.dictionaryLetter.index(letter))
            else:
                listnumBytes.append(0)
        if len(listnumBytes) == 1:
            return listnumBytes[0]
        else:
            return listnumBytes

    def comparisonMatrix(self,oldMatrixScreen, NewMatrixScreen):
        """The function accepts the old matrix and the new matrix. Gives a list of actions to fill the screen."""
        listSetSymbol = []  # setting a single character
        listSetWorld = []  # word records
        cursorCount = 0  # Cursor position
        countSpace = 0  # Number of spaces
        #TODO with space many symbols
        for row, (rowListOld, rowListNew) in enumerate(zip(oldMatrixScreen, NewMatrixScreen)):
            if rowListOld != rowListNew:
                list_edit = []
                for col, (Olditem, NewItem) in enumerate(zip(rowListOld, rowListNew)):
                    if Olditem != NewItem:
                        list_edit.append(NewItem)
                    else:
                        if len(list_edit) == 1:
                            countSpace += list_edit.count(80)
                            tempPos = cursorCount - 1
                            temp = (tempPos, list_edit[0])
                            listSetSymbol.append(temp)
                            list_edit = []
                        elif len(list_edit) > 1:
                            countSpace += list_edit.count(80)
                            tempPos = cursorCount - len(list_edit)
                            temp = (tempPos, list_edit)
                            listSetWorld.append(temp)
                            list_edit = []
                        else:
                            pass
                    cursorCount += 1
                else:
                    if len(list_edit) == 1:
                        countSpace += list_edit.count(80)
                        tempPos = cursorCount - 1
                        temp = (tempPos, list_edit[0])
                        listSetSymbol.append(temp)
                        list_edit = []
                    elif len(list_edit) > 1:
                        countSpace += list_edit.count(80)
                        tempPos = cursorCount - len(list_edit)
                        temp = (tempPos, list_edit)
                        listSetWorld.append(temp)
                        list_edit = []
                    else:
                        pass
            else:
                cursorCount += 16
        return listSetSymbol, listSetWorld, countSpace

    def clearScreen(self):
        self.ser.write(bytearray([1, 0]))
        self.ser.readline()

    def setSymbol(self,pos: int, sym):
        if issubclass(type(sym), str):
            self.ser.write(bytearray([3, 5, pos, self.strToCodeList(sym)]))
        else:
            self.ser.write(bytearray([3, 5, pos, sym]))
        self.ser.readline()
        time.sleep(0.01)

    def takeScreen(self,numberScreen):
        self.ser.write(bytearray([1, numberScreen]))
        self.ser.readline()

    def setWord(self,pos: int, intdata: list):
        tosend = [len(intdata) + 2, 6, pos]
        tosend += intdata
        self.ser.write(bytearray(tosend))
        self.ser.readline()

    def startPos(self):
        self.ser.write(bytearray([1, 7]))
        self.ser.readline()

    def clearAllScreens(self):
        for i in range(4):
            self.takeScreen(i + 1)
            self.clearScreen()
        self.takeScreen(self.nowScreen)



    def update_monitor(self):
        try:
            with open(os.getcwd()+"/driver/filesScreen/nowscreen", "r") as file:
                self.nowscreen = int(file.read(1))
                self.takeScreen(self.nowscreen)
            with open(os.getcwd()+"/driver/filesScreen/screen" + str(self.nowscreen), "r") as file:
                linesList = file.readlines()[:10]
                resultList = [line[:16].replace("\n", "").ljust(16) for line in linesList]
        except:
            return
        while len(resultList) < 10:
            resultList.append("".ljust(16))
        NowMatrix = [self.strToCodeList(line) for line in resultList]
        listSetSymbol, listSetWorld, countSpace = self.comparisonMatrix(self.allScreenOld[self.nowscreen - 1], NowMatrix)
        if countSpace > 50:
            self.clearScreen()
        for command in listSetWorld:
            self.setWord(command[0], command[1])
            time.sleep(0.02)
        for command in listSetSymbol:
            self.setSymbol(command[0], command[1])
            time.sleep(0.02)
        self.allScreenOld[self.nowscreen - 1] = copy.deepcopy(NowMatrix)




if __name__ == "__main__":
    driver = MC6205()
    while True:
        time.sleep(1)
        driver.update_monitor()

    # print(PA(matrixScreenOld))
    # print(PA(NowMatrix))

# print(ser.readline())
# print(ser.readline())





