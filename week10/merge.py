import glob, re

start_pattern = re.compile(r"^\*+ ?START OF")
end_pattern = re.compile(r"^\*+ ?END OF")
punctuation_pattern = re.compile(r"[\.,\?!\";\:]")

for filename in glob.glob("pg*.txt"):
    
    with open(filename, encoding="utf-8") as reader:
        position = "header"
        for line in reader:
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
                    line = punctuation_pattern.sub("", line).lower().replace("--", " -- ")
                    print(line)