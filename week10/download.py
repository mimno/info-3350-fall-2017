import sys, requests, re

book_id_pattern = re.compile(r"www.gutenberg.org/ebooks/(\d+)")

with open(sys.argv[1], encoding="utf-8") as reader:
    for line in reader:
        match = book_id_pattern.search(line)
        if match:
            book_id = match.group(1)
            url = "http://www.gutenberg.org/cache/epub/{}/pg{}.txt".format(book_id, book_id)
            response = requests.get(url)
            if response.status_code == requests.codes.ok:
                with open("pg{}.txt".format(book_id), "w", encoding="utf-8") as writer:
                    writer.write(response.text)
            else:
                print("problem with {} at {}: {}".format(book_id, url, response.status_code))
