# -*- coding: cp1252 -*-
#extract POS tags from parsed Spanish
#the POS is the first token after the word that isnt in square or <> brackets
#the next few (if noun or verb give tense, gender, number etc)
PAR = open("Spanish_parsed.txt", "r")
par = PAR.read()
PAR.close()

OUT = open("spanish-processed.txt", "w")
OUT.close()

prevpos = ""
prevgen = ""
prevnum = ""
prevword = ""
flipped = 0
for line in par.split("\n")[3:-1]:
    #print(line)
    tok = line.split()
    #print(tok)
    currword = tok[0]
    idx = 1
    if line != "." and line != "," and line != "?" and line != "¿":
        for t in tok[1:]:
            idx = idx+1
            if t[0] != "<" and t[0] != "[":
                #print(t)
                POS = t
                break
        if POS == "ADJ" or POS == "N":
            gen = tok[idx]
            num = tok[idx+1]

            #print(gen, num)
        if POS == "N":
            print("Currently noun, skip ", currword)
        else:
            if prevpos == "N":
                if POS == "ADJ":
                    #noun followed by an adjective
                    if (gen == prevgen or gen == "MF" or prevgen == "MF")and prevnum == num: #agrees in gender and number
                        #print(line)
                        #print("Order needs to be flipped")
                        OUT = open("spanish-processed.txt", "a")
                        OUT.write(currword+" "+prevword+" ")
                        flipped = 1
                        #print("writing", currword, prevword)
                        OUT.close()
                    else:
                    #non agreeing adj and noun, possible?
                        #print("no flipping because they dont agree")
                        OUT = open("spanish-processed.txt", "a")
                        #print("writing", prevword, currword)
                        OUT.write(prevword+" "+currword+" ")
                        OUT.close()
                        flipped = 0
                else:
                #noun not followed by an adjective, just print the noun and current word
                    #print("curr word follows a noun but is not an adjective")
                    OUT = open("spanish-processed.txt", "a")
                    #print("writing", prevword, currword)
                    OUT.write(prevword+" "+currword+" ")
                    OUT.close()
                    flipped = 0
            else:
                    #current word does not follow a noun and is not a noun, just print it
                    OUT = open("spanish-processed.txt", "a")
                    OUT.write(currword+" ")
                    OUT.close()
                    flipped = 0
        if POS == "ADJ" or POS == "N":
            prevgen = gen
            prevnum = num
        prevword = currword
        prevpos = POS
        
    else:
         OUT = open("spanish-processed.txt", "a")
         if flipped == 0:
             OUT.write(prevword+" .\n")
         else:
             OUT.write(" .\n")
         OUT.close()
         prevword = ""
         prevpos = ""
         prevgen = ""
         prevnum = ""
