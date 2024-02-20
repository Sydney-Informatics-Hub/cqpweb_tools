# cqpweb_tools

Utilities for reindexing corpus files for CQPweb.

## check_newlines.py

Find corpus files which don't end in a newline (\\n) (this is redundant - 
corpus_rewrite.py now makes sure all rearranged corpus files end in a newline)

## corpus_precis.py

Scan a bunch of corpus files and pull out the article IDs based on a regexp

## corpus_rewrite.py

Utility for reordering a set of corpus files according to a spreadsheet which
has the old ids and new ids, and the order in which the texts should occur.

The corpus files are assumed to be in the format CQPweb uses, [VRT or
verticalised text](https://www.kielipankki.fi/support/vrt-format/). These
have one line per token (a word or punctuation mark). Each file can have
one or more texts, delimited by XML-style tags which look something like

    <text id="1856_Paris_DecRespectingMaritimeLaw">

(the files can have other XML-style tags for things like sentences and 
chapters within a text).

CQPweb returns its concordance results in the order in which the corpus files
were indexed and the order of the tokens within those files. I wrote
corpus_rewrite.py to fix a corpus whose texts needed to be rearranged into
a more correct order (in the case in point, by date).

corpus_rewrite.py needs a spreadsheet which contains one line for each text
in the corpus, with an old_id (matching the corpus file ids), a new_id (which
will be used in the reindexed corpus) and all of the metadata required for
the corpus. (CQPweb corpora have arbitrary metadata which is uploaded as a tsv
file.)

The spreadsheet rows should be in the order you want the corpus texts to be
indexed.

When you run the script, it reads all of the corpus files from the original
directory, separates them based on XML tags, tries to match the IDs to the
spreadsheet values, and writes them out as single files (one file per text)
with filenames which are guaranteed to be in the correct lexicographical order,
like:

    warlaw_001_1856_Paris_DecRespectingMaritimeLaw
    warlaw_002_1863_Geneva_ResolutionsGenevaIntlConf
    warlaw_003_1863_LeiberCode
    warlaw_004_1864_Geneva_ConventionforAmeliorationWou
    warlaw_005_1868_DecRenouncingProjectilesUnder400Gra
    warlaw_006_1868_Geneva_AdditionalArticlesRelatingCo
    warlaw_007_1874_Brussels_DecLawsCustomsofWar
    warlaw_008_1880_Oxford_LawsWarLand
    warlaw_009_1899_Hague_Conv_II__LawsCustomsWar
    warlaw_010_1899_Hague_ConventionAdaptionMaritimeWar
    warlaw_011_1899_Hague_Dec_IV2__AsphixiatingGases
    warlaw_012_1899_Hague_Dec_IV3__ExpandingBullets
    warlaw_013_1899_Hague_FinalActHaguePeaceConf
    warlaw_014_1899_Hague_LaunchProjectilesExplosivesBa

You can then concatenate these files into appropriate chunks ready to be
indexed on CQPweb, making sure that the chunked filenames are also in the
correct lexicographical order.

## frequency_check.py

Script to test whether the frequency list from an indexed corpus is the same
as the original, as a sanity check of whether reindexing worked.  The input
files are the text files as downloaded fro the frequency list page in CQPWeb.