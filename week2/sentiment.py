### The two readings for this week try to model plot as a cycle of positivity 
### and negativity. How well can we measure these constructs in novels?

### In this work we'll look at evaluating documents with respect to a fixed
### vocabulary. I've included two sample sentiment lexicons, one by 
### Bing Liu and one from Matt Jockers' "syuzhet" package.

### ( For an interactive look, see this page: https://mimno.infosci.cornell.edu/sentiment/ )

## Example usage: python sentiment.py syuzhet.csv txt/oliver.txt

# 1. There's a bug in the code. All the paragraphs are being scored as 0.
#  Fix it, and describe what was happening. 

## [Description here]

# 2. I'm using the Counter class from the `collections` package instead of a 
#  python `dict`. Consult the documentation https://docs.python.org/3/library/collections.html
#  and describe four features that Counter provides that dict does not.

## a.
## b.
## c.
## d.

# 3. The directory `txt` contains works by Charles Dickens in the correct format:
#  one paragraph per line. Apply the two lexicons to `tale.txt`. Do they work?
#  Do they agree? Provide specific examples.

## [Description here]

# 4. The code is currently just adding up all the scores for each word token.
#  This favors longer documents: if we just repeat the contents twice, the score doubles.
#  What happens if we normalize by document length? In the `score_counts` function,
#  divide the score by the total number of tokens.

## [Describe how the output changes here. Is this normalization a good idea? Why or why not?]

# 5. Working with your table, create a lexicon for one of the emotions listed on
#  on the board, or choose your own. You may collect additional documents to test
#  your lexicon, please include these if so.

## [Include your team's final lexicon in your zip file. Discuss here your personal experience. What was hard about this process?]

# 6. I've set this up so that we are looking at the most extreme passages in 
#  the sources. What does this approach show, and what does it hide? How does it
#  affect how we evaluate the tool?

## [Discuss here]

#### IDEAS FOR YOUR WRITING RESPONSE FOR FRIDAY:

## Both groups are working from Vonnegut's description of plot. Does this
##  view really reflect plot? If not, what is missing, and how important is it
##  to you?
##
## Given your experience with lexicon-based sentiment analysis, how well does
##  it approximate a quantity that's relevant for plot analysis?
##
## Would a more nuanced view of emotion lead to a better representation of plot?


import re, sys
from collections import Counter

## The script takes two command line arguments: the lexicon file and the text file

## Format: each line is [word],[weight]
lexicon_file = sys.argv[1]
## Format: each line is one paragraph
text_file = sys.argv[2]

## Create a mapping from words to numbers
word_weights = {}
with open(lexicon_file) as lexicon_reader:
    for line in lexicon_reader:
        weight, word = line.split(",") ## split on comma
        word_weights[word] = float(weight) ## convert string to number

## Here's an example of a simple pattern defining a word token. 
word_pattern = re.compile("\w[\w\-\']*\w|\w") ## what matches this?

## Now look at the actual documents. We'll create a list with one object per text segment.
paragraphs = []

## This function applies the word weights to a list of word counts
def score_counts(counter):
    ## accumulate word weights in this variable
    score = 0
    
    ## count the words in the passage
    total_tokens = sum(counter.values())
    ## check for empty segments
    if total_tokens == 0:
        return 0
    
    ## for each word, look up its score
    for word in counter.keys():
        if word in word_weights:
            score += word_weights[word] * counter[word]
    return score

## here's where we actually read the file
with open(text_file, encoding="utf-8") as file:
    
    ## This block reads a file line by line.
    for line in file:
        line = line.rstrip()
        
        tokens = word_pattern.findall(line)
        
        ## turn a list into a word->count map
        paragraph_counts = Counter(tokens)
        
        ## create the paragraph object, with the original text, 
        ##  the word counts, and the total score.
        paragraphs.append({ 'text': line, 'counts': paragraph_counts, 'score': score_counts(paragraph_counts) })

## Now sort the objects, in place, by score
paragraphs.sort(key = lambda x: x['score'])

## Display the 10 most negative
for paragraph in paragraphs[0:9]:
    print("{}\t{}".format(paragraph['score'], paragraph['text']))

## ... and the 10 most positive
for paragraph in paragraphs[-10:-1]:
    print("{}\t{}".format(paragraph['score'], paragraph['text']))

