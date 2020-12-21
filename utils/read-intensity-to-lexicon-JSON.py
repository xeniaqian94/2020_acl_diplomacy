'''
-*- coding: utf-8 -*-
Copyright (C) 2020/12/19 
Author: Xin Qian

This script reads the three lexicon file in .txt, converts into a unified JSON file `hedging_lexicon.json`
Usage:

    python read-empathy-to-lexicon-JSON.py [threshold=default 0.5]

'''

import json
import sys
import csv

intensity_lexicon_obj = {"intensity": []}

threshold = 0.5 if len(sys.argv) == 1 else float(sys.argv[1])
with open("intensity_lexicon.txt", "r") as infile:
    reader = csv.reader(infile, delimiter='\t')
    next(reader)
    for rows in reader:
        k = str(rows[0])
        v = float(rows[2])
        if v > threshold:
            intensity_lexicon_obj['intensity'] += [k]

    print(intensity_lexicon_obj)

json.dump(intensity_lexicon_obj, open("intensity_lexicon.json", "w"), indent=2)
