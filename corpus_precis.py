# summarise a VRT corpus file

from pathlib import Path
import re

TOKENS = 10

ARTICLE_RE = re.compile(r'^<article n="(\d+)"/>')

def precis_by_article(filename, outfh):
    lines = 0
    with open(filename, "r") as fh:
        summarising = 0
        precis = ""
        n = None
        for line in fh:
            lines += 1
            if m := ARTICLE_RE.match(line):
                n = m.group(1)
                precis = ""
                summarising = 10
                ln = lines
            else:
                if summarising > 0:
                    bits = re.split(r'\s+', line)
                    precis += " " + bits[0]
                    summarising -= 1
                    if summarising == 0:
                        outfh.write(f"Article {n} {ln}: {precis}\n")


CORPUS_ORIG = 'corpus_orig/warlaw/'
PRECIS_DIR = 'precis/'

for corpus_file in Path(CORPUS_ORIG).glob("war*"):
    safe_txt = Path(corpus_file.name.replace(".", "_")).with_suffix('.txt')
    precis_file = Path(PRECIS_DIR) / safe_txt
    print(corpus_file, precis_file)
    with open(precis_file, 'w') as pfh:
        precis_by_article(corpus_file, pfh)