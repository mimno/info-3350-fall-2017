"""
Ex 15: More Dunning's log-likelihood test, Multiple hypotheses.

Can an observation be significant but not convincing?

In text mining we often count things and compare 
proportions. Frequently we can count the same thing
in different contexts, like a word in two different
novels. If we want to make claims about differences
between contexts, we need to know whether an observed
difference could have arisen by random chance.
We can use Ted Dunning's
G^2 metric as an indicator of significance, but how does 
the number of words we test affect our evaluation of 
significance?

First, refresh your memory about Dunning's G^2:

1. As we did last week, try a few different proportions.
Record the output of dunning_score(...) here.

2. What score do you think indicates a difference that you
would consider convincing evidence that two observed
proportions are really different?

Now let's look at the difference between two Greek
historians, Herodotus and Thucydides.

3. Run `print_nicely(word_scores[:50])`. Copy the output here.
How do the observed Dunning G scores compare to your expectation?

4. What are the most "surprising" words according to 
the Dunning score? Search through the documents for examples.
What did you learn about the content and the style of these
two historians?

We're looking at about 5000 distinct tests, one for each
word. Should we be worried? Let's simulate random
word distributions.

5. Now create two lists, `fake_herodotus` and `fake_thucydides`
using the `shuffle_lists()` function with the `herodotus_tokens`
and `thucydides_tokens` lists as input. Record the length of
all four lists here, and confirm that the new ones have
the same length as the original `_tokens` lists.

6. Now use the "fake" token lists to create `fake_scores`.
Use `print_nicely()` and array slices (ie [:50], etc) to look
at the range of Dunning scores. How do the "most significant" 
scores compare to your expectations about significance?
Would you have been fooled if you didn't realize that
these results were random?

7. Thucydides writes "for it is the habit of humans to trust
the things they desire to unexamined hope, but to confront
the things they reject with the full force of reason." 
How is this relevant to our discussions?

"""

from collections import Counter
import math, re, random

word_pattern = re.compile("\w[\w\-\']*\w|\w")

thucydides_tokens = []
herodotus_tokens = []

scored_words = []

### Evaluate the "surprise factor" of two proportions that are expressed as counts.
###  ie x1 "heads" out of n1 flips.
def dunning_score(x1, x2, n1, n2):
    p1 = float(x1) / n1
    p2 = float(x2) / n2
    p = float(x1 + x2) / (n1 + n2)
    
    return -2 * ( x1 * math.log(p / p1) + (n1 - x1) * math.log((1 - p)/(1 - p1)) + 
                  x2 * math.log(p / p2) + (n2 - x2) * math.log((1 - p)/(1 - p2)) )

with open("thucydides.txt") as thucydides:
    for line in thucydides:
        thucydides_tokens.extend(word_pattern.findall(line))
    
with open("herodotus.txt") as herodotus:
    for line in herodotus:
        herodotus_tokens.extend(word_pattern.findall(line))

def score_differences(a, b):
    a_counter = Counter(a)
    b_counter = Counter(b)

    a_length = len(a)
    b_length = len(b)
    vocabulary = a_counter.keys() & b_counter.keys()
    
    scored_words = []
    
    for w in vocabulary:
        a_n = a_counter[w]
        b_n = b_counter[w]
        
        ## Create a tuple containing information about each word
        g_score = dunning_score(a_n, b_n, a_length, b_length)
        scored_words.append( (round(g_score, 3), a_n, b_n, w) )
        scored_words.sort(reverse = True)
    
    return scored_words

def shuffle_lists(a, b):
    a_length = len(a)
    b_length = len(b)
    
    merged = list(a)
    merged.extend(b)
    random.shuffle(merged)
    
    return (merged[:a_length], merged[a_length:])

def print_nicely(scores):
    for word_info in scores:
        print("{}\t{}\t{}\t{}".format(word_info[0], word_info[1], word_info[2], word_info[3]))

word_scores = score_differences(herodotus_tokens, thucydides_tokens)

