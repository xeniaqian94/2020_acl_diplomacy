'''
-*- coding: utf-8 -*-
Copyright (C) 2020/12/22 
Author: Xin Qian

This script samples 10 cases each of cassandra (intended truth and perceived lie), and deceived (intended lie and perceived truth).
'''

import json
from os.path import join
from random import shuffle, sample


def print_cassandra_deceived_cases(gamefile):
    with open(gamefile) as inh:
        for ln in inh:
            conversation = json.loads(ln)

            # speaker score
            messages, sender_labels, receiver_labels = conversation['messages'], conversation['sender_labels'], \
                                                       conversation['receiver_labels']

            for idx, msg in enumerate(messages):
                if sender_labels[idx] and not receiver_labels[idx]:
                    print("cassandra", msg)
                if not sender_labels[idx] and receiver_labels[idx]:
                    print("deceived", msg)


if __name__ == '__main__':
    ROOT = 'data/'

    for file in ['train.jsonl', 'validation.jsonl', 'test.jsonl']:
        print_cassandra_deceived_cases(join(ROOT, file))
