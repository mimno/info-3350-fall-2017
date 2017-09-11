## The TXT directory contains Shakespeare plays from http://lexically.net/wordsmith/support/shakespeare.html
## For each play there's the complete play and then a separate set of files
##  that contain all the lines for each character separately. We'll focus
##  on the "whole play" files.

## 1. What encoding are the files in? Change the encoding from UTF-8 to the correct
##  value.

## 2. What is the format of the files? How can you extract just text? Modify the code
##  to ignore headers, stage directions, and speaker names.

## 3. Right now we're not saving anything as we read through each play. What data
##  structure should we design so that we can calculate the probability of words
##  by genre?

## 4. Calculate the probability of words in a play and in a genre. For each word
##  in each play, print the word, the two probabilities, and the name of the play
##  and the genre to the screen, separated by tabs, one word per line.

## 5. Practice using the command line tools "sort", "head", "tail", and "grep" to
##  organize and view the output of this script.

import re, sys, glob
from collections import Counter

genre_directories = { "tragedy" : "TXT/tragedies", "comedy" : "TXT/comedies", "history" : "TXT/histories" }

## Here's an example of a simple pattern defining a word token. 
word_pattern = re.compile("\w[\w\-\']*\w|\w")

for genre in genre_directories.keys():
    
    
    for filename in glob.glob("{}/*.txt".format(genre_directories[genre])):
        
        play_counter = Counter()
        
        with open(filename, encoding="utf-8") as file: ## What encoding?
            
            ## This block reads a file line by line.
            for line in file:
                line = line.rstrip()
                
                ## [Add a rule to ignore non-spoken text here]
                
                tokens = word_pattern.findall(line)
                
                play_counter.update(tokens)
        
        ## Simplest possible output
        print(play_counter.most_common(20))