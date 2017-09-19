"""
In this script we'll be examining another similarity measure: Burrows's delta. Unlike
the techniques in nearest.py, Burrows's delta measures the similarity of a text with
 a group of texts.

For this script we'll read all of the ota novels and identify the overall author 
groups. Then, we'll calculate the similarity between these author groups and one file,
specified by the user.

QUESTIONS

1. How many authors are there? What problems exist with this author set? Modify how 
author metadata is interpreted within the code.

[Response here, modifications in code.]

2. What is the range of Burrows's delta? How does it differ from previous measures in
nearest.py?

[Response here]

3. How is a numpy array different than a list? Why use numpy arrays instead of lists?

[Response]

4. What are the three most likely authors of ota/5166.txt ("The Monk" by Matthew Gregory) 
according to Burrows's delta? What's the smallest number of most frequent words that can
be used to correctly identify the author of ota/5166.txt? Use the `sort -n` command to 
sort the output.

[Response here]

5. Why is Burrows's delta so accurate for ota/4855.txt ("The castle of Otranto")?

[Response here]

6. Can word sets other than the most frequent be used with Burrows's delta to identify 
authorship? Do different word frequency ranges describe different aspects of a text?

[Response here]

7. Are there texts that look very similar according to cosine similarity (e.g. Gothic) that
have very different author signatures according to Burrows's delta?

[Response here]

"""

import re, sys
import numpy as np
from collections import Counter

## Usage: nearest.py [filename to compare]
query_filename = sys.argv[1]

word_pattern = re.compile("\w[\w\-\']*\w|\w")

novel_metadata = {} # <- dict of dicts
novel_counts = {} # <- dict of Counters
author_counts = {} # <- dict of Counters
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
    novel_metadata[filename] = metadata

    ## Now count the words in the novel
    counter = Counter()
    with open(filename, encoding="utf-8") as file:
        
        ## This block reads a file line by line.
        for line in file:
            line = line.rstrip()
            
            tokens = word_pattern.findall(line)
            
            counter.update(tokens)
    
    ## And save those counts for later
    novel_counts[filename] = counter

    ## Update author subset counts if current file is not the query file
    if filename != query_filename:
        author = metadata["author"]
        author_counts[author] = author_counts.get(author, Counter()) + counter

    ## Record the fact that each word in this novel occurred at least once
    ## by passing the list of unique terms, not their token counts
    word_novels.update(counter.keys())

## All the distinct word types in one list
vocabulary = list(word_novels.keys())

## Get author frequencies
author_freqs = {}
for author in author_counts.keys():
    counter = author_counts[author]
    count = np.array([counter[v] for v in vocabulary])
    freq = (count / np.sum(count)) * 100 # <- percentage
    author_freqs[author] = freq

corpus_freqs = np.mean(list(author_freqs.values()), axis=0)
corpus_stds = np.std(list(author_freqs.values()), axis=0)

## Get vocabulary indicies for most frequent words
working_index = np.argsort(corpus_freqs)[::-1][:150]
working_means = corpus_freqs[working_index]
working_stds = corpus_stds[working_index]

## Burrows's delta score
def delta(author_freqs, text_counter):
    ## Calculate frequencies for text
    text_count = np.array([text_counter[vocabulary[i]] for i in working_index])
    text_fingerprint = (text_count / sum(text_counter.values())) * 100 # <- percentage
    
    author_fingerprint = author_freqs[working_index]
    
    ## Calculate zscores
    text_zscores = (text_fingerprint - working_means) / working_stds
    author_zscores = (author_fingerprint - working_means) / working_stds
    
    ## Calculate delta
    delta = np.mean(np.absolute(text_zscores - author_zscores))

    return delta

for author in author_freqs.keys():
    score = delta(author_freqs[author], novel_counts[query_filename])
   
    print("{:.2f} {}".format(score, author))
    