"""
In last week's experiment, we wanted to know how many cups of tea someone would
have to get right for us to be convinced that they are not just guessing randomly.
The question was "is there really a difference that Dr. Bristol can taste?"
The intuition was that the more cups tasted, the more convinced we could be.

Today we're going to look at word counts. A question could be "is there really a 
difference between how two authors use the same word?" or "does author A like 
word w more than author B likes that word?" What makes this complicated
is that most words are rare. Even if two authors *like* some word exactly the same,
that doesn't mean they will both *use* the word the same number of times.

In this script we'll be examining a method for finding distinctive words between
two groups of texts: Dunning's g-test. This method tests if two proportions 
(e.g. word frequencies) are significantly different.

For this script we'll be comparing works by Jane Austen and Charles Dickens. 
We'll read the novels from each author's directory and then perform Dunning's 
g-test for each term in the overall vocabulary.

1. Describe the meaning of each cell in the cotingency table for these values:
    Group 1: 10 out of 50, Group 2: 5 out of 50.

2. Using the contingency_table and dunning_g methods, calculate Dunning
   g-scores for the following proportions:
   (a) 100/120, 30/55
   (b) 100/120, 10/12
   (c) 45/100, 105/200
   (d) 0/5, 10/25.
   How do differences in proportions and differences in counts affect the 
   resulting g-scores?

3. What do the magnitude of a g-score indicate?

4. Add code to calculate the Dunning g-score for each term in the vocabulary.
   Print the ten most distinctive words for Austen and Dickens using the
   print_extreme method. What do you think of these terms?

5. Add code to determine the least distinctive term usage by Austen and 
   Dickens. Print the ten least distincitve terms. Are these terms surprising?

6. How would the existing Dunning g-scores change if we removed words from
   our vocabulary? What if instead we added another novel?

"""
import re, sys, glob
import numpy as np
from collections import Counter
from scipy.stats import entropy

word_pattern = re.compile("\w[\w\-\']*\w|\w")

def get_counts(author):
    counter = Counter()
    for filename in glob.glob("{}/pg*.txt".format(author)):
        with open(filename, encoding="utf-8") as reader:
            for line in reader:
                line_tokens = word_pattern.findall(line.lower())
                counter.update(line_tokens)
    return counter

austen_counts = get_counts("Austen")
dickens_counts = get_counts("Dickens")
total_counts = austen_counts + dickens_counts
vocabulary = sorted(list(total_counts.keys()))

def contingency_table(count1, total1, count2, total2):
    table = np.zeros((2,2))
    table[0] = count1, count2
    table[1] = total1-count1, total2-count2
    return table

def dunning_g(table):
  rows = table.sum(axis=1)
  cols = table.sum(axis=0)
  score = 2 * table.sum() * (entropy(rows) + entropy(cols) - entropy(table.ravel()))
  return score

# [2: Add code here.]

gscores = []
for term in vocabulary:
    gscore = None
    # [4: Add code to calculate a term's Dunning g-score]
    gscores.append(gscore)

# Print the the top k word-score pairs
def print_extreme(words, scores, k, is_top):
  k_pos = None
  if is_top:
    k_pos = np.argsort(scores)[::-1][:k]
  else:
    k_pos = np.argsort(scores)[:k][::-1]
  print(k_pos)
  for i, pos in enumerate(k_pos):
    print("{}. {}: {}".format(i+1, words[pos], scores[pos]))

print("Most distinctive words used by Jane Austen and Charles Dickens:")
# [4: Add code here.]
print("\nLeast distinctive terms used by Jane Austen and Charles Dickens:")
# [5: Add code here.]
