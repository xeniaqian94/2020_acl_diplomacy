'''
This script adds a new field to the train/val/test.json file

Usage:

    python add_score_change.py


'''
import json
from os.path import join
from random import shuffle, sample

season_id = {
    "Spring": 0,
    "Fall": 1, "Winter": 2
}


def recover_score_change(gamefile):
    score_dict = dict()

    def insert_key_value(key, value):
        if key in score_dict and value != score_dict[key]:
            print("ALERT, key and old value not consistent", key, value, "old", score_dict[key])
        score_dict[key] = value

    unique_games = set()
    score_dict = dict()

    with open(gamefile) as inh:
        for ln in inh:
            conversation = json.loads(ln)

            # speaker score
            speakers, game_id, years, seasons, game_scores = conversation['speakers'], conversation['game_id'], \
                                                             conversation['years'], \
                                                             conversation['seasons'], conversation['game_score']

            for idx in range(len(speakers)):
                insert_key_value((game_id, years[idx], seasons[idx], speakers[idx]), int(game_scores[idx]))

            # receiver score
            receivers, game_id, years, seasons, game_scores, score_deltas = conversation['receivers'], conversation[
                'game_id'], \
                                                                            conversation['years'], \
                                                                            conversation['seasons'], conversation[
                                                                                'game_score'], conversation[
                                                                                'game_score_delta']

            for idx in range(len(receivers)):
                insert_key_value((game_id, years[idx], seasons[idx], receivers[idx]),
                                 (int(game_scores[idx]) - int(score_deltas[idx])))

            unique_games.add(game_id)

    sorted_score_key = sorted([key_tuple for key_tuple in list(score_dict.keys())],
                              key=lambda key_tuple: (key_tuple[0], key_tuple[3], key_tuple[1], season_id[key_tuple[2]]),
                              reverse=False)
    # print(sorted_score_key)
    print("unique_games for this file", unique_games)

    #         for msg, sender_label, receiver_label, score_delta \
    #             in zip(conversation['messages'],conversation['sender_labels'], \
    #                 conversation['receiver_labels'], conversation['game_score_delta']):
    #             messages.append({'message': msg, 'receiver_annotation': receiver_label,\
    #                 'sender_annotation':sender_label, 'score_delta': int(score_delta)})
    # shuffle(messages)
    # return messages

    score_change_dict = dict()
    for tuple in score_dict:
        print(
            "prev tuple", sorted_score_key[sorted_score_key.index(tuple) - 1] if (
                    tuple[1] != '1901' or tuple[2] != 'Fall') else 0, "current tuple",
            tuple)
        score_change_dict[tuple] = score_dict[tuple] - (
            score_dict[sorted_score_key[sorted_score_key.index(tuple) - 1]] if (
                    tuple[1] != '1901' or tuple[2] != 'Fall') else 0)
    return score_change_dict


def write_score_change(outfile, gamefile, score_change_dict):
    with open(outfile, "w") as outh:
        with open(gamefile) as inh:
            for ln in inh:
                conversation = json.loads(ln)

                # speaker score
                speakers, game_id, years, seasons, game_scores = conversation['speakers'], conversation['game_id'], \
                                                                 conversation['years'], \
                                                                 conversation['seasons'], conversation['game_score']

                conversation['game_score_change'] = [
                    score_change_dict[(game_id, years[idx], seasons[idx], speakers[idx])] for idx in
                    range(len(speakers))]

                outh.write(json.dumps(conversation) + '\n')


if __name__ == '__main__':
    ROOT = 'data/'

    for file in ['train.jsonl', 'validation.jsonl', 'test.jsonl']:
        write_score_change(join(ROOT, file).replace(".", ".power."), join(ROOT, file), recover_score_change(join(ROOT, file)))

        # to_single_message_format(join(ROOT, 'validation.jsonl')),
        #                                                     join(ROOT, 'validation_sm.jsonl'))
        # write_single_messages(to_single_message_format(join(ROOT, 'train.jsonl')),
        #                                                     join(ROOT, 'train_sm.jsonl'))
        # write_single_messages(to_single_message_format(join(ROOT, 'test.jsonl')),
        #                                                     join(ROOT, 'test_sm.jsonl'))
