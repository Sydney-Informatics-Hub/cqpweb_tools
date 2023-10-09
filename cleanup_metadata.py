#!/bin/env python

# clean up warlaw metadata

from openpyxl import load_workbook
import csv
import re
import sys

RAW_NOTEBOOK = "./treaties_2023.xlsx"

TSV_OUT = "./output.tsv"

def sanitise_metadata(cell):
    v = cell.value
    if v is None:
        return "null"
    return re.sub(r"[^A-Za-z0-9_]", "_", str(v))


wb = load_workbook(RAW_NOTEBOOK)
ws = wb.active
records = []
for row in ws:
    rec = [ sanitise_metadata(cell) for cell in row ]
    records.append(rec)

tsvwriter = csv.writer(sys.stdout, dialect="excel-tab")
for rec in records:
    if not rec[0] == "null" and not rec[0] == "Text ID":
        tsvwriter.writerow(rec)