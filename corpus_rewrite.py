# update text ids in a directory of corpus VRT files - writes out a full
# copy of each file
# 

from pathlib import Path
import re
import logging
from openpyxl import load_workbook
import sys
import re
import csv


LOGLEVEL = logging.INFO
LOGDIR = "./logs"

logger = logging.getLogger(__name__)

logger.setLevel(LOGLEVEL)
logch = logging.StreamHandler()
logch.setLevel(LOGLEVEL)
logger.addHandler(logch)
logfh = logging.FileHandler(Path(LOGDIR) / "corpus_text_id.log")
logfh.setLevel(LOGLEVEL)
logger.addHandler(logfh)

CORPUS_ORIG = "corpus_orig"
CORPUS_REMAPPED = "corpus_reorder"

METADATA_EXCEL = "data/warlaw_metadata_2023.xlsx"
TSV_OUT = "data/warlaw_cqpweb_metadata.tsv"


COL_NEW_ID = 1 # 'B'
COL_OLD_ID = 8 # 'I'
TRUNCATE_TO = 40
TEXT_ID_RE = re.compile(r'(<text id=")([^\"]*)(">.*)')
MAP_COLS = [ 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17 ]

def sanitise_metadata(cell):
    v = cell.value
    if v is None:
        return "null"
    return re.sub(r"[^A-Za-z0-9_]", "_", str(v))


def load_id_mappings(excelfile):
    wb = load_workbook(excelfile)
    ws = wb.active
    mappings = {}
    n = 1
    records = []
    for row in ws.iter_rows():
        new_id = sanitise_metadata(row[COL_NEW_ID])
        old_id = row[COL_OLD_ID].value
        if not new_id is None and not old_id is None:
            if new_id != 'Text ID':
                if TRUNCATE_TO:
                    if len(old_id) > TRUNCATE_TO:
                        logger.warn(f"Corpus id {old_id} is > 40 chars")
                    new_id = new_id[:TRUNCATE_TO]
                mappings[old_id] = ( new_id, n )
                logger.info(f"map old {old_id} to new {new_id} {n}")
                n += 1
        cleaned = [ sanitise_metadata(cell) for cell in row ]
        records.append([ new_id ] + [ cleaned[c] for c in MAP_COLS ])
    print(f"Writing tsv metadata to {TSV_OUT}")
    with open(TSV_OUT, "w") as tsvh:
        tsvwriter = csv.writer(tsvh, dialect="excel-tab")
        for rec in records:
            if not rec[0] == "null" and not rec[0] == "Text ID":
                tsvwriter.writerow(rec)
    return mappings

def convert_ids(mappings, cfh):
    for line in cfh:
        if m := TEXT_ID_RE.match(line):
            prefix = m.group(1)
            old_id = m.group(2)
            suffix = m.group(3)
            if not old_id in mappings:
                logger.warn(f"Warning: id {old_id} in {corpus_file} not in spreadsheet")
                yield line
            else:
                new_id = mappings[old_id]
                new_line = f"{prefix}{new_id}{suffix}\n"
                yield new_line
        else:
            yield line


def convert_file(mappings, orig_file, new_file):
    with open(new_file, "w") as nfh:
        with open(orig_file, "r") as ofh:
            for newline in convert_ids(mappings, ofh):
                nfh.write(newline)


def check_ids(mappings, orig_file):
    n = 0
    old_ids = mappings.keys()
    new_ids = mappings.values()
    with open(orig_file, "r") as ofh:
        for line in ofh:
            if m := TEXT_ID_RE.match(line):
                old_id = m.group(2)
                found_old = old_id in old_ids
                found_new = old_id in new_ids
                print(f"{n},{old_id},{found_old},{found_new}")
            n += 1


def write_temp_text(target_dir, n, new_id, content):
    new_file = target_dir / Path(f"warlaw_{n:03d}_{new_id}")
    logger.info(f"Writing {new_file}")
    with open(new_file, "w") as nfh:
        nfh.write(content)
        # ensure all corpus text files end with a newline
        if not ord(content[-1]) == 10:
            nfh.write("\n")


mappings = load_id_mappings(METADATA_EXCEL)

files = list(Path(CORPUS_ORIG).glob("war*"))
files.sort()

target_dir = Path(CORPUS_REMAPPED)
target_dir.mkdir(parents=True, exist_ok=True)

i = 1

for corpus_file in files:
    contents = ""
    new_id = None
    with open(corpus_file) as ofh:
        for line in ofh:
            if m := TEXT_ID_RE.match(line):
                prefix = m.group(1)
                old_id = m.group(2)
                suffix = m.group(3)
                if not old_id in mappings:
                    logger.error(f"Warning: id {old_id} in {corpus_file} not in spreadsheet")
                    sys.exit(-1)
                if new_id is not None:
                    write_temp_text(target_dir, i, new_id, content)
                    i += 1
                ( new_id, n ) = mappings[old_id]
                content = f"{prefix}{new_id}{suffix}\n"
            else:
                content += line
    if new_id is not None:
        write_temp_text(target_dir, i, new_id, content)
        i += 1


#    new_file = target_dir / corpus_file.name
    # logger.info(f"{corpus_file} => {new_file}")
    # convert_file(mappings, corpus_file, new_file)
