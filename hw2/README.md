Methods I tried:

1. Simple METEOR with 10PR/9P+R(lower than baseline)

2. METEOR including bigrams and trigrams (sort of like a combination of BLEU and METEOR, 0.509925, higher than baseline)
python meteor.py

3. 2 + stemming words in hyp1, hyp2 and reference and removing punctuation (0.516887)
python meteor-stem.py

4. 3 + synonym matching of hyp1 and hyp2 with reference words (0.51842)
python meteor-syn.py