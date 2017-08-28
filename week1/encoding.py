## This is part one of this week's assignment. It looks at characters.
## Part two will involve tokenization of files into words.
## To turn in this assignment, you will create a zip file containing the `week1` directory.
## Some answers will involve adding code, and we will be able to see the output when we run the script. For others, you will need to add your response in comments.

### Compatibility check: Does this word look like greek? Does it print to the screen correctly?
greek = "μῆνιν"
print(greek)

### 1. From characters to codepoints with `ord`.
###  This function takes a character and returns a numeric codepoint.
###  Python 3 uses Unicode natively. 
print("The codepoint is {}".format(ord("A")))
### Modify the following two lines to print the codepoint in hexadecimal and zero-padded 8-bit binary.
### Useful: https://docs.python.org/3.6/library/string.html#format-specification-mini-language
print("The codepoint in hex is {}".format(ord("A")))
print("The codepoint in binary is {}".format(ord("A")))


### 2. From codepoints to characters with chr().
print("The character is {}".format(chr(97)))
### copy the previous line to find the character for codepoint 210.


### 3. From codepoints to bytes with encode()
### The following example string contains four codepoints.
english = "word"
### The encode() function maps the abstract codepoints to bytes, and returns
###  a byte array, which is not a string but may look like one.
print(english.encode("utf-8"))
### a. Change the encoding to "ascii", "utf-16", and "iso-8859-1" (Latin 1). Describe what happens in the comment below.
### [answer here]

### b. Try a more interesting example. What happens when you convert an Icelandic
###  string to ascii, utf-8, utf-16, and iso-8859-1? You may need to look carefully at the byte array.
icelandic = "orð"
### [answer here]

### c. Now use the `greek` variable from above, and try the same encodings.
### [answer here]

### 4. From bytes to codepoints with decode()
### To invert the transformation from bytes to codepoints we need to specify an encoding scheme. What happens if we get it wrong?
### a. Write code to encode the `greek` word in UTF-8, but then decode it as Latin 1, and print the result. What happens?
### [code here]

### [description here]

### b. Do this transformation once again (encode as UTF-8, decode as Latin 1). What does it look like?
### [code here]

### [description here]


### 5. Whitespace and punctuation. Consider this string:
"This string has a tab\tand, as well, more\r\nthan one line."
### Write a for-loop that prints the codepoint for each character.
### [code here]


### 6. Something is strange about this string. Use the tools you've seen so far to inspect it. Is it what it appears?
weird_string = "Eﬃciency is the ﬁnal reﬂection"
### [description here, with any helpful code]


### 7. One of the responses I got Friday looked like this when I opened it.
text_with_Os = "He said ÒDonÕt worry!Ó, but I didnÕt believe him."
## In the comment below, describe what happened. What characters are not showing correctly, and why are they displaying as they are? Hint: figure out what OS the student was using.
### 
### [answer here]


### 8. The file "mystery.txt" is in a standard encoding, but which one?
###  
###  a. Fill in the correct encoding in code below (it's not UTF8).
### UNCOMMENT THE FOLLOWING 3 LINES (it will cause a UnicodeDecodeError)
#with open("mystery.txt", encoding="utf-8") as file:
#    for line in file:
#        print(line)
print("The text is in LANGUAGE")
###  b. Figure out what language the text is in, and include it below. You may use any internet resource.

