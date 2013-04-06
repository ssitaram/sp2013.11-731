#!/usr/bin/env python
import argparse
import sys
import models
import heapq
import numpy as np
from collections import namedtuple

parser = argparse.ArgumentParser(description='Simple phrase based decoder.')
parser.add_argument('-i', '--input', dest='input', default='data/input.txt', help='File containing sentences to translate (default=data/input)')
parser.add_argument('-t', '--translation-model', dest='tm', default='data/tm', help='File containing translation model (default=data/tm)')
parser.add_argument('-s', '--stack-size', dest='s', default=10, type=int, help='Maximum stack size (default=1)')
parser.add_argument('-n', '--num_sentences', dest='num_sents', default=sys.maxint, type=int, help='Number of sentences to decode (default=no limit)')
parser.add_argument('-l', '--language-model', dest='lm', default='data/lm', help='File containing ARPA-format language model (default=data/lm)')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,  help='Verbose mode (default=off)')
opts = parser.parse_args()

tm = models.TM(opts.tm, sys.maxint)
lm = models.LM(opts.lm)
sys.stderr.write('Decoding %s...\n' % (opts.input,))
input_sents = [tuple(line.strip().split()) for line in open(opts.input).readlines()]

hypothesis = namedtuple('hypothesis', 'logprob, lm_state, predecessor, phrase, transprob')
phrase = namedtuple("phrase", "english, logprob")


## CYK Pseudocode from http://mt-class.org/slides/JHU_MT_lecture_2012-03-27.pdf
## Also based on David Bamman's submitted code
##input: words[1..N]
##for i in 1..N
##  for each unary rule X -> words[i]
##      add (X,i,i) to the chart
##  for span in 1..N
##      for i in 1..(N-span)
##          j = i + span
##          for k in i..j
##              for rule X -> Y Z
##                  if (Y,i,k) and (Z,k,j)
##                      add (X,i,j) to the chart
##  output: (S,1,N)

def initialize_chart(sent):
    #create empty chart
    N = len(sent)
    chart = []
    for i in range(N+1):
        chart.append([{} for _ in range(N+1)])
    #print(chart)
    for i in range(0, N):
        source_tup = (sent[i],)
        if source_tup in tm:
            #iterate through all english phrases
            #print(tm[source_tup])
            for tgt_phrase in tm[source_tup]:
                init_hyp = hypothesis(tgt_phrase.logprob, "", None, tgt_phrase.english, tgt_phrase.logprob)
                #print(init_hyp)
                chart[0][i][tgt_phrase.english]=init_hyp
        else:
            #print("Error, source word not found in translation model")
            x=0
    return chart

def update_logprob_lm(old_logprob, lm_state, old_phrase, curr_word):
    #update the logprob given old logprob, lm_state and current word
    (lm_state, curr_word_logprob) = lm.score(lm_state, curr_word)
    #print(curr_word)
    #print(lm_state, curr_word_logprob)
    #print(curr_word_logprob)
    new_logprob = old_logprob + curr_word_logprob
    #print(new_logprob)
    new_phrase= old_phrase + " " + curr_word
    return (new_logprob, lm_state, new_phrase)

for sent in input_sents:
    #initialize chart for each sentence
    chart = initialize_chart(sent)
    #print(chart)
    N = len(sent)
    ##  for span in 1..N
    ##      for i in 1..(N-span)
    #trying to follow pseudocode notation
    for span in range(1, N):
        for i in range(0, N-span):
    ##          j = i + span
            j = i+span
            startphrase = sent[i:j+1]
            if startphrase in tm:
                lm_state = lm.begin()
                for tgt_phrase in tm[startphrase]:
                    #calculate LM prob for each individual token and update hyp
                    updated_logprob = tgt_phrase.logprob
                    transprob = tgt_phrase.logprob
                    #print(transprob)
                    for ind in tgt_phrase.english.split(" "):
                        (lm_state, ind_logprob) = lm.score(lm_state, ind)
                        updated_logprob = updated_logprob + ind_logprob
                    updated_hyp = hypothesis(updated_logprob, "", None, tgt_phrase.english, tgt_phrase.logprob)
                    #print(updated_logprob)
                    
                    #print(updated_hyp)
                    #seems ok till here
                    chart[span][i][tgt_phrase.english] = updated_hyp
