## The TXT directory contains Shakespeare plays from http://lexically.net/wordsmith/support/shakespeare.html
## For each play there's the complete play and then a separate set of files
##  that contain all the lines for each character separately. We'll focus
##  on the "whole play" files.

## 1. The code currently causes a "math domain error". Why, and how can you fix it?

## 2. We're adding up the log probabilities of the words. Why is the log function important?
##  What would happen if we calculated the probability of a play instead of the log probability?

## 3. Look at the log probability of each play according to each genre's language model.
##  What do you think of these numbers? How does the length of the play relate?

## 4. How accurate is the classifier? Are we allowing the classifier to "peek" at the 
##  data we're asking it to classify? Modify the code to remove the effect of each play in turn.

## 5. Reevaluate your classifier. What has changed? What do you think of this difference?

## 6. Why is the classifier making the decisions it does? What separates "comedy" words from "tragedy"
##  words? How can you pick apart the computation we're doing here to measure the impact of specific words?
##  Work on this part in groups.

import re, sys, glob, math
from collections import Counter

genre_directories = { "tragedy" : "TXT/tragedies", "comedy" : "TXT/comedies", "history" : "TXT/historical" }

word_pattern = re.compile("\w[\w\-\']*\w|\w")

genre_play_counts = {}
genre_counts = {}
all_counts = Counter()

for genre in genre_directories.keys():
    
    genre_play_counts[genre] = {}
    genre_counts[genre] = Counter()
    
    for filename in glob.glob("{}/*.txt".format(genre_directories[genre])):
        
        play_counter = Counter()
        
        genre_play_counts[genre][filename] = play_counter
        
        with open(filename, encoding="utf-16") as file: ## What encoding?
            
            ## This block reads a file line by line.
            for line in file:
                line = line.rstrip()
                if not line.startswith("\t"):
                    continue
                
                line = line.lower()
                
                tokens = word_pattern.findall(line)
                
                play_counter.update(tokens)
        
        genre_counts[genre] += play_counter
        all_counts += play_counter

vocabulary = all_counts.keys()
vocabulary_size = len(vocabulary)

genres = genre_play_counts.keys()

## Now loop through all plays and decide which genre they match most closely

print("\t".join(genres))

for real_genre in genres:
    
    for filename in genre_play_counts[real_genre].keys():
        play_counter = genre_play_counts[real_genre][filename]
        play_sum = sum(play_counter.values())
        
        genre_scores = {}
        
        for genre in genres:
            genre_counter = genre_counts[genre]
            genre_sum = sum(genre_counter.values())
            genre_scores[genre] = 0
            
            for word in play_counter:
                p_word_in_genre = (genre_counter[word]) / (genre_sum)
                genre_scores[genre] += play_counter[word] * math.log(p_word_in_genre)
            
            genre_scores[genre] /= play_sum
        
        max_score = max(genre_scores.values())
        
        print("{:.3f}\t{:.3f}\t{:.3f}\t{}".format(genre_scores['tragedy'], genre_scores['comedy'], genre_scores['history'], filename))
