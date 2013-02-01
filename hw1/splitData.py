#split data into en and fr files
INP = open("data/dev-test-train.de-en", "r")
inp = INP.read()
INP.close()
OUTDE = open("data/de.txt", "w")
OUTEN = open("data/en.txt", "w")
OUTDE.close()
OUTEN.close()

for line in inp.split("\n")[:-1]:
    de = line.split("|||")[0]
    en = line.split("|||")[1]
    #print(de)
    #print(en)
    OUTDE = open("data/de.txt", "a")
    OUTEN = open("data/en.txt", "a")
    OUTDE.write(de+"\n")
    OUTEN.write(en+"\n")
    OUTDE.close()
    OUTEN.close()
