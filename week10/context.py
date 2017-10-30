"""

What does the context of a word tell us? This will be the basis of word embeddings, but it's good to get some intuitions about what these look like.

We'll use a collection of ghost stories from Gutenberg as an example.

1. Look at the context of words with the `contexts` function. Find three interesting examples with context size 5. (Copy enough output to get a sense of what's there, don't copy everything if it's long.)

[Response here]

2. Try smaller and larger context windows. What can you get from the larger windows that you can't from the smaller windows? What can you still see from small windows (1 or 2 words)? [hint: try different parts of speech]

[Response here]

3. Now use `nearby_words` to summarize these contexts. Use the Counter `most_common()` function if the results are too large. How much can you tell about a word from its top 20 most frequently co-occurring words? How does the window size affect this?

[Response here]

4. Use the `smoothed_kl` function to measure the divergence between Counters. You can either generate these from the `nearby_contexts` function with window size 2 or use the `total_counts` Counter for the whole collection. Compare five words to the `total_counts` distribution. What word has the least divergence? Why do you think that might be so?

[Response here]

5. Compute the same values, but with three progressively larger window sizes. What happens to the KL divergence? What happens to the relative differences in KL divergence?

[Response here]

6. Show five examples of pairs of words that you think are similar and five that you think are not. Show multiple window sizes for each pair. Do these results match your intuitions?

[Response here]

"""

import sys, glob, re, math
from collections import Counter

word_pattern = re.compile("\w[\w\-\']*\w|\w")

## For simplicity, we'll just load the entire collection into one big list of tokens, ignoring boundaries between documents.
tokens = []

for filename in glob.glob("pg*.txt"):
    with open(filename, encoding="utf-8") as reader:
        for line in reader:
            line_tokens = word_pattern.findall(line)
            
            tokens.extend(line_tokens)

total_tokens = len(tokens)
total_counts = Counter(tokens)
vocabulary_size = len(total_counts.keys())

### The keyword-in-context view (KWIC)
def contexts(word, n):
    for i in range(total_tokens):
        if tokens[i] == word:
            ## Show the n previous and n subsequent words
            pre_context = " ".join(tokens[i-n:i])
            post_context = " ".join(tokens[i+1:i+n+1])
            print("{} [{}] {}".format(pre_context, tokens[i], post_context))

### A summary of the words that appear near a target word
def nearby_words(word, n):
    counter = Counter()
    for i in range(total_tokens):
        if tokens[i] == word:
            ## Count up the n previous and n subsequent words
            counter.update(tokens[i-n:i])
            counter.update(tokens[i+1:i+n+1])
    return counter

### Treat two Counters as probability distributions, and calculate their divergence
def smoothed_kl(p, q):
    value = 0.0
    
    sum_p = sum(p.values())
    sum_q = sum(q.values())
    
    for word in total_counts.keys():
        p_prob = (p[word] + 0.01) / (sum_p + 0.01 * vocabulary_size)
        q_prob = (q[word] + 0.01) / (sum_q + 0.01 * vocabulary_size)
        value += p_prob * math.log2(p_prob / q_prob)
    return value
