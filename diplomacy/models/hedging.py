'''
-*- coding: utf-8 -*-
Copyright (C) 2020/12/19
Author: Xin Qian

This script is largely the same as `harbringers.py`,
except on line 56 (lexicon file) and ~line79 (non-unigram feature based on hedging_lexicon.json) -> TODO

Usage:
    TODO

'''

# BoW Version
import jsonlines
import json
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.feature_selection import RFE
import numpy as np
from sklearn.preprocessing import StandardScaler
import spacy
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
import sys
import warnings

warnings.filterwarnings("ignore")


def spacy_tokenizer(text):
    tokens = [tok.text for tok in nlp(text)]
    return tokens, " ".join(tokens)


# change the format from list of lists into a single list
def aggregate(dataset):
    messages = []
    rec = []
    send = []
    power = []
    for dialogs in dataset:
        messages.extend(dialogs['messages'])
        rec.extend(dialogs['receiver_labels'])
        send.extend(dialogs['sender_labels'])
        # ONLY FOR POWER VERSION
        power.extend(dialogs['game_score_delta'])
    # print(len(rec), len(send), len(messages))
    merged = []
    for i, item in enumerate(messages):
        merged.append({'message': item, 'sender_annotation': send[i], 'receiver_annotation': rec[i],
                       'score_delta': int(power[i])})
    return merged


def convert_to_binary(dataset, lexicon_file):
    binary_data = []
    matrix = []

    ## TODO: convert utils/hedging-resources-master/booster_words.txt etc. into JSON format, than change the line below
    with open(lexicon_file) as f:
        feature_dict = json.load(f)# json.loads(f.readline())
    feature_dict['but'] = ['but']
    feature_dict['countries'] = ['austria', 'england', 'france', 'germany', 'italy', 'russia', 'turkey']

    for message in dataset:
        # drop the instances that were not annotated
        if message['receiver_annotation'] == True or message['receiver_annotation'] == False:
            pass
        else:
            if TASK == "SENDER":
                pass
            elif TASK == "RECEIVER":
                continue

        binary = []
        # add features

        # loop through each message, then for each feature group.  If word in message matches the dictionary, add binary feature
        for feature in feature_dict.keys():
            feature_flag = False
            preprocessed_message_tokens, preprocessed_message_concatenated = spacy_tokenizer(message['message'].lower())
            total = 0
            for word_or_phrase in feature_dict[feature]:
                if (word_or_phrase in preprocessed_message_tokens) or (
                        " " in word_or_phrase and word_or_phrase in preprocessed_message_concatenated):
                    total += 1
                    feature_flag = True
                    # if feature == "discourse_markers":
                    #     print("Matching a discourse_markers feature", word_or_phrase, preprocessed_message_concatenated)
            # break
            if feature_flag:
                binary.append(total)
            else:
                binary.append(0)

        # a severe power skew (a difference of 5 or more supply centers) has the best result
        if POWER == "y":
            if message['score_delta'] > 4:
                binary.append(1)
            else:
                binary.append(0)

            if message['score_delta'] < -4:
                binary.append(1)
            else:
                binary.append(0)

        if TASK == "SENDER":
            annotation = 'sender_annotation'
        elif TASK == "RECEIVER":
            annotation = 'receiver_annotation'

        # add class label
        if message[annotation] == False:
            binary.append(0)
        else:
            binary.append(1)

        binary_data.append(binary)
    return binary_data


# split up x and y label in data
def split_xy(data):
    X, y = [], []
    for line in data:
        x = line[:len(line) - 1]
        single_y = line[len(line) - 1]
        X.append(x)
        y.append(single_y)
    return (X, y)


def log_reg(train, test, lexicon_file):
    if TASK == "SENDER":
        corpus = [message['message'].lower() for message in aggregate(train)]
    elif TASK == "RECEIVER":  # for receivers, drop all missing annotations
        corpus = [message['message'].lower() for message in aggregate(train) if
                  message['receiver_annotation'] != "NOANNOTATION"]

    # only used for getting lie/not lie labels
    train = convert_to_binary(aggregate(train), lexicon_file)
    # validation set not used for consistency with neural
    test = convert_to_binary(aggregate(test), lexicon_file)
    train = split_xy(train)
    test = split_xy(test)

    # code to scale features, if power is added as a raw value, not binary feature.  Doesn't help but best practice
    scaler = StandardScaler()
    train_scaled = scaler.fit_transform(train[0])
    test_scaled = scaler.fit_transform(test[0])

    # balanced class weight is important, since otherwise it will only learn majority class
    logmodel = LogisticRegression(class_weight='balanced', max_iter=1000)

    # RFE VERSION.  Doesn't improve results
    #    rfe = RFE(logmodel, n_features_to_select = 1000, step = 100, verbose = 1)
    #    rfe = rfe.fit(train_scaled, train[1])
    #    print(rfe.support_)
    #    print(rfe.ranking_)
    #    predictions = rfe.predict(test_scaled)
    #    print(rfe.score(test_scaled, test[1]))
    #    print(classification_report(test[1],predictions))

    logmodel.fit(train_scaled, train[1])
    predictions = logmodel.predict(test_scaled)
    print(classification_report(test[1], predictions, digits=3))


if __name__ == '__main__':
    if len(sys.argv) == 4:
        POWER = "y"
        if sys.argv[1] == 's':
            TASK = "SENDER"
        elif sys.argv[1] == 'r':
            TASK = "RECEIVER"
        else:
            print("Specify s for sender or r for receiver")
            exit()

        if sys.argv[2] == 'n':
            POWER = sys.argv[2]
        elif sys.argv[2] == 'y':
            POWER = sys.argv[2]
        else:
            print("Specify y for including power and n for not including it e.g.: python bagofwords.py s n")
            exit()
        lexicon_file = sys.argv[3]
    else:
        print("Specify s for sender or r for receiver e.g.:  python harbringers.py s")
        exit()

    data_path = 'data/'

    with jsonlines.open(data_path + 'train.jsonl', 'r') as reader:
        train = list(reader)
    # VAL NOT USED IN LOG REG FOR CONSISTENCY WITH NEURAL
    # with jsonlines.open(data_path+'validation.jsonl', 'r') as reade
    # dev = list(reader)
    with jsonlines.open(data_path + 'test.jsonl', 'r') as reader:
        test = list(reader)

    # spacy used for tokenization
    nlp = English()

    log_reg(train, test, lexicon_file)
