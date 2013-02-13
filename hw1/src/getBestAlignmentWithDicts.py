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


###changes###
#read in sure and maybedicts as dicts of dicts##

SUREDICT = open("sure.dict", "r")
MAYBEDICT = open("maybe.dict", "r")
suredict = {}
maybedict = {}
surefile = SUREDICT.read()
maybefile = MAYBEDICT.read()
SUREDICT.close()
MAYBEDICT.close()

for line in surefile.split("\n"):
    tgtword = line.split(" : ")[0]
    restsrc = line.split(" : ")[1]
    if restsrc.find(":") != -1:
        print("there's a colon in the dict")
    restsrc = line.split(" : ")[1].split(" ")
    for idx in range(0, len(restsrc)-1, 2):
        if tgtword not in suredict.keys():
            suredict[tgtword] = {}
        suredict[tgtword][restsrc[idx]] = restsrc[idx+1]
        
for line in maybefile.split("\n"):
    tgtword = line.split(" : ")[0]
    restsrc = line.split(" : ")[1]
    if restsrc.find(":") != -1:
        print("there's a colon in the dict")
    restsrc = line.split(" : ")[1].split(" ")
    for idx in range(0, len(restsrc)-1, 2):
        if tgtword not in maybedict.keys():
            maybedict[tgtword] = {}
        maybedict[tgtword][restsrc[idx]] = restsrc[idx+1]
        
#print(suredict)
#print(maybedict)
#translation probability table
TPT = open("trans_prob_table70k.txt", "r")
trans_prob_table = TPT.read()
TPT.close()
prob_dd = dd(lambda: dd (lambda: 0.0)) 
for line in trans_prob_table.split("\n")[:-1]:
    #print(line)
    src_word = line.split("\t")[0].lower()
    tgt_word = line.split("\t")[1].lower()
    prob = float(line.split("\t")[2])
    prob_dd[tgt_word][src_word] = prob



##it is very late and I am tired so this may be very horrible code##

for src_sent, tgt_sent in zip(src_sents.split("\n")[:10], tgt_sents.split("\n")[:10]):
    src_words = src_sent.split(" ")[:-1]
    tgt_words = tgt_sent.split(" ")[1:]
    align = []
    totalprob = 1
    for tgt_word in tgt_words:
        tgt_word = tgt_word.lower()
        ##changes##
        ##top 10 candidates for source word with probabilities##
        candidatedict = {}
        candidatelist = []
        src_prob_list = []
        #print(src_words)
        for src_word in src_words:
            src_word = src_word.lower()
            src_prob_list.append(prob_dd[tgt_word][src_word])
            candidatedict[src_word] = prob_dd[tgt_word][src_word]
        #print("Target word "+tgt_word)
        #print("Source words "+str(src_words))
        #print("Candidate dict ")
        #print(candidatedict)
        max_src_prob_word = src_words[src_prob_list.index(max(src_prob_list))]  ###eww
        max_prob = max(src_prob_list)
        swinsuredict = {}
        if tgt_word in suredict.keys():
            for sw in suredict[tgt_word]:
                if sw in src_words:
                    swinsuredict[sw] = suredict[tgt_word][sw]

        if tgt_word in suredict.keys():
            if max_src_prob_word not in swinsuredict.keys() and swinsuredict != {} and max_prob < 0.05:
                print(tgt_word+" wants to align with "+max_src_prob_word)
                #print("Does not agree with dictionary!")
                #print(swinsuredict)
                #now pick the highest valued candidate from the dictionary and assign it to max_src_prob_word
                max_src_prob_word,ignored = max(swinsuredict.iteritems(), key=lambda x:x[1])
                print("Replacing with "+max_src_prob_word)
                #max_src_prob_word = max_src_prob_word+"?"
        #print(tgt_word)
        #print(max_src_prob_word)
        align.append(max_src_prob_word)
        #print(candidatedict)

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
        if align[i][-1] == "?" and align[i] != "?":
            align[i] = align[i][:-1]
            OUT.write(str(src_words.index(align[i]))+"?"+str(i)+" ")
        else:
            OUT.write(str(src_words.index(align[i]))+"-"+str(i)+" ")
    OUT.write("\n")
    OUT.close()

##for (f, e) in bitext:
##  for (i, f_i) in enumerate(f): 
##    for (j, e_j) in enumerate(e):
##      if dice[(f_i,e_j)] >= opts.threshold:
##        sys.stdout.write("%i-%i " % (i,j))
##  sys.stdout.write("\n")
