# -*- coding: cp1252 -*-
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
import nltk

def word_matches(h, ref):
    return(len(h & ref))
    
def precision(h, ref):
    #num matches/len hyp
    num_matches = word_matches(h, ref)
    return 1.0*num_matches/len(h)

def recall(h, ref):
    #num matches/len ref
    num_matches = word_matches(h, ref)
    return 1.0*num_matches/len(ref)

def meteor(h_precision, h_recall):
    #precision*recall/(1-alpha)*p+alpha*r
    if h_precision == 0 and h_recall == 0:
        return 0
    return 1.0* (10*h_precision*h_recall)/(9*h_precision+h_recall)

def process(sent):
    #removing punctuation and making everything lowercase
    sentnew = []
    punc = [".", ",", "(", ")", ":", ";", "?", "!", "\"", "'", "&quot;", "-"]
    for word in sent:
        word = word.lower()
        word = word.replace("é", "e")
        for p in punc:
            word = word.replace(p, "")    
        sentnew.append(word)
    return sentnew
                            
def main():

    OUT = open("../output.txt", "w")
    OUT.close()
    INP = open("../data/test.hyp1-hyp2-ref", "r")
    inp = INP.read()
    lmtzr = WordNetLemmatizer()
    for sent in inp.split("\n")[:-1]:
        h1 = sent.split(" ||| ")[0].split(" ")
        h2 = sent.split(" ||| ")[1].split(" ")
        ref = sent.split(" ||| ")[2].split(" ")
        #word stemming
        h1new = []
        h2new = []
        refnew = []
        for w in h1:
            wnew = lmtzr.lemmatize(w)
            h1new.append(wnew)
        h1 = h1new
        for w in h2:
            wnew = lmtzr.lemmatize(w)
            h2new.append(wnew)
        h2 = h2new
        for w in ref:
            wnew = lmtzr.lemmatize(w)
            refnew.append(wnew)
        ref = refnew
        #end word stemming
        h1p = process(h1)
        h2p = process(h2)
        refp = process(ref)
        #print(h1c, h2c, refc)
        #h1_match = word_matches(h1, rset)
        #h2_match = word_matches(h2, rset)
        h1c = Counter(h1p)
        h2c = Counter(h2p)
        refc = Counter(refp)
        h1_bigrams = nltk.bigrams(h1p)
        h2_bigrams = nltk.bigrams(h2p)
        ref_bigrams = nltk.bigrams(refp)
        h1_trigrams = nltk.trigrams(h1p)
        h2_trigrams = nltk.trigrams(h2p)
        ref_trigrams = nltk.trigrams(refp)
        #print(h_bigrams, ref_bigrams)
        h1_bigramsc = Counter(h1_bigrams)
        h2_bigramsc = Counter(h2_bigrams)
        ref_bigramsc = Counter(ref_bigrams)
        h1_trigramsc = Counter(h1_trigrams)
        h2_trigramsc = Counter(h2_trigrams)
        ref_trigramsc = Counter(ref_trigrams)
        h1_allc = h1c + h1_bigramsc + h1_trigramsc
        h2_allc = h2c + h2_bigramsc + h2_trigramsc
        ref_allc = refc + ref_bigramsc + ref_trigramsc
        h1_precision = precision(h1_allc, ref_allc)
        h2_precision = precision(h2_allc, ref_allc)
        h1_recall = recall(h1_allc, ref_allc)
        h2_recall = recall(h2_allc, ref_allc)
        h1_meteor = meteor(h1_precision, h1_recall)
        h2_meteor = meteor(h2_precision, h2_recall)
        OUT = open("../output.txt", "a")

        if h1_meteor > h2_meteor:
            OUT.write("-1\n")
        else:
            if h1_meteor == h2_meteor:
                OUT.write("0\n")
            else:
                OUT.write("1\n")
        OUT.close()
 
# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
