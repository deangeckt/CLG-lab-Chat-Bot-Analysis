import pandas as pd
from collections import defaultdict
import json
import os
import numpy as np
from app.pages.common.versions import experiments_short_names, root_folder

experiments = ['Baseline', 'Random CS', 'Short-context CS', 'Adversarial CS', 'Alignment CS']

def is_in_nouns(nouns_names, map_idx, uter_text, lang):
    if uter_text.endswith(('!', '.', '?')):
        uter_text = uter_text[:len(uter_text)-1]

    nouns = nouns_names[map_idx][lang]
    tokens = uter_text.split(' ')
    tokens_in = [token in nouns for token in tokens]
    if not any(tokens_in):
        return -1

    amount_of_tokens_in = sum(tokens_in)
    tokens = np.array(tokens)
    tokens_in = np.array(tokens_in)
    tokens_in = list(tokens[tokens_in])
    print(f'map:{map_idx}:{uter_text} - {amount_of_tokens_in}: {tokens_in}')
    return amount_of_tokens_in

def read_games_data():
    nouns_names = defaultdict(lambda: dict[str, list])
    for i in range(1, 5):
        df = pd.read_csv(f'offline/nouns/map_{i}_names.csv', encoding='utf-8')
        dict_data = {'eng': list(df['eng']), 'es': list(df['es'])}
        nouns_names[i] = dict_data

    amounts_of_tokens_in = []
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
            role = game_data['config']['game_role']
            human_uters = list(filter(lambda e: e['id'] != role, game_data['chat']))

            for uter in human_uters:
                if uter['lang'] == 'none':
                    continue
                elif uter['lang'] == 'mix':
                    amount = is_in_nouns(nouns_names, map_idx, uter['msg'], 'eng')
                    amount += is_in_nouns(nouns_names, map_idx, uter['msg'], 'es')
                else:
                    amount = is_in_nouns(nouns_names, map_idx, uter['msg'], uter['lang'])

                if amount > 0:
                    amounts_of_tokens_in.append(amount)
                else:
                    num_of_sentences_without_nouns += 1

    num_of_sentences_with_nouns = len(amounts_of_tokens_in)
    mean_num_of_nouns_per_sent = np.mean(amounts_of_tokens_in)
    print()
    print('num_of_sentences_with_nouns:', num_of_sentences_with_nouns)
    print('num_of_sentences_without_nouns:', num_of_sentences_without_nouns)
    print('mean_num_of_nouns_per_sent:', mean_num_of_nouns_per_sent)


if __name__ == '__main__':
    """
    run from root repo
    """
    read_games_data()