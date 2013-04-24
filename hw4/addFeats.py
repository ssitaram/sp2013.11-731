# -*- coding: utf-8 -*-
#calculate features
#number of target words
#and number of untranslated russian words (no of russian words in output)


### also make a training file out of dev sentences for logistic regression
import re
INP = open("data/dev.100best", "r")
inp = INP.read()
INP.close()

REF = open("data/dev.ref", "r")
ref = REF.read()
REF.close()

OUT = open("data/devnew.100best", "w")
OUT.close()
count = 0
ru = list('ёъяшертыуиопющэасдфгчйкльжзхцвбнмЁЪЯШЕРТЫУИОПЮЩЭАСДФГЧЙКЛЬЖЗХЦВБНМ')
for line in inp.split("\n"):
    target = line.split("|||")[1]
    #print(target)
    numwords = len(target.split())
    rucount = 0.0
    for word in target.split():
        for w in word:
            if w in ru:
                #print(word)
                rucount = rucount + 1
                break
    idx = count//100
    #print(idx)
##    for r in ref.split("\n")[idx]:
##        if r == line:
##            ex = 1
##        else:
##            ex = -1
    OUT = open("data/devnew.100best", "a")
    OUT.write(line+" numtgt="+str(numwords)+" numru="+str(rucount/numwords)+"\n")
    OUT.close()
    count = count + 1

