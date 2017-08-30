### On Monday we talked about how encodings allow us to map
###  bytes to characters. In this lesson we'll look at finding
###  meaningful groups of characters.

### In the git repo you will find six files containing 
###  sample text. Each is selected to highlight issues in
###  tokenization. I've included a template for the first
###  one, which we will modify together in class.

import re, sys

## SAMPLE 1

## Here's an example of a simple pattern defining a word token. 
word_pattern = re.compile("[\w]+")

with open("sample1.txt", encoding="utf-8") as file:
    
    ## This block reads a file line by line.
    for line in file:
        line = line.rstrip()
        
        ## This converts a string (line) into a list (tokens)
        tokens = word_pattern.findall(line)
        
        print(tokens)

### [Discuss sample 1 here.]

## SAMPLE 2

### [Copy and modify code as necessary here.]

### [Discuss sample 2 here.]


## SAMPLE 3

### [Copy and modify code as necessary here.]

### [Discuss sample 3 here.]


## SAMPLE 4

### [Copy and modify code as necessary here.]

### [Discuss sample 4 here.]


## SAMPLE 5

### [Copy and modify code as necessary here.]

### [Discuss sample 5 here.]


## SAMPLE 6

### [Copy and modify code as necessary here.]

### [Discuss sample 6 here.]

