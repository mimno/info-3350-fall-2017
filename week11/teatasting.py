"""
Randomization Tests

Load this script interactively:

    python -i teatasting.py

Goal: We often want to make arguments that variables are related. For example, we might want to argue that one author uses a word more often than another, or that 19th C novels use longer sentences than 20th century novels. But with finite and often small samples, we could find patterns that are really just random chance. How do we tell whether two variables are actually related, or if there is only chance similarity?

The key question is: what would I observe if there were no connection between the two variables? An experiment is *statistically* convincing if the pattern I saw is sufficiently unlikely by random chance. But what do "unlikely" and "sufficiently" mean?

We'll start by replicating the "Tea Tasting" experiment from R.A. Fisher's book "The Design of Experiments" (1935). Here the two variables are (1) whether milk was added to a cup before or after the tea and (2) whether a taster says the milk was added before or after. 

1. Run the function "guess_equal()" with n=8, 10 times. Record your results here:

[Response here]

2. How important is it that we know how many positive examples there are? Run the function "guess_randomly()", also with n=8, 10 times. Record your results. How are these results different from #2? Would you be more or less willing to tolerate a mistake?

[Response here]

3. In the `run_experiments` function, write a "for" loop that runs `guess_equal` function `num_trials` times. Use the `results` Counter to keep track of how many times you get each number of correct guesses. Run this function 10 times with 1000 trials each, and record your results here:

[Response here]

4. Change the number of trials from 8 to 10. (You will need to specify a new "correct" array.) Rerun your experiments from #3. How many times do you get >= 8 correct? 

[Response here]

5. If someone tells you they can tell the difference between Gimme's Espresso Blend and Holiday Blend, what experiment would you design to test their ability? How many cups would you ask them to taste, and what would you tell them about the experiment? How many cups would you need them to taste for you to be satisfied that they really can tell the difference even if they make a mistake?

[Response here]


"""

from collections import Counter
import random

eight_cups = [1, 1, 0, 0, 1, 0, 1, 0]

## Simulate a random guess with an equal number of positives/negatives
def guess_equal(correct):
    n = len(correct)
    
    ## Make a copy of the correct list, then shuffle it
    guess = list(correct) 
    random.shuffle(guess)
    
    print(correct)
    print(guess)
    
    correct_guesses = 0
    for i, j in zip(correct, guess):
        if i == j:
            correct_guesses += 1
            
    return correct_guesses

def guess_randomly(correct):
    n = len(correct)
    
    ## Simulate purely random guessing
    guess = []
    for i in range(n):
        guess.append(random.randint(0,1))
    
    print(correct)
    print(guess)
    
    correct_guesses = 0
    for i, j in zip(correct, guess):
        if i == j:
            correct_guesses += 1
            
    return correct_guesses

def run_experiments(correct, num_trials):
    results = Counter()
    
    ### Write your "do num_trials experiments" for-loop here:
    
    return results