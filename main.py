import serial
import time
import copy
dictionaryLetter = list("█ПЯРСТУЖВЬЫЗШЭЩЧЮАБЦДЕФГХИЙКЛМНОР"+"QRSTUVWXYZ[⌄]^-$ABCDEFGHIJKLMNO" +'0123456789:;<=>? !"#§%&'+"'()*+,_./")
matrixScreen = [[80 for col in range(16)] for row in range(10)]
matrixScreenOld = [[80 for col in range(16)] for row in range(10)]

def PA(args): #функция отрисовки матрицы на экран
    if not args:
        return None
    result = ""
    result += "\t" + "\t".join([str(x) for x in range(len(args[0]))]) + "\n" + "\n"
    for i in range(len(args)):
        add = [str(x) for x in args[i]]
        result += str(i) + "\t" + "\t".join(add) + "\n"
    return result


#TODO class Screen
def strToCodeList(word:str):
    """Convert character to post byte code"""
    listnumBytes = []
    print(word)
    for letter in word.upper():
        if letter in dictionaryLetter:
            listnumBytes.append(dictionaryLetter.index(letter))
        else:
            listnumBytes.append(0)
    print(listnumBytes)
    if len(listnumBytes) == 1:
        return listnumBytes[0]
    else:
        return listnumBytes


def comparisonMatrix(oldMatrixScreen,NewMatrixScreen):
    """The function accepts the old matrix and the new matrix. Gives a list of actions to fill the screen."""
    listSetSymbol = [] #setting a single character
    listSetWorld = [] #word records
    cursorCount = 0 #Cursor position
    countSpace = 0 #Number of spaces
    for row,(rowListOld,rowListNew) in enumerate(zip(oldMatrixScreen,NewMatrixScreen)):
        if rowListOld!=rowListNew:
            list_edit = []
            for col,(Olditem,NewItem) in enumerate(zip(rowListOld,rowListNew)):
                if Olditem != NewItem:
                    list_edit.append(NewItem)
                else:
                    if len(list_edit) == 1:
                        countSpace+=list_edit.count(80)
                        tempPos = cursorCount-1
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
                    tempPos = cursorCount-1
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

    return listSetSymbol,listSetWorld,countSpace

def clearScreen():
    ser.write(bytearray([1,0]))
    ser.readline()
    time.sleep(1)

def setSymbol(pos:int,sym):
    if issubclass(type(sym), str):
        ser.write(bytearray([3,5,pos,strToCodeList(sym)]))
    else:
        ser.write(bytearray([3, 5, pos, sym]))
    ser.readline()
    time.sleep(0.01)

def takeScreen(numberScreen):
    ser.write(bytearray([1, numberScreen]))
    ser.readline()

def setWord(pos:int,intdata:list):
    tosend = [len(intdata)+2, 6, pos]
    tosend+=intdata
    ser.write(bytearray(tosend))
    ser.readline()
    time.sleep(0.5)

def startPos():
    ser.write(bytearray([1,7]))
    ser.readline()
    time.sleep(1)

ser = serial.Serial("/dev/ttyACM0")
ser.baudrate = 115200
ser.timeout = 40
if not ser.is_open:
    ser.open()

time.sleep(10)
res = ""
while True:
    try:
        res = ser.readline()
        print(res)
        if res.decode()[0] == "r":
            print("ready")
            break
    except:
        pass

print("takeScreen")
time.sleep(5)
takeScreen(1)
print("clearScreen")
time.sleep(1)
clearScreen()
print("StartPos")
time.sleep(1)
startPos()
print("startLoop")



while True:
    time.sleep(2)
    try:
        with open("ScreeOne.txt", "r") as file:
            linesList = file.readlines()[:10]
            resultList = [line[:16].replace("\n", "").ljust(16) for line in linesList]
    except:
        pass
    while len(resultList) < 10:
        resultList.append("".ljust(16))
    NowMatrix = [strToCodeList(line) for line in resultList]
    print(PA(NowMatrix))
    listSetSymbol,listSetWorld,countSpace = comparisonMatrix(matrixScreenOld,NowMatrix)
    print(listSetSymbol)
    print(listSetWorld)
    if countSpace > 60:
        clearScreen()
    for command in listSetSymbol:
        setSymbol(command[0],command[1])
        #time.sleep(0.1)
    for command in listSetWorld:
        setWord(command[0],command[1])
        #time.sleep(0.1)

    matrixScreenOld = copy.deepcopy(NowMatrix)
    # print(PA(matrixScreenOld))
    # print(PA(NowMatrix))

# print(ser.readline())
# print(ser.readline())





