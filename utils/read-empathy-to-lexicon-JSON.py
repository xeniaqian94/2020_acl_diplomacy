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

empathy_lexicon_obj = {"empathy": []}

threshold = 4.0 if len(sys.argv)==1 else float(sys.argv[1])
with open("empathy_lexicon.txt", "r") as infile:
    reader = csv.reader(infile)
    next(reader)
    for rows in reader:
        k = str(rows[0])
        v = float(rows[1])
        if v > threshold:
            empathy_lexicon_obj['empathy'] += [k]

    print(empathy_lexicon_obj)

json.dump(empathy_lexicon_obj, open("empathy_lexicon.json", "w"), indent=2)
