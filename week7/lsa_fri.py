"""

We want to find interpretable, low-dimensional models of documents. What does 
a Singular Value Decomposition do, and why might it be useful?

You will need the novels-gutenberg directory in the current directory.

1. Working with vectors and matrices part II. At the >>> python prompt, create this matrix:

  x = np.array([[ 0.37962213,  1.21124263,  0.56771852],
       [ 1.36941388,  2.62035395,  2.25421422],
       [ 0.72534686,  1.55442357,  1.90488544]])

Now create the SVD:

  (U, s, V) = np.linalg.svd(x)

Now describe the value of the following expressions. What is the code doing?
Why do you get the results you see? Write your answers between lines.

a. U
b. s
c. U[:,0]
d. U[:,0].dot(U[:,0])
e. U[:,0].dot(U[:,1])
f. V[0,:].dot(V[0,:])
g. V[0,:].dot(V[1,:])
# In addition to your description, compare the following expressions to the original matrix x
h. np.outer( U[:,0], V[0,:] )
i. np.outer( U[:,0], V[0,:] ) * s[0]
j. np.outer( U[:,0], V[0,:] ) * s[0] + np.outer( U[:,1], V[1,:] ) * s[1]
k. np.outer( U[:,0], V[0,:] ) * s[0] + np.outer( U[:,1], V[1,:] ) * s[1] + np.outer( U[:,2], V[2,:] ) * s[2]

2. Imagine that half your documents are in English and half are in French. What might be different about the `weights` array?

[Response here]

3. Use the `sort_vector()` function to examine the word and document vectors. Find some examples that are surprising, interesting, or confusing.

[Response here]

4. Do you trust 2D visualizations of documents? Why or why not? What would you want to know before using one?

[Response here]

"""

import re, sys
import numpy as np
from collections import Counter

word_pattern = re.compile("\w[\w\-\']*\w|\w")

novel_metadata = {} # <- dict of dicts
novel_counts = {} # <- dict of Counters
word_counts = Counter()

## Open the metadata file and read the header line
metadata_reader = open("novels-gutenberg/metadata.tsv")
metadata_fields = metadata_reader.readline().rstrip().split("\t")

## Read the rest of the lines of the file
for line in metadata_reader:
    
    ## Get the next line of the metadata file, and split it into columns
    fields = line.rstrip().split("\t")
    
    ## Convert the list of field values into a map from field names to values
    metadata = dict(zip(metadata_fields, fields))
    
    if not "Author" in metadata:
        metadata["Author"] = "Unknown"
    
    ## Save it for later with the filename as key
    filename = "novels-gutenberg/text/pg{}.txt".format(metadata["ID"])
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

## All the distinct word types in descending order by frequency
vocabulary = [x[0] for x in word_counts.most_common()]

vocabulary = vocabulary[0:10000]
reverse_vocabulary = {}
for word_id, word in enumerate(vocabulary):
    reverse_vocabulary[word] = word_id

## All the filenames
filenames = list(novel_counts.keys())
titles = [novel_metadata[id]["Title"] for id in filenames]

## Allocate a matrix with two rows for every file and one column for every word type
file_word_counts = np.zeros([ len(filenames), len(vocabulary) ])

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

## Run the singular value decomposition
(file_vectors, weights, word_vectors) = np.linalg.svd(file_word_counts, full_matrices=False)

## transpose word vectors
word_vectors = word_vectors.T

## Absorb the factor weights into the matrices
weighted_word_vectors = word_vectors.dot( np.diag(np.sqrt(weights)) )
weighted_file_vectors = file_vectors.dot( np.diag(np.sqrt(weights)) )

## Write data to files, which we can load with R

with open("file_vectors.tsv", "w") as out:
    for i in range(len(file_vectors[0,:])):
        out.write("V{}\t".format(i))
    out.write("Title\n")
    
    for file_id in range(len(filenames)):
        for i in range(len(file_vectors[file_id,:])):
            out.write("{:.6f}\t".format(file_vectors[file_id,i]))
        out.write("{}\n".format(titles[file_id]))

with open("word_vectors.tsv", "w") as out:
    for i in range(len(word_vectors[0,:])):
        out.write("V{}\t".format(i))
    out.write("Word\n")
    
    for word_id in range(len(vocabulary)):
        for i in range(len(word_vectors[word_id,:])):
            out.write("{:.6f}\t".format(word_vectors[word_id,i]))
        out.write("{}\n".format(vocabulary[word_id]))


## Pass in a vector and a list of strings that define a meaning for each
##  element in the vector. Sort the elements by value and print the top
##  and bottom strings.
def sort_vector(v, names):
    sorted_list = sorted(list(zip(v, names)))
    for pair in sorted_list[:10]:
        print(pair)
    for pair in sorted_list[-10:]:
        print(pair)


