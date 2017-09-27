"""

Today we'll finish up our new corpus and start thinking about clustering.
Specifically, what are the issues in agglomerative clustering?

QUESTIONS

1. This code is currently assuming the structure of the OTA corpus. Convert it to 
use the structure of our new corpus.

[Describe changes in code here]

2. Agglomerative clustering merges the closest pair of clusters. What should happen then? List possible options and their advantages / disadvantages.

[Response here]

3. What makes agglomerative clustering fast or slow?

[Response here]

4. What do you notice about the distances between merged clusters in this implementation as the algorithm proceeds?

[Response here]

5. What do you think of agglomerative clustering? Is it reasonable? Is the output useful? Why or why not? What would you prefer?

[Response here]

"""

import re, sys
import numpy as np
from collections import Counter

word_pattern = re.compile("\w[\w\-\']*\w|\w")

novel_metadata = {} # <- dict of dicts
novel_counts = {} # <- dict of Counters
word_counts = Counter()

metadata_fields = ["filename", "title", "author", "year", "language", "license"]


## Read a collection, one .txt file per document, with metadata from a .tsv.
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
    
    ## Record the total number of times each word occurs
    word_counts.update(counter)

## All the distinct word types in one list
vocabulary = list(word_counts.keys())

## All the filenames
filenames = list(novel_counts.keys())

## Allocate a matrix with two rows for every file and one column for every word type
file_word_counts = np.zeros([ 2 * len(filenames), len(vocabulary) ])

## Convert a map of file-level counters to a single matrix
## We'll use two index variables, file_id and word_id. These will be 
##  *numbers*, not strings, that point to a string in either of
##  the two arrays.
for file_id in range(len(filenames)):
    counter = novel_counts[ filenames[file_id] ]
    
    for word_id in range(len(vocabulary)):
        file_word_counts[file_id,word_id] = counter[ vocabulary[word_id] ]
    
    ## Normalize for length
    file_word_counts[file_id,:] /= np.sum(file_word_counts[file_id,:])

pairwise_distances = []

for file_a in range(len(filenames)):
    
    ## The original files will be normalized, but the merged 
    ##  nodes will not, so make sure everything adds up to 1.0
    counts_a = file_word_counts[file_a,:] / np.sum(file_word_counts[file_a,:])
    for file_b in range(file_a + 1, len(filenames)):
        
        counts_b = file_word_counts[file_b,:] / np.sum(file_word_counts[file_b,:])
        
        diff_a_b = np.sum( np.abs( counts_a - counts_b ) )
        
        pairwise_distances.append( (file_a, file_b, diff_a_b) )

## Sort in ascending order by similarity
pairwise_distances.sort(key = lambda x: x[2])

num_nodes = len(filenames)
parents = list(range(2 * len(filenames)))

constituent_files = []
for filename in filenames:
    constituent_files.append([filename])

## Now merge until we have only X nodes left
while num_nodes < len(filenames) + 100:
    closest_pair = pairwise_distances.pop(0)
    
    file_a = closest_pair[0]
    file_b = closest_pair[1]
    
    new_node = num_nodes
    constituent_files.append(constituent_files[file_a] + constituent_files[file_b])
    
    file_word_counts[new_node,:] = file_word_counts[file_a,:] + file_word_counts[file_b,:]
    
    print("{:3d}: merging {} and {} ({:.4f})".format(new_node, file_a, file_b, closest_pair[2]))
    parents[file_a] = new_node
    parents[file_b] = new_node
        
    ## Remove pairs involving merged nodes
    pairwise_distances = [x for x in pairwise_distances if x[1] != file_a and x[2] != file_a and x[1] != file_b and x[2] != file_b]
    
    pairwise_distances.sort(key = lambda x: x[2])
    
    ## Now add the new distances for the merged node
    counts_new = file_word_counts[new_node,:] / np.sum(file_word_counts[new_node,:])
    for file_b in range(num_nodes):
        ## only compare unmerged nodes
        if parents[file_b] == file_b:
            counts_b = file_word_counts[file_b,:] / np.sum(file_word_counts[file_b,:])
            
            diff_new_b = np.sum( np.abs( counts_new - counts_b ) )
            
            pairwise_distances.append( (new_node, file_b, diff_new_b) )
    
    num_nodes += 1

for node in range(num_nodes):
    print(node)
    
    ## Look for unmerged nodes
    if parents[node] == node:
        for filename in constituent_files[node]:
            print("  {} - {} / {}".format(filename, novel_metadata[filename]["title"], novel_metadata[filename]["author"]))