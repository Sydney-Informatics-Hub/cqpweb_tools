# TODO

1. Rearrange the corpus files so that the texts are in the order specified in the spreadsheet - see data/original_ids.csv for the original text IDs and the order which they should be occuring according to the spreadsheet
2. Reindex the corpus on a local version of the CQPweb stack
3. Test the reindexed corpus with a bunch of searches compared against the current live CQPWeb
4. Reindex the CQPweb version

Reindexing notes

XML- go to the "manage corpus XML" tab in the navigator on prod

there's a template for it "XML tempates"

1  text        Text
2  text_id     Text ID   Unique ID, dependend of text
3  s           Sentence
4  article     article
5  article_n   number    dependent of article
6  section     section
7  section_n   number    dependent of section
8  chapter     chapter
9  chapter_n   number    dependent of chapter
10 signatures  signature


Warlaw tags on CQPweb production

Simple POS (Oxford Simplified Tagset)
Full USAS analysis (USAS tagset)
Lemma
Part-of-speech tag (C6 tagset)
Semantic tag (USAS tagset)
Tagged lemma
The primary word-level annotation scheme is: 	Part-of-speech tag 

Added an annotation template to the local server

indexing and adding metadata - I did the latter with "automatically run
frequence-list setup" and it's taking a very long time.

Remember: indexing a nontrivial corpus on the server requires the same
backend juggling which I did for obesity, but I have notes on that

PROGRESS: got sick of waiting for it and killed the browser

It's returning search results, but some of the KIC lines have "[UNREADABLE]"
messages, like the XML is broken or something

More notes - the bad text/text_ids were from missing newlines.

Steps:

CEQL bindings copying those on the production server

Build frequency tables and word counts separately

There are still a few discrepancies between the results in production and
on the laptop

Tooltips are not showing all of the metadata fields on my new one
