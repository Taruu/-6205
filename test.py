with open("number.txt") as file:
    all = file.readlines()

all = [line.replace("\n","") for line in all]

ListAll = []
for line in all:
    ListAll.append(line.split("|"))
    print(line.split("|"))
print(ListAll)
def numericString(one, two, three, four):
    resultstring = ""
    for i in range(5):
        if i == 1 or i == 3:
            resultstring += ListAll[i][one] + " " + ListAll[i][two] + " . " + ListAll[i][three] + " " + ListAll[i][four] + "\n"
        else:
            resultstring += ListAll[i][one] + " " + ListAll[i][two] + "   " + ListAll[i][three] + " " + ListAll[i][four] + "\n"
    else:
        return resultstring


print(numericString(1,7,3,8))