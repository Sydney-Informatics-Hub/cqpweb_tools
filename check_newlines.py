
# check for newline at end of corpus text

from pathlib import Path

CORPUS_CHECK = 'corpus_reorder'

def check_end(fn):
    with open(fn, "r") as fh:
        text = fh.readlines()
        last = text[-1]
        if not ord(last[-1]) == 10:
            print(fn, ord(last[-1]))



files = list(Path(CORPUS_CHECK).glob("war*"))
files.sort()

for corpus_file in files:
    check_end(corpus_file)