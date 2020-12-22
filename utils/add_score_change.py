import json
from os.path import join
from random import shuffle, sample

season_id = {
    "Spring": 0,
    "Fall": 1, "Winter": 2
}

global score_dict
score_dict = dict()


def insert_key_value(score_dict, key, value):
    if key in score_dict and value != score_dict[key]:
        print("ALERT, key and old value not consistent", key, value)


def recover_score_change(gamefile):
    unique_games = set()
    score_dict = dict()

    with open(gamefile) as inh:
        for ln in inh:
            conversation = json.loads(ln)
            print(conversation.keys())

            # speaker score
            speakers, game_id, years, seasons, game_scores = conversation['speakers'], conversation['game_id'], \
                                                             conversation['years'], \
                                                             conversation['seasons'], conversation['game_score']

            for idx in range(len(speakers)):
                insert_key_value(score_dict, (game_id, years[idx], seasons[idx], speakers[idx]), game_scores[idx])

            # receiver score
            receivers, game_id, years, seasons, game_scores, score_deltas = conversation['speakers'], conversation[
                'game_id'], \
                                                                            conversation['years'], \
                                                                            conversation['seasons'], conversation[
                                                                                'game_score'], conversation[
                                                                                'game_score_delta']

            for idx in range(len(receivers)):
                insert_key_value(score_dict, (game_id, years[idx], seasons[idx], receivers[idx]),
                                 game_scores[idx] - score_deltas[idx])

            unique_games.add(game_id)

    sorted_score_key = sorted([key_tuple for key_tuple in list(score_dict.keys())],
                              key=lambda key_tuple: (key_tuple[0], key_tuple[3], key_tuple[1], season_id[key_tuple[2]]),
                              reverse=False)
    print(sorted_score_key)
    print("unique_games for this file", unique_games)

    #         for msg, sender_label, receiver_label, score_delta \
    #             in zip(conversation['messages'],conversation['sender_labels'], \
    #                 conversation['receiver_labels'], conversation['game_score_delta']):
    #             messages.append({'message': msg, 'receiver_annotation': receiver_label,\
    #                 'sender_annotation':sender_label, 'score_delta': int(score_delta)})
    # shuffle(messages)
    # return messages


# def write_single_messages(messages, outfile):
#     with open(outfile, "w") as outh:
#         for msg in messages:
#             outh.write(json.dumps(msg)+'\n')

if __name__ == '__main__':
    ROOT = 'data/'

    for file in ['train.jsonl', 'train.jsonl', 'train.jsonl']:
        recover_score_change(join(ROOT, 'train.jsonl'))

    # to_single_message_format(join(ROOT, 'validation.jsonl')),
    #                                                     join(ROOT, 'validation_sm.jsonl'))
    # write_single_messages(to_single_message_format(join(ROOT, 'train.jsonl')),
    #                                                     join(ROOT, 'train_sm.jsonl'))
    # write_single_messages(to_single_message_format(join(ROOT, 'test.jsonl')),
    #                                                     join(ROOT, 'test_sm.jsonl'))
