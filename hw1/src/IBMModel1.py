import sys
import os
from nltk import FreqDist as FDist
from nltk import ConditionalFreqDist as CondFDist

def init_prob_unit():
    #initialize uniform prob distribution to t(e|f)
    print("Initializing Uniform Prob distribution")
    N = len(de_inp)
    if N != len(en_inp):
        print("number of lines in src and target don't match!")
    ten_de = CondFDist()
    for num in range(N):
        for de_word in de_inp[num].split():
            for en_word in en_inp[num].split():
                ten_de[de_word].inc(en_word)
    #make probs uniform
    for de_word in ten_de.conditions():
        for key in ten_de[de_word].keys():
            ten_de[de_word][key] = 1.0/len(ten_de[de_word])
            #print(ten_de[de_word][key])
    return ten_de


def run_EM(no_of_iter, ten_de):
    #Run EM for specified number of iterations
    print("Running EM")
    ## pseudocode from http://www.statmt.org/mtm2/data/day2-1x2.pdf
    ##    do until convergence
    ##    set count(e|f) to 0 for all e,f
    ##    set total(f) to 0 for all f
    ##    for all sentence pairs (e_s,f_s)
    ##    for all words e in e_s
    ##    total_s(e) = 0
    ##    for all words f in f_s
    ##    total_s(e) += t(e|f)
    ##    for all words e in e_s
    ##    for all words f in f_s
    ##    count(e|f) += t(e|f) / total_s(e)
    ##    total(f) += t(e|f) / total_s(e)
    ##    for all f
    ##    for all e
    ##    t(e|f) = count(e|f) / total(f)
    #print(ten_de)
    N = len(de_inp)
    for i in range(no_of_iter):
        print("Doing iteration "+str(i))
        totalde = FDist()
        counten_de = CondFDist()
        for sent in range(N):
            total_s = FDist()
            for en_word in en_inp[sent].split():
                for de_word in de_inp[sent].split():
                    total_s.inc(en_word, ten_de[de_word][en_word])
##                    print(en_word)
##                    print(de_word)
##                    print(total_s[en_word])
            for en_word in en_inp[sent].split():
                for de_word in de_inp[sent].split():
                    counten_de[de_word].inc(en_word, ten_de[de_word][en_word]/total_s[en_word])
                    totalde.inc(de_word, ten_de[de_word][en_word]/total_s[en_word])
        for de_word in ten_de.conditions():
            for en_word in ten_de[de_word].keys():
                ten_de[de_word][en_word] = counten_de[de_word][en_word]/totalde[de_word]
    return ten_de
    
#target language EN
ENINP = open("../data/en.txt", "r")
en_inp = ENINP.readlines()[:35000]
ENINP.close()

#source language DE
DEINP = open("../data/de.txt", "r")
de_inp = DEINP.readlines()[:35000]
DEINP.close()

ten_de_init = init_prob_unit()
ten_de_final = run_EM(5, ten_de_init)

OUT = open("trans_prob_table.txt", "w")
OUT.close()
for de_word in ten_de_final.conditions():
    for en_word in ten_de_final[de_word]:
        OUT = open("trans_prob_table.txt", "a")
        ###source word - target word - probability####
        OUT.write(de_word+"\t"+en_word+"\t"+str(ten_de_final[de_word][en_word])+"\n")
        OUT.close()
