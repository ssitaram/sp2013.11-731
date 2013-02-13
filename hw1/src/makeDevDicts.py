#make dictionary out of dev set alignments and use them in alignment step after running IBM model 1
#make sure dict and maybedict
#creating a dict from de-en
#dict structure is target word : list of source words it aligns to with the counts of each word


DEV = open("../data/dev.align", "r")
dev = DEV.read()
DEV.close()

DESENTS = open("../data/de.txt", "r")
desents = DESENTS.read()
DESENTS.close()

ENSENTS = open("../data/en.txt", "r")
ensents = ENSENTS.read()
ENSENTS.close()

SUREDICT = open("sure.dict", "w")
SUREDICT.close()
MAYBEDICT = open("maybe.dict", "w")
MAYBEDICT.close()

suredict = {}
maybedict = {}

for line, de, en in zip(dev.split("\n"), desents.split("\n")[:150], ensents.split("\n")[:150]):
    #remember that dev is only top few of de and en sents 
    alignments = line.split(" ")
    dewords = de.split(" ")[:-1]
    enwords = en.split(" ")[1:] ##because of weird format of de and en files which i should have fixed
    #print(dewords)
    #print(enwords)
    for pair in alignments:
        if pair.find("-") != -1:
            #print("Sure alignments")
            srcidx = pair[:pair.find("-")]
            tgtidx = pair[pair.find("-")+1:]
            #print(srcidx)
            #print(tgtidx)
            srcword = dewords[eval(srcidx)].lower()
            tgtword = enwords[eval(tgtidx)].lower()
            #print(srcword+"-"+tgtword)
            #some messy dictionary stuff
            #initialize value to 1 if not present in dictionary
            if tgtword not in suredict.keys():
                suredict[tgtword] = {}
            else:
                if srcword not in suredict[tgtword].keys():
                    
                    #suredict[tgtword] = suredict.get(tgtword, {})
                    suredict[tgtword][srcword] = 1
                else:
                    #increment value by 1
                    #print("incrementing!")
                    suredict[tgtword][srcword] = suredict[tgtword][srcword] + 1

            
        else:
            if pair.find("?") != -1:
                #print("Maybe alignments")
                srcidx = pair[:pair.find("?")]
                tgtidx = pair[pair.find("?")+1:]
                #print(srcidx)
                #print(tgtidx)
                srcword = dewords[eval(srcidx)].lower()
                tgtword = enwords[eval(tgtidx)].lower()
                #print(srcword+"?"+tgtword)
                if tgtword not in maybedict.keys():
                    maybedict[tgtword] = {}
                else:
                    if srcword not in maybedict[tgtword].keys():
                    
                    #suredict[tgtword] = suredict.get(tgtword, {})
                        maybedict[tgtword][srcword] = 1
                    else:
                    #increment value by 1
                        maybedict[tgtword][srcword] = maybedict[tgtword][srcword] + 1
                    
            else:
                print("Something wrong, not sure or maybe")

                
for tgtword in suredict.keys():
    SUREDICT = open("sure.dict", "a")
    if suredict[tgtword] != {}:
        SUREDICT.write(tgtword+" : ")
        for srcword in suredict[tgtword].keys():
            SUREDICT.write(srcword+" "+str(suredict[tgtword][srcword])+" ")
            #print(suredict[tgtword][srcword])
        SUREDICT.write("\n")
    SUREDICT.close()
    
#lots of redundant code, clean up if have time

for tgtword in maybedict.keys():
    MAYBEDICT = open("maybe.dict", "a")
    if maybedict[tgtword] != {}:
        MAYBEDICT.write(tgtword+" : ")
        for srcword in maybedict[tgtword].keys():
            MAYBEDICT.write(srcword+" "+str(maybedict[tgtword][srcword])+" ")
            #print(suredict[tgtword][srcword])
        MAYBEDICT.write("\n")
    MAYBEDICT.close()
#print(suredict)
#print(maybedict)
