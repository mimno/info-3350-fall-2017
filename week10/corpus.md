I wanted to build a Horror collection. I started by looking at the Gutenberg site to see if they had already curated a list. After a bit of browsing I came to this page:

    http://www.gutenberg.org/wiki/Horror_(Bookshelf)

I downloaded the page using curl:

    curl "http://www.gutenberg.org/wiki/Horror_(Bookshelf)" > gutenberg_horror.html

This grabbed the contents of the page and redirected the output to a file. The quotation marks are important because the url has parentheses.

I looked at the contents of the page. The links to actual documents seemed to be of the form `www.gutenberg.org/ebooks/[id]`.

I next created a python script, `download.py`. This script looks at each line of a file and searches for the following regular expression pattern:

    www.gutenberg.org/ebooks/(\d+)

If this pattern is found, the digits at the end will be copied into the first match group.

To make sure this was working, I stopped there and set the script to print the IDs I found. Here's the output:

    $ python download.py gutenberg_horror.html 
    14154
    375
    23172
    11074
    16726
    10897
    ...

There were quite a few rows, I used `wc -l` to count them:

    $ python download.py gutenberg_horror.html | wc -l
          49

49 volumes seemed about right, and the pattern in the page seemed pretty consistent, so I decided it was working well enough.

Next I added some code to actually download the documents. I started by going to the page for one of the books, which contains links to all of the possible versions held by Gutenberg for that text. I want the UTF-8 text, of course, so I looked at that link: `http://www.gutenberg.org/ebooks/375.txt.utf-8`. I vaguely remembered from before that the actual link was something else, so I tried clicking on it. The URL bar read `http://www.gutenberg.org/cache/epub/375/pg375.txt`, so it does look like there's a hidden redirect there.

Most HTTP libraries should be able to handle redirects, but there's no reason not to just go for the "true" URL if that will work. But which library? I remember that there's a particularly good HTTP library for python, and a quick Google search points me to the `requests` package, which sounds familiar. That page has a nice short example, which i used to create my own code.

Grabbing files from URLs is a dangerous business, so I made sure to check the request status. Then I ran my script. As usual, it didn't run at first. Here's the error:

    $ python download.py gutenberg_horror.html 
    Traceback (most recent call last):
      File "download.py", line 11, in <module>
        response = requests.get()
    TypeError: get() missing 1 required positional argument: 'url'

I want to create a URL for each book ID, and I had originally constructed that string inside the `get()` command. But then I decided that I wanted to be able to print the URL I had requested if there were any problems, so I cut that expression out of the argument of the `get()` function and pasted it one line above, defining a new variable `url`. I then went back down to the error checking code to add a print statement containing my new `url` variable, but forgot to put the variable in the `get()` statement!

After fixing that bug, I ran the script again. At this point it sat for a while doing nothing. I wished I had kept the statement that prints the book IDs in, so I could at least tell if it was stuck. But it returned after about 45 seconds, with three errors:

    $ python download.py gutenberg_horror.html 
    problem with 6534 at http://www.gutenberg.org/cache/epub/6534/pg6534.txt: 404
    problem with 19797 at http://www.gutenberg.org/cache/epub/19797/pg19797.txt: 404
    problem with 53419 at http://www.gutenberg.org/cache/epub/53419/pg53419.txt: 404

The first two of these are audiobooks and the third I saved manually. I then checked to see if I had successfully downloaded anything.

    $ ls -l
    -rw-r--r--    1 mimno  staff   306868 Oct 29 12:46 pg10002.txt
    -rw-r--r--    1 mimno  staff   180104 Oct 29 12:46 pg10007.txt
    -rw-r--r--    1 mimno  staff   575789 Oct 29 12:46 pg10053.txt
    -rw-r--r--    1 mimno  staff   333638 Oct 29 12:46 pg10150.txt
    -rw-r--r--    1 mimno  staff   338502 Oct 29 12:46 pg10542.txt
    -rw-r--r--    1 mimno  staff  1025163 Oct 29 12:46 pg10662.txt
    -rw-r--r--    1 mimno  staff   129924 Oct 29 12:46 pg10897.txt
    -rw-r--r--    1 mimno  staff   204062 Oct 29 12:46 pg11074.txt
    -rw-r--r--    1 mimno  staff   132428 Oct 29 12:46 pg11438.txt
    ....

Along with the script and the original HTML file, I had about the right number of `pgID.txt` files. They have about the right size for volume-length documents, and they all have varying sizes. If I get a lot of short files of exactly the same length, I know I'm usually hitting an error page or a "get lost, robot" page.

To check that the books were loading correctly, I checked a file at random, which turned out to be Kafka's *The Trial*. Horror? I guess. But the file seemed clean. I'm particularly interested in accented characters and "smart quotes", which will show if non-ascii character encodings are being handled correctly. I don't see anything one way or another, so we may be ok.

How much text do we have? I used `wc` again to check:

    $ wc *.txt
        5688   54197  306868 pg10002.txt
        3693   31291  180104 pg10007.txt
       13666   90436  575789 pg10053.txt
        6082   60307  333638 pg10150.txt
    ...
      9036   74594  427642 pg8492.txt
      4986   51050  283532 pg9629.txt
    342234 3161269 18092894 total

About 3M words. Not huge, but quite respectable.

One of the notorious problems with using Project Gutenberg texts for computation is that they insert a large volume of legal text at the beginning and end of each document. This text can skew statistics, and I'd like to remove it. But Gutenberg has been operating for decades and the exact wording and format of the license text varies considerably, so it's difficult to remove.

I started with the headers. These often end with an all-caps statement about the text starting. I first checked the term "START", but that seems to be used for the start of the text and the start of the license. What about "START OF"? I used `grep -c "START OF" *.txt` to check whether this occurs exactly once in every document, and it seems to. Is this what I think it is?

    $ grep "START OF" *.txt
    pg10002.txt:*** START OF THIS PROJECT GUTENBERG EBOOK THE HOUSE ON THE BORDERLAND ***
    pg10007.txt:*** START OF THIS PROJECT GUTENBERG EBOOK CARMILLA ***
    pg10053.txt:*** START OF THIS PROJECT GUTENBERG EBOOK LA VAMPIRE ***
    pg10150.txt:***START OF THE PROJECT GUTENBERG EBOOK DRACULA'S GUEST***
    pg10542.txt:***START OF THE PROJECT GUTENBERG EBOOK THE BOATS OF THE "GLEN CARRIG"***
    ...

Everything looked right. All the lines were clearly marking the beginning of a text. So would this work with the end? Not quite, there were three false positives: "MYSTERIOUS FRIEND OF VARNEY.", "THE END OF THE SOLAR SYSTEM", and "CHAPTER XV--THE END OF THE MEETING". None of these contained asterisks, though, and all of the real end-of-text lines did, with the small variation of whether there was a space after the three asterisks or not.

