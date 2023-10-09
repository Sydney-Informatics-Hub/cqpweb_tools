# update text ids in a directory of corpus VRT files - writes out a full
# copy of each file
# 

from pathlib import Path
import re
import json
import logging
from openpyxl import load_workbook

LOGLEVEL = logging.INFO

logger = logging.getLogger(__name__)

logger.setLevel(LOGLEVEL)
logch = logging.StreamHandler()
logch.setLevel(LOGLEVEL)
logger.addHandler(logch)


CORPUS_ORIG = "corpus_orig"
CORPUS_REMAPPED = "corpus_remapped"

METADATA_EXCEL = "List of treaties_CQWEBMetadata_UPDATED2023.xlsx"

COL_NEW_ID = 1 #'B'
COL_OLD_ID = 6 # 'G'
TEXT_ID_RE = re.compile(r'<text id="([^\"]*)">')
TEXT_ID_TEMPLATE = '<text id="{id}">'

def load_id_mappings(excelfile):
    wb = load_workbook(excelfile)
    ws = wb.active
    mappings = {}
    for row in ws.iter_rows():
        new_id = row[COL_NEW_ID].value
        old_id = row[COL_OLD_ID].value
        if new_id and new_id != 'Text ID':
            mappings[old_id] = new_id
    return mappings

def convert_ids(mappings, cfh):
    for line in cfh:
        if m := TEXT_ID_RE.match(line):
            old_id = m.group(1)
            if not old_id in mappings:
                logger.warn(f"Warning: id {old_id} in {corpus_file} not in spreadsheet")
                yield line
            else:
                new_id = mappings[old_id]
                yield TEXT_ID_TEMPLATE.format(id=new_id)
        else:
            yield line


def convert_file(mappings, orig_file, new_file):
    with open(new_file, "w") as nfh:
        with open(orig_file, "r") as ofh:
            for newline in convert_ids(mappings, ofh):
                nfh.write(newline)


mappings = load_id_mappings(METADATA_EXCEL)

print(json.dumps(mappings, indent=2))

for corpus_file in Path(CORPUS_ORIG).glob("war*"):
    new_file = Path(CORPUS_REMAPPED) / corpus_file.name
    logger.info(f"{corpus_file} => {new_file}")
    convert_file(mappings, corpus_file, new_file)
