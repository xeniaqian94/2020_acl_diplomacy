'''
-*- coding: utf-8 -*-
Copyright (C) 2020/12/22 
Author: Xin Qian

This script calculates word overlap in different lexicons
'''
import json

import itertools

lexicon_files = ["harbinger_lexicon.json", "hedging_lexicon.json", "empathy_lexicon.json", "intensity_lexicon.json",
                 "NRC-VAD-Lexicon.json"]

word_list = {}
# get word count
for file in lexicon_files:
    # print(file)
    jobject = json.load(open(file, "r"))

    if file != "NRC-VAD-Lexicon.json":
        word_list[file] = sum(jobject.values(), [])
    else:
        for which_of_vad in jobject:
            word_list[which_of_vad] = jobject[which_of_vad]

for key in word_list:
    print(key, len(word_list[key]))

# calculate overlap

for key1, key2 in itertools.permutations(list(word_list.keys()), 2):
    print(key1, key2, len(set(word_list[key1]).intersection(set(word_list[key2]))) * 1.0 / len(set(word_list[key1])))
