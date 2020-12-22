'''
-*- coding: utf-8 -*-
Copyright (C) 2020/12/19 
Author: Xin Qian

This script reads the lexicon file in .txt, converts into a unified JSON file `NRC-VAD-Lexicon.json`
Usage:

    python read-VAD-to-lexicon-JSON.py [threshold=default 0.5]

'''

import json
import sys
import csv

vad_lexicon_obj = {"V": [], "A": [], "D": []}

threshold = 0.5 if len(sys.argv) == 1 else float(sys.argv[1])
with open("NRC-VAD-Lexicon.txt", "r") as infile:
    reader = csv.reader(infile, delimiter='\t')
    next(reader)
    for rows in reader:
        k = str(rows[0])

        v = float(rows[1])
        if v > threshold:
            vad_lexicon_obj['V'] += [k]

        a = float(rows[2])
        if a > threshold:
            vad_lexicon_obj['A'] += [k]

        d = float(rows[3])
        if d > threshold:
            vad_lexicon_obj['D'] += [k]

    print(vad_lexicon_obj)

json.dump(vad_lexicon_obj, open("NRC-VAD-Lexicon.json", "w"), indent=2)
