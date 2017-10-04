"""

Today we'll work on the k-means algorithm. This will be due Wednesday night after 
the break. Write your responses individually, but discuss and compare results 
with your colleagues. 

You may want to save examples of clusterings to discuss how results change. One
way to save output to a file is:

    python kmeans.py > c10-v10000-r1.txt

I've named the file to remind me that this is run #1 with 10 clusters and a 10000 
word vocabulary. Use whatever names are useful for you. 

Include these files in your zip file if you refer to them.

Have the novels-gutenberg repo in the same directory as this script, but do not
inlude it when you turn in your work.

QUESTIONS

1. Run the clustering algorithm. How do your results compare to other people at
your table? Give some examples of similarities and differences. Does the level
of variability concern you?

[Response here]

2. By default we're using cosine similarity. Change the `score` function to 
point to absolute similarity. Does this change anything? Compare your clusters
to others at your table. Could you tell the difference between cosine-based
clusters and absolute-based clusters?

[Response here]

3. We're starting with 10 clusters. Experiment with different numbers of clusters. 
Describe how the results change or do not change.

[Response here]

4. By default we're using a vocabulary of the 10000 most common words. Try different
settings, such as the 44 most common, or middle-frequency words. How do results 
differ? 

[Response here]

5. In the agglomerative clustering algorithm we had to compare every document to
every other document. Count the number of comparisons we're making in the k-means
algorithm. How is it different, and why would that matter?

[Response here]

6. We're printing the title and author of each work, but we have other information
as well. Modify the printing code at the end to add one of our other metadata
fields. Do you notice -- or not notice -- any patterns?

[Response here]

7. Describe, in your own words, how the k-means algorithm works. Imagine you are 
speaking to a clever but non-technical person, like a supreme court justice.

[Response here]

"""

import re, sys
import numpy as np
from collections import Counter

num_clusters = 10

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

## All the filenames
filenames = list(novel_counts.keys())

## Allocate a matrix with two rows for every file and one column for every word type
file_word_counts = np.zeros([ len(filenames), len(vocabulary) ])

## Allocate a matrix for the cluster means
cluster_means = np.zeros([ num_clusters, len(vocabulary) ])
cluster_sizes = np.zeros(num_clusters)

## Randomly initialize cluster allocations
cluster_assignments = np.random.choice(num_clusters, len(filenames))

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

## Define some similarity functions between files and clusters

def cosine_sim(file_id, cluster_id):
    a = file_word_counts[file_id,:]
    b = cluster_means[cluster_id,:]
    
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    
    return a.dot(b) / (a_norm * b_norm)

def absolute_sim(file_id, cluster_id):
    a = file_word_counts[file_id,:]
    b = cluster_means[cluster_id,:]
    
    return 2.0 - np.sum(np.abs(a - b))

## In python functions are variables, so we can set the value of a variable
##  to a function in order to change behavior.
score = cosine_sim

## The main loop: move means, reassign clusters
for iteration in range(100):
    
    ## Step 1: With the current cluster assignments, calculate the cluster means
    cluster_means[:,:] = 0.0 # clear everything
    cluster_sizes[:] = 0.0
    for file_id in range(len(filenames)):
        cluster_id = cluster_assignments[file_id]
        
        cluster_means[cluster_id,:] += file_word_counts[file_id,:]
        cluster_sizes[cluster_id] += 1
    
    ## Step 1a: What should we do with empty clusters?
    for cluster_id in range(num_clusters):
        if cluster_sizes[cluster_id] == 0:
            random_file = np.random.choice(len(filenames), 1)[0]
            cluster_means[cluster_id,:] += file_word_counts[random_file,:]
        else:
            cluster_means[cluster_id,:] /= cluster_sizes[cluster_id]
    
    ## Step 2: With the current cluster means, reassign files to clusters
    for file_id in range(len(filenames)):
        ## Create an empty array
        cluster_scores = np.zeros(num_clusters)
        ## and fill it with the similarity score of each cluster
        for cluster_id in range(num_clusters):
            cluster_scores[cluster_id] = score(file_id, cluster_id)
        ## Now find the cluster id with the largest score
        cluster_assignments[file_id] = np.argmax(cluster_scores)


## Now print the members of each cluster
for cluster_id in range(num_clusters):
    print(cluster_id)

    cluster_files = [filenames[f] for f, c in enumerate(cluster_assignments) if c == cluster_id]
    for filename in cluster_files:
        print("  {} / {}".format(novel_metadata[filename]["Title"], novel_metadata[filename]["Author"]))