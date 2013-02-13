Summary of my method:
The base model I used was IBM model1, run on 8 iterations with the entire data. I used a few heuristics while calculating the most probable source word aligned to the target word, which were:
1. Noticing that many punctuation marks got aligned to words, I aligned all punctuations to themselves if they were present in the source candidates
2. Many German and English words are same (like proper nouns) so I aligned them if there was an exact match in source and target
3. Some English words are very similar to German words and have affixes in German. So I aligned German and English words that had a substring match on an English word. This can backfire for small words, so the minimum length of the English word had to be 5.

I also had some ideas to use the development gold standard labels, but unfortunately it did not give me an improvement in AER. Originally, I wanted to use a German-English dictionary, but since I did not find any on the web that I could use easily, I decided to try and construct a "dictionary" using the gold standard alignments. I extracted all the "sure" aligned words and created a dictionary with counts of how many times the words were aligned to the target word. Then while aligning source and target words I looked up the dictionary and one of the source words was found in the dictionary, I used it for alignment. Using this technique gave me worse results than the baseline, and I suspect it is because the dictionary was quite small, since the dev data was relatively small.

To construct the probabilty table, run IBMModel.py
To align using heuristics mentioned above, run getBestAlignmentHeuristics.py