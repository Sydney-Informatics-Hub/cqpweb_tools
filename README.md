# cqpweb-utils

Scripts for wrangling corpora and metadata files for CQPweb.

Writing some notes down so that I can remember what I was doing with this.

Problems which the reindex is supposed to fix:

* update the text IDs to match the 2023 spreadsheet
* make sure that the metadata .tsv matches values in the 2023 spreadsheet
* fix the ordering problem - CQPweb returns search results in corpus order -
  this is the order in which the corpus was indexed, by filename and then
  by order within the corpus. At first, I thought this only affected one
  text, 1949_2_Second_Geneva_Convention_WoundedS - which is at the end of the
  last corpus file. However, when checking the text ids, I found that there
  are ten or more such texts (the order in which they appear in the current
  corpus is different to the order in the spreadsheet)


I've already written a script which rewrites out the corpus with updated text
ids, this is corpus_text_id.py - its inputs are the 2023 spreadsheet.

This needs to be adapted so that it writes out the corpus in the order given
by the spreadsheet. At present, it makes a copy of the corpus in the same order
which it was originally found.

The current version uses a line-by-line approach and copies the filenames. The
new version needs to 

- read a textID and find the new mapped ID if one exisst
- either collect the rest of the text or write it out somewhere

A simple approach: write out each of the texts as a separate file with a 
filename giving the sequence (ie 1856_Paris_DecRespectingMaritimeLaw written
out as warlaw_001, etc)

Then reassemble these into bigger chunks which preserve the order.

