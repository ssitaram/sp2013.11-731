#convert corpus into integer representation
#replace all strings with integer
#treat upper and lowercase as same
INPSRC = open("data/de.txt", "r")
OUTSRC = open("data/de-num.txt", "w")
OUTSRC.close()
INPTGT = open("data/en.txt", "r")
OUTTGT = open("data/en-num.txt", "w")
OUTTGT.close()
inpsrc = INPSRC.read()
inptgt = INPTGT.read()
INPSRC.close()
INPTGT.close()
srcdict = {}
tgtdict = {}
srcidx = 0
tgtidx = 0
finished = 0
for line in inpsrc.split("\n"):
    finished += 1
    if finished%1000 == 0:
        print("finished dict src "+str(finished))
    words = line.split(" ")
    for word in words:
        word = word.lower()
        if word not in srcdict.keys():
            srcdict[word] = srcidx
            srcidx += 1
finished = 0 
for line in inpsrc.split("\n"):
    finished += 1
    if finished%1000 == 0:
        print("finished writing src "+str(finished))
    words = line.split(" ")
    outsent = ""
    for word in words:
        word = word.lower()
        outsent = outsent + str(srcdict[word])
    OUTSRC = open("data/de-num.txt", "a")
    OUTSRC.write(outsent+"\n")
    OUTSRC.close()

finished = 0         
for line in inptgt.split("\n"):
    finished += 1
    if finished%1000 == 0:
        print("finished dict tgt "+str(finished))
    words = line.split(" ")
    for word in words:
        word = word.lower()
        if word not in tgtdict.keys():
            tgtdict[word] = tgtidx
            tgtidx += 1
finished = 0 
for line in inptgt.split("\n"):
    finished += 1
    if finished%1000 == 0:
        print("finished writing tgt "+str(finished))
    words = line.split(" ")
    outsent = ""
    for word in words:
        word = word.lower()
        outsent = outsent + str(tgtdict[word])
    OUTSRC = open("data/en-num.txt", "a")
    OUTSRC.write(outsent+"\n")
    OUTSRC.close()

