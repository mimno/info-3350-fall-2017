"""

We want to find interpretable, low-dimensional models of documents. What does 
a Singular Value Decomposition do, and why might it be useful?

You will need the novels-gutenberg directory in the current directory.

1. Working with vectors and matrices. At the >>> python prompt, create this matrix:

  x = np.array([[1,2,3], [1,2,3], [1,2,3]])

Now describe the value of the following expressions. Write your answers between lines.

a. x[1,1]
b. x[:,1]
c. x[1,:]
d. np.diag(x[1,:])
e. x.T
f. x[1,:].dot( x[2,:] )
g. x[:,0].dot( x[:,1] )
h. x.dot( x[:,1] )
i. x.dot( x )
j. x.dot( np.diag(x[1,:]) )
k. x ** 2
l. x - np.array([1,2,3])
m. x - np.array([1,2,3])[:,None]
n. np.sum(x)
o. np.sum(x, axis=0)
p. np.sum(x, axis=1)
q. np.sum(x ** 2, axis=1)
r. np.sqrt(np.sum(x ** 2, axis=1))


2. The code below runs an SVD. Describe some properties of these matrices.

[Response here]

3. Describe the properties of the `weights` vector.

[Response here]

4. What is the first column of the file_vectors and word_vectors (transpose) matrix representing?

[Response here]

4. What is the second column of the file_vectors and word_vectors (transpose) matrix representing?

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

## 
weighted_word_vectors = word_vectors.dot( np.diag(np.sqrt(weights)) )
weighted_file_vectors = file_vectors.dot( np.diag(np.sqrt(weights)) )