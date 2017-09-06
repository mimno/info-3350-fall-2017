## This is a little script I used to convert files with multi-line paragraphs
## separated by empty lines into a format with one line per paragraph, and no
## breaks. You won't need it today, but I include it for interest.

import sys

line_buffer = []

with open(sys.argv[1]) as file:
    for line in file:
        line = line.rstrip()
        if line == "":
            print(" ".join(line_buffer))
            line_buffer = []
        else:
            line_buffer.append(line)

print(" ".join(line_buffer))