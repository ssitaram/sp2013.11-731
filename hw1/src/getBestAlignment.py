from collections import defaultdict as dd

#source sentences
SRC = open("../data/de.txt", "r")
src_sents = SRC.read()
SRC.close()

#target sentences
TGT = open("../data/en.txt", "r")
tgt_sents = TGT.read()
TGT.close()

OUT = open("../output.txt", "w")
OUT.close()


#translation probability table
TPT = open("../../../../tpts/trans_prob_table3.txt", "r")
trans_prob_table = TPT.read()
TPT.close()
prob_dd = dd(lambda: dd (lambda: 0.0)) 
for line in trans_prob_table.split("\n")[:-1]:
    #print(line)
    src_word = line.split("\t")[0]
    tgt_word = line.split("\t")[1]
    prob = float(line.split("\t")[2])
    prob_dd[tgt_word][src_word] = prob



##it is very late and I am tired so this may be very horrible code##

for src_sent, tgt_sent in zip(src_sents.split("\n"), tgt_sents.split("\n")):
    src_words = src_sent.split(" ")
    tgt_words = tgt_sent.split(" ")[1:]
    align = []
    totalprob = 1
    for tgt_word in tgt_words:
        src_prob_list = []
        for src_word in src_words:
            src_prob_list.append(prob_dd[tgt_word][src_word])

        max_src_prob_word = src_words[src_prob_list.index(max(src_prob_list))]  ###eww
        #print(tgt_word)
        #print(max_src_prob_word)
        align.append(max_src_prob_word)

    OUT = open("../output.txt", "a")
    #print(src_sent)
    #print(align)
    ##The notation `i-j` means the word at position *i* (0-indexed) in the German sentence
    ##is aligned to the word at position *j* in the English sentence
    for i in range(0,len(tgt_words)):
        #print(src_words)
        #print(str(src_words.index(align[i])))
        #print(str(i))
        #print(tgt_words)
        OUT.write(str(src_words.index(align[i]))+"-"+str(i)+" ")
    OUT.write("\n")
    OUT.close()

##for (f, e) in bitext:
##  for (i, f_i) in enumerate(f): 
##    for (j, e_j) in enumerate(e):
##      if dice[(f_i,e_j)] >= opts.threshold:
##        sys.stdout.write("%i-%i " % (i,j))
##  sys.stdout.write("\n")