##          for k in i..j
##              for rule X -> Y Z
##                  if (Y,i,k) and (Z,k,j)
##                      add (X,i,j) to the chart

            
                    
            for k in range(0, span):
                st1 = chart[k][i]
                st2 = chart[span-k-1][i+k+1]

                for s1 in heapq.nlargest(opts.s, st1.itervalues(), key=lambda h: h.logprob):
                    for s2 in heapq.nlargest(opts.s, st2.itervalues(), key=lambda h: h.logprob):
                            transprob=s1.transprob + s2.transprob
                            lm_state=lm.begin()
                            old_logprob = transprob
                            new_phrase = ""
                            for curr_word in s1.phrase.split():
                                #print(curr_word)
##                                (new_logprob, new_lm_state, new_phrase) = update_logprob_lm(old_logprob, lm_state, old_phrase, curr_word)
##                                old_logprob = new_logprob
##                                old_phrase = new_phrase
##                                lm_state = new_lm_state

                                (lm_state, word_logprob) = lm.score(lm_state, curr_word)
                                
                                #print(lm_state, word_logprob)
                                old_logprob += word_logprob
                                new_phrase+=curr_word+" " 
                             
                                #print(old_logprob, old_phrase[1:])
                                #a little messy here
                            for curr_word in s2.phrase.split():
##                                (new_logprob, new_lm_state, new_phrase) = update_logprob_lm(old_logprob, lm_state, old_phrase, curr_word)
##                                old_logprob = new_logprob
##                                old_phrase = new_phrase
##                                lm_state = new_lm_state
                                (lm_state, word_logprob) = lm.score(lm_state, curr_word)
                                  #print(lm_state, word_logprob)
                                old_logprob += word_logprob
                                new_phrase+=curr_word+" "
                                
                            new_phrase = new_phrase.rstrip() #remove extra space in the beginning
                            new_logprob = old_logprob #get latest value of logprob to put in hypothesis           
                            h=hypothesis(new_logprob, "", None, new_phrase, transprob)

                            if new_phrase not in chart[span][i] or chart[span][i][new_phrase].logprob < h.logprob:
                                chart[span][i][new_phrase]=h

                            if span < 10:
                                transprob=s1.transprob + s2.transprob
                                lm_state=lm.begin()
                                
                                new_phrase=""
                                old_logprob=transprob
                                for curr_word in s2.phrase.split():
                                    (lm_state, word_logprob) = lm.score(lm_state, curr_word)
                                    old_logprob += word_logprob
                                    #print(word_logprob)
                                    
                                    new_phrase+=curr_word+" " 
                                    #print(logprob)
                                for curr_word in s1.phrase.split():
                                    (lm_state, word_logprob) = lm.score(lm_state, curr_word)
                                    old_logprob += word_logprob
                                    #print(word_logprob)
                                    new_phrase+=curr_word+" "
                                    #print(logprob)

                                new_phrase=new_phrase.rstrip()
                                #print(new_phrase)
                                new_logprob = old_logprob #get latest value
                                h=hypothesis(new_logprob, "", None, new_phrase, transprob)
                                #print(h)
                                if new_phrase not in chart[span][i] or chart[span][i][new_phrase].logprob < h.logprob:
                                    chart[span][i][new_phrase]=h

                                

    winner=heapq.nlargest(opts.s, chart[N-1][0].itervalues(), key=lambda h: h.logprob)
    #chart2[N-1][0] = chart[N-1][0].remove([{}]*N)
    #winner=heapq.nlargest(opts.s, chart[N-3][0].itervalues(), key=lambda h: h.logprob)
    #winner2 = max(chart[N-1][0].itervalues(), key=lambda h: h.logprob)
    #print (chart)
    print "%s" % (winner[0].phrase)


