import pandas as pd
from collections import defaultdict
import json
import os
import numpy as np
from app.pages.common.versions import experiments_short_names, root_folder

experiments = ['Baseline', 'Random CS', 'Short-context CS', 'Adversarial CS', 'Alignment CS']

def clean_endings(token: str):
    if token.endswith(('!', '.', '?', '¿')):
        return token[:len(token)-1]
    return token

def is_in_nouns(nouns_names, map_idx, uter_text, lang):
    nouns = nouns_names[map_idx][lang]
    tokens = uter_text.split(' ')
    tokens = [clean_endings(t) for t in tokens]
    tokens_in = [token in nouns for token in tokens]
    if not any(tokens_in):
        return -1, -1

    amount_of_tokens_in = sum(tokens_in)
    tokens = np.array(tokens)
    tokens_in = np.array(tokens_in)
    actual_tokens_in = list(tokens[tokens_in])

    cognates = np.array(nouns_names[map_idx]['cg'])
    if len(cognates):
        cognates_in = [cognates[nouns.index(token)] for token in actual_tokens_in]
        amount_of_cognates_in = sum(cognates_in)
    else:
        amount_of_cognates_in = -1
    print(f'map: {map_idx} - {uter_text} ({lang}) - {amount_of_tokens_in} - {actual_tokens_in}')
    return amount_of_tokens_in, amount_of_cognates_in

def read_games_data():
    nouns_names = {}
    for i in range(1, 5):
        df = pd.read_csv(f'offline/nouns/map_{i}_names.csv', encoding='utf-8')
        cognates_list = list(df['is_cognate']) if 'is_cognate' in df else []
        nouns_names[i] = {'eng': list(df['eng']), 'es': list(df['es']), 'cg': cognates_list}

    amounts_of_tokens_in = []
    amounts_of_cg_tokens_in = []
    num_of_sentences_without_nouns = 0

    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')
        data = json.load(json_file)

        version = data['server_version']
        experiment = experiments_short_names.get(version, 'err')
        if experiment not in experiments:
            continue

        for idx, game_data in enumerate(data['games_data']):
            map_idx = idx + 1
            # control map here
            if map_idx != 1:
                continue

            role = game_data['config']['game_role']

            # control human / bot here
            human_uters = list(filter(lambda e: e['id'] != role, game_data['chat']))

            for uter in human_uters:
                if uter['lang'] == 'none':
                    continue
                elif uter['lang'] == 'mix':
                    en_amount, en_cg_amount = is_in_nouns(nouns_names, map_idx, uter['msg'], 'eng')
                    es_amount, es_cg_amount = is_in_nouns(nouns_names, map_idx, uter['msg'], 'es')
                    amount = en_amount + es_amount
                    cg_amount = en_cg_amount + es_cg_amount
                else:
                    amount, cg_amount = is_in_nouns(nouns_names, map_idx, uter['msg'], uter['lang'])

                if amount > 0:
                    amounts_of_tokens_in.append(amount)
                else:
                    num_of_sentences_without_nouns += 1

                if cg_amount > 0:
                    amounts_of_cg_tokens_in.append(cg_amount)


    num_of_sentences_with_nouns = len(amounts_of_tokens_in)
    num_of_sentences_with_cg_nouns = len(amounts_of_cg_tokens_in)
    mean_num_of_nouns_per_sent = np.mean(amounts_of_tokens_in)

    print()
    print('num_of_sentences_with_nouns:', num_of_sentences_with_nouns)
    print('num_of_sentences_without_nouns:', num_of_sentences_without_nouns)
    print('mean_num_of_nouns_per_sent:', mean_num_of_nouns_per_sent)
    print('num_of_sentences_with_cognates_nouns:', num_of_sentences_with_cg_nouns)


if __name__ == '__main__':
    """
    run from root repo
    """
    read_games_data()