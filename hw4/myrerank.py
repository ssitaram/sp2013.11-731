#!/usr/bin/env python
import optparse
import sys
import bleu

from sklearn import linear_model
import numpy
import random
import os
OUT = open("test.trans", "w")
OUT.close()

optparser = optparse.OptionParser()
optparser.add_option("-d", "--dev-kbest-list", dest="input", default="data/devnew.100best", help="100-best dev translation lists")
optparser.add_option("-r", "--ref", dest="ref", default="data/dev.ref", help="dev references")
optparser.add_option("-k", "--test-kbest-list", dest="test", default="data/testnew.100best", help="100-best test translation lists")
optparser.add_option("-l", "--lm", dest="lm", default=-1.0, type="float", help="Language model weight")
optparser.add_option("-t", "--tm1", dest="tm1", default=-0.5, type="float", help="Translation model p(e|f) weight")
optparser.add_option("-s", "--tm2", dest="tm2", default=-0.5, type="float", help="Lexical translation model p_lex(f|e) weight")
(opts, _) = optparser.parse_args()
weights = {'p(e)'       : float(opts.lm) ,
           'p(e|f)'     : float(opts.tm1),
           'p_lex(f|e)' : float(opts.tm2),
           'numtgt': -0.25,
           'numru': -0.25
           }
test_all_hyps = [pair.split(' ||| ') for pair in open(opts.test)]

#initial input is devset to make training examples and train the log reg model
all_hyps = [pair.split(' ||| ') for pair in open(opts.input)]

REF = open(opts.ref, "r")
all_ref = REF.read().split("\n")
num_sents = len(all_hyps) / 100
allindic = []
alltrainfeats = []

HYPFILE = open("scorehyps", "w")
HYPFILE.close()

REFFILE = open("scorerefs", "w")
REFFILE.close()

#generate training examples 
for s, ref in zip(xrange(0, num_sents), all_ref):
  #get all hyps for single sentence
  hyps_for_one_sent = all_hyps[s * 100:s * 100 + 100]
  count = 0
  ##TODO repeat this 10 times so that num_sents*10 training examples are generated
  while count < 3:
    count = count + 1
    #get two random hyps
    num1 = random.randint(0, 99)
    num2 = random.randint(0, 99)
    if num1 == num2:
      if num1 == 0:
        num2 = num2 + 1
      else:
        num2 = num2 - 1 #just making sure they arent the same example
    hyp1 = hyps_for_one_sent[num1][1]
    #print(hyp1)
    hyp2 = hyps_for_one_sent[num2][1]
    #print(hyp2)
    feats1 = hyps_for_one_sent[num1][2]
    feats2 = hyps_for_one_sent[num2][2]

    #calculate bleu score for each example
    s1=list(bleu.bleu_stats(hyp1, ref))
    bs1=bleu.bleu(s1)
    s2=list(bleu.bleu_stats(hyp2, ref))
    bs2=bleu.bleu(s2)
    #print(bs1, bs2)
    #make training vector with difference in values of feats and indicator
    if bs1 > bs2:
      indic = 1
    else:
      if bs1 < bs2:
        indic = -1
      else:
          continue
      #ignore the ones that have same bleu score?
    #get feat values for each pair of features and subtract
    trainfeats = []
    for f1, f2 in zip(feats1.split(), feats2.split()):
      (k1, v1) = f1.split("=")
      (k2, v2) = f2.split("=")
      #print(k1, v1, k2, v2)
      fdiff = eval(v2) - eval(v1)
      trainfeats.append(fdiff)
    #print(trainfeats)
    allindic.append(indic)
    alltrainfeats.append(trainfeats)
    
    HYPFILE = open("scorehyps", "a")
    HYPFILE.write(hyp1+"\n"+hyp2+"\n")
    HYPFILE.close()
    REFFILE = open("scorerefs", "a")
    REFFILE.write(ref+"\n"+ref+"\n")
    REFFILE.close()

# score all hyps with meteor
os.system("java -Xmx1G -jar meteor-1.4/meteor-1.4.jar scorerefs scorehyps | grep Segm > meteorscores")
indicators = []
# read meteor scores
MET=open("meteorscores")
met = MET.read()
allMeteorScores=[]
for line in met.split("\n"):
  toks=line.split("\t")
  score=float(toks[1])
  #print(score)
  allMeteorScores.append(score)
MET.close()
#print(len(alltrainfeats))
#print(len(allMeteorScores))

for i in range(len(alltrainfeats)):
  if allMeteorScores[i*2+1] < allMeteorScores[i*2]:
    val = 1
  else:
    val = -1
  indicators.append(val)
#print(alltrainfeats)
#print(indicators)
#print(len(indicators))
#print(len(alltrainfeats))
#response variables
feats = numpy.array(alltrainfeats)
ind = numpy.array(indicators)
#print(feats, ind)
logreg=linear_model.LogisticRegression(fit_intercept=False, penalty="l2")    
logreg.fit(feats, ind)

# update weights
weights['p(e)']=logreg.coef_[0][0]
weights['p(e|f)']=logreg.coef_[0][1]
weights['p_lex(f|e)']=logreg.coef_[0][2]
weights['numtgt']=logreg.coef_[0][3]
weights['numru']=logreg.coef_[0][4]

#print(weights)
num_sents_test = len(test_all_hyps) / 100
for s in xrange(0, num_sents_test):
  hyps_for_one_sent = test_all_hyps[s * 100:s * 100 + 100]
  (best_score, best) = (-1e300, '')
  score = 0.0
  for (num, hyp, feats) in hyps_for_one_sent:
      for feat in feats.split(' '):
        (k, v) = feat.split('=')
        score += weights[k] * float(v)
      if score > best_score:
        (best_score, best) = (score, hyp)
  sys.stdout.write("%s\n" % best)
