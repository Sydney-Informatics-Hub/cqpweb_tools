#!/bin/env python

# clean up warlaw metadata

from openpyxl import load_workbook
import csv
import re
import sys

RAW_NOTEBOOK = "./data/warlaw_cqpweb_metadata.xlsx"

TSV_OUT = "./data/warlaw_cqpweb_metadata.tsv"


def sanitise_metadata(cell):
    v = cell.value
    if v is None:
        return "null"
    return re.sub(r"[^A-Za-z0-9_]", "_", str(v))


def main():
    wb = load_workbook(RAW_NOTEBOOK)
    ws = wb.active
    records = []
    for row in ws:
        rec = [sanitise_metadata(cell) for cell in row]
        records.append(rec)

    tsvwriter = csv.writer(sys.stdout, dialect="excel-tab")
    for rec in records:
        if not rec[0] == "null" and not rec[0] == "Text ID":
            tsvwriter.writerow(rec)


if __name__ == "__main__":
    main()
