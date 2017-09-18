"""
The ota directory contains 18th century novels from the Oxford Text Archive
For each volume there's a file in plain text format. Information about
each volume is in the metadata.tsv file in tab-delimited format.

This week we'll be looking at the idea of similarity between documents.
What makes two documents different, and how does our representation of
documents affect this calculation? Do our measurements of similarity
relate to existing ideas about genre, authorship, and influence?

For this script we'll read all the novels first and then calculate their
similarity to one file, specified by the user.

QUESTIONS

1. In the Jaccard function we're using `set`s to implement intersection and union.
How is a set different from a list? What happens when you call `set()` on a 
dictionary? What about a Counter?

[Response here]

2. What is the range of possible values for each of the three functions? What
values indicate closeness or distance? Modify the output of the `absolute_distance()`
function so that it is more like the output of the other two functions.

[Response here]

3. Absolute and cosine are much slower than Jaccard. Why? Can you modify the code
to make them faster? If so, why does it work, and what does that tell you about
the use of language?

[Written response here, modifications in code]

4. Compare the most similar volumes to ota/5166.txt ("The Monk") according to 
each of the three metrics. How similar are the orderings? Use the `sort -n` command
to sort the output.

[Response here]

5. Why are the values of these similarity metrics so different?

[Response here]

6. Is "the Gothic novel" a thing? Does it have clear boundaries based on your
analysis? Why or why not?

"""

import re, sys, glob, math
from collections import Counter

## Usage: nearest.py [filename to compare]
query_filename = sys.argv[1]

word_pattern = re.compile("\w[\w\-\']*\w|\w")

novel_metadata = {}
novel_counts = {}
word_novels = Counter()

metadata_fields = ["filename", "title", "author", "year", "language", "license"]

for line in open("metadata.tsv"):
    ## Get the next line of the metadata file, and split it into columns
    fields = line.rstrip().split("\t")
    
    ## Convert the list of field values into a map from field names to values
    metadata = dict(zip(metadata_fields, fields))
    
    if not "author" in metadata:
        metadata["author"] = "Unknown"
    
    ## Save it for later with the filename as key
    filename = metadata["filename"]
    novel_metadata[filename] = metadata # <- dict of dicts.
    
    ## Now count the words in the novel
    counter = Counter()
    with open(metadata["filename"], encoding="utf-8") as file:
        
        ## This block reads a file line by line.
        for line in file:
            line = line.rstrip()
            
            tokens = word_pattern.findall(line)
            
            counter.update(tokens)
    
    ## And save those counts for later
    novel_counts[filename] = counter
    
    ## Record the fact that each word in this novel occurred at least once
    ##  by passing the list of unique terms, not their token counts
    word_novels.update(counter.keys())

## All the distinct word types in one list
vocabulary = word_novels.keys()

## set distance: |A intersect B| / |A union B|
def jaccard_similarity(a, b):
    shared_words = len( set(a) & set(b) )
    all_words = len( set(a) | set(b) )
    
    return float(shared_words) / all_words

## probability distance
def absolute_distance(a, b):
    score = 0
    
    sum_a = sum(a.values())
    sum_b = sum(b.values())
    
    for word in vocabulary:
        prob_a = a[word] / sum_a
        prob_b = b[word] / sum_b
        score += abs( prob_a - prob_b )
    
    return score

## vector angle distance
def cosine_similarity(a, b):
    score = 0
    
    length_a = 0
    for x in a.values():
        length_a += x * x
    length_a = math.sqrt(length_a)
    
    length_b = 0
    for x in b.values():
        length_b += x * x
    length_b = math.sqrt(length_b)
    
    for word in vocabulary:
        score += a[word] * b[word]
    score /= length_a * length_b
    
    return score

for filename in novel_metadata.keys():
    score = jaccard_similarity(novel_counts[filename], novel_counts[query_filename])
    #score = absolute_distance(novel_counts[filename], novel_counts[query_filename])
    #score = cosine_distance(novel_counts[filename], novel_counts[query_filename])
   
    print("{:.5f} {} / {} [{}]".format(score, novel_metadata[filename]["title"], novel_metadata[filename]["author"], filename))
    