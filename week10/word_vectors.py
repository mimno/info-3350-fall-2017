"""

Like LSA and topic modeling, the goal of word embeddings is to create a numeric representation of the meaning of words. I've given you three word embedding matrices. (I use "word embedding" and "word vector" interchangeably.)

Start with `horror.vec`, which is an embedding trained on our collection of horror fiction:

    python -i word_vectors.py horror.vec

1. The function `get_vector()` retrieves the vector for a string. Pick a word and get its vector. What is the dimension of this vector?

[Response here]

2. The function `nearest()` sorts all words by their cosine similarity to a specified vector. The arguments are a vector and a number of nearest neighbors. Search for three or more words and copy the 20 nearest neighbors here. What is the closest word to your query vector, and what is its cosine similarity?

[Response here]

3. Go back to the `context.py` script, and search for one of the same words, using context-size five. (Use `.most_common(100)` to avoid pages and pages of output.) Now do the same for some of the words that the embedding said were nearest. Are their context words similar?

[Response here]

4. Go back to the embedding vectors. Now try searching for the sum of two vectors: just use `+`! Search for three pairs of words, and copy the 20 nearest neighbors here. What do you notice about the single closest vector? How is this different from the previous question?

[Response here]

5. What about subtraction? Use the same examples as in the previous problem, but this time search for the *difference* between vectors (use `-`). Comment on what changes and what stays the same.

[Response here]

6. The file `original.vec` is trained in the same way on the same files, but without modifications to the text. Load these vectors instead of `horror.vec`. Run the same queries. What do you think is different about how I pre-processed the training data?

[Response here]

7. The file `ecco_vectors.vec` has embeddings trained by Ryan Heuser on billions of words from 18th century books. Load this file, and try at least five queries. This can include single words or combinations of words. How are these different from the vector results from the smaller Horror fiction data set? What do you notice about words in 18th century books?

[Response here]

"""

import numpy as np
import sys

reader = open(sys.argv[1], encoding="utf-8")

# The first line of the file gives the dimensions of the matrix
first_line = reader.readline()
fields = first_line.split(" ")
n_rows = int(fields[0])
n_cols = int(fields[1])

word_vectors = np.zeros((n_rows, n_cols))
vocabulary = []
word_ids = {}

for line in reader:
    fields = line.strip().split(" ")
    word = fields[0]
    vector = np.array(fields[1:], dtype=float)
    norm = np.linalg.norm(vector)
    
    # in some odd cases a word may have no vector
    if norm == 0.0:
        continue
    
    # record the word and its row position in the matrix
    word_id = len(vocabulary)
    vocabulary.append(word)
    word_ids[word] = word_id
    
    word_vectors[word_id] = vector / norm

## look up the id for a word, and grab the row associated with that word
def get_vector(word):
    return word_vectors[ word_ids[word] ]

## define a shortcut
v = get_vector

def nearest(v, n):
    norm = np.linalg.norm(v)
    if norm > 0.0:
        v /= norm
    return(sorted(zip(word_vectors.dot(v), vocabulary), reverse=True)[:n])

