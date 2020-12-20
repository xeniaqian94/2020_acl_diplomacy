'''
-*- coding: utf-8 -*-
Copyright (C) 2020/12/19 
Author: Xin Qian

This script reads the three lexicon file in .txt, converts into a unified JSON file `hedging_lexicon.json`
Usage:

    python read-hedging-to-lexicon-JSON.py

'''


import json

hedging_lexicon_obj = {}

for hedging_subgroup in ['booster_words', 'discourse_markers', 'hedge_words']:
    f = open("hedging-resources-master/" + hedging_subgroup + ".txt", "r")
    hedging_lexicon_obj[hedging_subgroup] = []
    for line in f.readlines():
        if len(line.strip()) > 0 and line[0]!="#":
            hedging_lexicon_obj[hedging_subgroup] += [line.strip()]

json.dump(hedging_lexicon_obj, open("hedging_lexicon.json", "w"), indent=2)
