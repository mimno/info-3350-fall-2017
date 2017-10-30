"""
We'll use this script in class to build some intuitions about entropy and KL divergence.

These were inspired by work from Simon DeDeo.
"""

import random, math

## Anne thinks of trees more often, Bertha prefers cars
things = ["tree", "bird", "car"]
anne_probs = [0.5, 0.25, 0.25]
bertha_probs = [0.25, 0.25, 0.5]

def think_of(p, n):
    return random.choices(things, weights=p, k=n)

## If we're optimizing for Anne's probability distribution, how many questions will it take to guess a particular value?
def guess_anne(value):
    if value == "tree":
        return 1
    else:
        return 2

## If we're optimizing for Bertha's probability distribution, how many questions will it take to guess a particular value?
def guess_bertha(value):
    if value == "car":
        return 1
    else:
        return 2

## Count the total questions for a list of choices, given a particular guessing script
def average_questions(choices, guesser):
    total_questions = 0
    for value in choices:
        total_questions += guesser(value)
    return total_questions / len(choices)

## Kullback-Leibler divergence
def kl(p, q):
    value = 0.0
    for i in range(len(p)):
        if p[i] != 0:
            value += p[i] * math.log2(p[i] / q[i])
    return value