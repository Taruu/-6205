import copy
matrixScreen = [[80 for col in range(16)] for row in range(10)]
dictionaryLetter = list("█ПЯРСТУЖВЬЫЗШЭЩЧЮАБЦДЕФГХИЙКЛМНОР"+"QRSTUVWXYZ[⌄]^-$ABCDEFGHIJKLMNO" +'0123456789:;<=>? !"#§%&'+"'()*+,_./")


def PA(args): #функция отрисовки матрицы на экран
    if not args:
        return None
    result = ""
    result += "\t" + "\t".join([str(x) for x in range(len(args[0]))]) + "\n" + "\n"
    for i in range(len(args)):
        add = [str(x) for x in args[i]]
        result += str(i) + "\t" + "\t".join(add) + "\n"
    return result


def strToCodeList(word:str):
    """Convert character to post byte code"""
    listnumBytes = []
    for letter in word.upper():
        if letter in dictionaryLetter:
            listnumBytes.append(dictionaryLetter.index(letter))
        else:
            listnumBytes.append(0)
    if len(listnumBytes) == 1:
        return listnumBytes[0]
    else:
        return listnumBytes




print(PA(matrixScreen))

oldMatrixScreen = copy.deepcopy(matrixScreen)

matrixScreen[0][0] = 1
matrixScreen[0][5] = 1
matrixScreen[1][1] = 1
matrixScreen[1][2] = 2
matrixScreen[1][3] = 3
matrixScreen[1][4] = 4
print(PA(matrixScreen))

print(comparisonMatrix(oldMatrixScreen, matrixScreen))

