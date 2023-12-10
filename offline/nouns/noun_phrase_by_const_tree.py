import os
import json
import stanza
import nltk
from app.pages.common.versions import experiments_short_names, root_folder
import numpy as np

debug_print = False
experiments = ['Baseline', 'Random CS', 'Short-context CS', 'Adversarial CS', 'Alignment CS']

def is_eng_valid_np(root):
    if type(root) != nltk.tree.Tree:
        return False
    if root.label() != 'NP':
        return False
    if root.height() != 3:
        return False
    for token in root:
        if token.label() == 'NN':
            return True
    return False


def is_es_noun_exist(root):
    if type(root) != nltk.tree.Tree:
        return False
    if root.label() == 'NOUN':
        return True
    for child in root:
        if is_es_noun_exist(child):
            return True
    return False

def is_es_valid_np(root):
    if type(root) != nltk.tree.Tree:
        return False
    if root.label() != 'sn':
        return False

    return is_es_noun_exist(root)


def extract_english_noun_phrases(root, nouns, depth):
    if type(root) != nltk.tree.Tree:
        return
    for child in root:
        tab_str = depth * '\t'
        if is_eng_valid_np(child):
            if debug_print:
                print(f'{tab_str}{child}')
            nouns.append(' '.join(child.leaves()))
        extract_english_noun_phrases(child, nouns, depth + 1)


def extract_spanish_noun_phrases(root, nouns, depth):
    if type(root) != nltk.tree.Tree:
        return
    for child in root:
        tab_str = depth * '\t'
        if is_es_valid_np(child):
            if debug_print:
                print(f'{tab_str}{child}')
            nouns.append(' '.join(child.leaves()))
        extract_spanish_noun_phrases(child, nouns, depth + 1)


def extract_noun_phrase(text, lang):
    # TODO: run time improvement - check if 'NP' and 'NN' in str(root), if not - no need to recur
    if lang == 'eng':
        return 0
    nlp = en_nlp if lang == 'eng' else es_nlp
    foo = extract_english_noun_phrases if lang == 'eng' else extract_spanish_noun_phrases

    doc = nlp(text)
    sentence = doc.sentences[0]
    root = nltk.tree.Tree.fromstring(str(sentence.constituency))
    nouns = []
    foo(root, nouns, 0)
    if nouns:
        print(f'{text} ({lang}) - {nouns}')
    return len(nouns)


def read_games_data():
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
                    continue
                    # en_amount = extract_noun_phrase(uter['msg'], 'eng')
                    # es_amount = extract_noun_phrase(uter['msg'], 'es')
                    # amount = en_amount + es_amount
                else:
                    amount = extract_noun_phrase(uter['msg'], uter['lang'])

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
    en_nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,constituency')
    es_nlp = stanza.Pipeline(lang='es', processors='tokenize,pos,constituency')

    # read_games_data()

    ## mistakes
    es_text = ['bien, me dirigo a la roca cerca del tigre y avanzo al palito',
               '¿cuál es el siguiente paso después del amigo sapo?',
               "genial, ahora estoy en la isla con el loro y el elefante"]
    # en_text = [
    #            "i'm on it, mate",
    #            ]
    # for text in en_text:
    #     extract_noun_phrase(text, 'eng')
    for text in es_text:
        extract_noun_phrase(text, 'es')
