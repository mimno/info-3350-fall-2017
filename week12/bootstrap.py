"""
On Monday we examined a method for finding distinctive words between two
groups of texts. Specifically, we looked for significantly different word
usages between Jane Austen and Charles Dickens. However, the collection of
texts we used was far from complete; our corpus was biased. Adding or removing
volumes could dramatically change the distinctiveness of existing words. How
can we be confident that a word has significantly different usage by Jane
Austen than Charles Dickens? As usual, we can't ask them to write more novels.

Today we'll examine a method for checking our confidence in a measurement:
bootstrap sampling. We often want to measure properties of a dataset by
calculating the value of some function of that dataset. This could be as 
simple as a sample mean, or as complicated as a word embedding model.

We can't expand our real dataset, but we can create lots of *similar* datasets
by sampling with replacement from the real dataset. Using a large number of
these "bootstrap" samples, and calculating the value of the same function
of each sample, we can estimate whether the value we actually got is 
reliable, or if small changes to the dataset cause large changes in the
function value. 

In this script we'll look at how the presence/absence of particular novels in
week10's horror collection affect our trained word embeddings, particularly
how a word's neighbors change. We'll use bootstrap sampling to measure how
stable a word's neighbors are given this collection.

0. Ensure that python packages gensim and nltk are installed. For Anaconda, use
   the following command: "conda install [package name]"

1. Construct bootstrap samples of size 5 for the following groups using the
   bootstrap_sample method:
   (a) [1, 2, 3, 4, 5]
   (b) [0, 2, 0, 2, 2]
   (c) [1, 1, 1, 7, 1]
   How do these samples differ from the original group? How much can a
   particular bootstrap sample deviate from the original? Include specific
   examples.

2. Let's now examine how a measurement, in this case arithmetic mean, differs
   between a collection and its bootstrap samples. We'll be summarizing the
   resulting bootstrap means through averaging (i.e. constructing a mean of
   means). For 100-item collections with the following underlying
   distributions:
   (a) [0, 1, 2, 3, 4, 5, 6, 8, 9]
   (b) [0, 0, 1, 1, 1, 1, 8, 10, 11, 12],
   construct twenty 25-item bootstrap samples. Print the mean of the
   original collection and the mean of the means of its bootstrap samples.
   Describe how these values differ.

3. How does the mean of bootstrap means change with respect to the "true" mean
   of the original collection as the bootstrap sample size is increased or 
   decreased?

4. Switching to word embeddings, write code to build a word embedding for a
   bootstrap sample of size n over a list of novels. Which words will have
   fairly stable nearest neighbors and which will not? For five "query" words,
   list the words that are consistently close to that word in all bootstrap
   models, and some words that only appear as nearest neighbors once or twice.
   Try to find at least one query word whose neighbors are very stable, and one
   whose neighbors are variable. What might account for this difference?

"""
import glob, re
import nltk
import numpy as np

from gensim.models import Word2Vec

# Insure that required nltk data is downloaded
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

start_pattern = re.compile(r"^\*+ ?START OF")
end_pattern = re.compile(r"^\*+ ?END OF")
punctuation_pattern = re.compile(r"[\.,\?!\";\:]")

word_pattern = re.compile("[^\W\d_][\w\-\']*[^\W\d_]|[^\W\d_]")

# This dictionary maps a filename to its corresponding list of tokenized
# sentences. Each entry correspnds to a novel in our horror collection. 
novel_sentences = {}

# This code reads in our horror novels and transforms them into tokenized
# sentences which will be used to build word embeddings.
for filename in glob.glob("horror/pg*.txt"):
    sentences = []
    with open(filename, encoding="utf-8") as reader:
        content = reader.read()
        position = "header"
        # First remove the Project Gutenberg headers and footers.
        clean_lines = []
        for line in content.split('\n'):
            line = line.rstrip()
            if position == "header":
                match = start_pattern.search(line)
                if match:
                    position = "text"
            elif position == "text":
                match = end_pattern.search(line)
                if match:
                    position = "footer"
                    break
                else:
                    line = line.lower().replace("--", " -- ")
                    clean_lines.append(line)
        clean_content = '\n'.join(clean_lines)
        # Tokenize cleaned text by sentence and word.
        for sentence in sent_tokenize('\n'.join(clean_lines)):
            sentence_tokens = word_pattern.findall(sentence)
            sentences.append(sentence_tokens)
    novel_sentences[filename] = sentences

# Size n bootstrap sample from input group of items.
def bootstrap_sample(items, n):
    return np.random.choice(items, size=n, replace=True)

# Note: This is not element-wise multiplication, but rather repeats the items
# in the list 10 times.
collection_a = [0,1,2,3,4,5,6,7,8,9]*10
collection_b = [0,0,1,1,1,1,8,10,11,12]*10
bootstraps_a = None
bootstraps_b = None

"""
2. Add code here. Use the print statements below to print out the resulting
   means.
"""
#print('(a): true: {}, sample: {}, bootstrap: {}'.format(?, ?, ?))
#print('(b): true: {}, sample: {}, bootstrap: {}'.format(?, ?, ?))

# This method trains a word embedding using the tokenized sentences associated
# with filenames_list. Note that including duplicate filenames means that 
# multiple copies of a novel's sentences are used for training.
def word_embedding(filenames_list):
    # Gather input sentences
    sentences = []
    for filename in filenames_list:
        sentences.extend(novel_sentences[filename])
    return Word2Vec(sentences)

# Get the n closest neighbors of a word within a word embedding.
def nearest(embedding, word, n):
    return embedding.similar_by_word(word, n)

# Train a word embedding using a size n bootstrap sample of filenames_list.
def bootstrap_embedding(filenames_list, n):
    print("Code for #4 is missing") # Remove upon finishing problem 4
    # 4. Add code here.
