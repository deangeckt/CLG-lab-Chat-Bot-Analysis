import numpy as np
import pandas as pd
import json
import os
from lingua import Language, LanguageDetectorBuilder
from collections import defaultdict
import itertools

from tqdm import tqdm

root_folder = r"../data/prolific/"
output_folder = r'../data/prolific_lang_ids'
global_cs_counter=0

def pred_lang_token(token: str):
    confidence_values  = detector.compute_language_confidence_values(token)
    simple_list = [(v.value, v.language) for v in confidence_values]
    conf, lng = max(simple_list)
    return conf, lng



def run_on_dataset():
    global global_cs_counter
    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')

        if os.path.exists(os.path.join(output_folder, file_name)):
            print(f'skip: {file_name}')
            continue

        data = json.load(json_file)
        for game in data['games_data']:
            chat = game['chat']
            for chat_ele in chat:
                uter = chat_ele['msg']
                uter_lng = custom_pred_lang_sentence(uter)

                tokens = uter.split(' ')

                words = []
                for token in tokens:
                    conf, lang = pred_lang_token(token)
                    lang = 'eng' if lang == Language.ENGLISH else 'es'
                    words.append({'token': token, 'lang': lang, 'conf': conf})

                chat_ele['words'] = words
                chat_ele['lang'] = uter_lng

                # if uter_lng == 'mix':
                #     print(f'__{uter}__')
                #     global_cs_counter = global_cs_counter + 1

        with open(os.path.join(output_folder, file_name), 'w') as f:
            json.dump(data, f)

def print_deubg(text: str):
    print(text, pred_lang_token(text))
    for token in text.split(' '):
        print(token, pred_lang_token(token))
    print()


def pred_lang_sentence(sentence: str):
    """
    still not 100% solution
    """
    result = detector.detect_multiple_languages_of(sentence)
    if len(result) == 1:
        return 'eng' if result[0].language == Language.ENGLISH else 'es'
    else:
        return 'mix'


def has_switch(lst):
    # for key, iter in itertools.groupby(lst):
    #     print((key, len(list(iter))))
    seq_th = 2
    is_valid = {1: False, 0: False}
    for key, iter in itertools.groupby(lst):
        count = len(list(iter))
        if count >= seq_th:
            is_valid[key] = True
    return all(list(is_valid.values()))


#0.71 th -> 29 mixed, all are valid!
#0.7 th -> 45 mixed, FP mistakes: eng:16

def custom_pred_lang_sentence(sentence: str):
    """
    uses word-lvl predication and goes through the sequence
    """
    preds = [pred_lang_token(token) for token in sentence.split(' ')]
    conf_preds = list(filter(lambda x: x[0] > 0.71, preds))
    if len(conf_preds) == 0:
        langs = ['eng' if p[1] == Language.ENGLISH else 'es' for p in preds]
        return max(set(langs), key=langs.count)

    langs = ['eng' if p[1] == Language.ENGLISH else 'es' for p in conf_preds]
    binary_langs = [1 if l == 'eng' else 0 for l in langs]
    if has_switch(binary_langs):
        return 'mix'

    return max(set(langs), key=langs.count)

def examples():
    # bad word-lvl cls example. good whole sentence clf
    print_deubg('go and make a u-turn')
    # good word-lvl cls example. bad whole sentence clf
    print_deubg('hi there! que comience el juego!!')
    print_deubg('si debe empezar at the tent')
    print_deubg('hola, q tal? ready to go?')

    # other solution - sentence lvl
    sents = [
        'hi there! que comience el juego!!', # correct
        'go and make a u-turn',
        'hey, q tal? empezamos el juego?',
        'hi there, empezamos?',
        'hola, q tal? ready to go?', # mistake
        'si debe empezar at the tent', # mistake here
        'ok',
        'si',
    ]
    print('sentence-lvl predication using multiple lang util')
    for sentence in sents:
        print(sentence, '->', pred_lang_sentence(sentence).upper())
    print()


    # sequence solution
    print('sentence-lvl predication using Sequence counting')
    for sentence in sents:
        print(sentence, '->', custom_pred_lang_sentence(sentence).upper())
    print()

    # print(has_switch([1, 1, 1, 1, 0, 1, 1]))
    # print(has_switch([1,1,1,1,1,1,1]))
    # print(has_switch([1,1,1,0,1,1,1]))
    # print(has_switch([1,1,1,0,0,1,1]))
    # print(has_switch([1,1,0,0,0,0,0]))
    # print(has_switch([1,0,0,0,0,0,0]))
    # print(has_switch([0,0,0,0,0,1]))
    # print(has_switch([0,0,0,0,0,1,1,0,0,0]))


def examples2():
    sents = ['Okay, I am at the dirt path now. I will look east and I see a campfire. What do I do next?',
             'passing the crab and the large rock and the smaller rock. i see a shark and a ball. what do i do next?']
    for sentence in sents:
        print(sentence, '->', custom_pred_lang_sentence(sentence).upper())
    print()

if __name__ == '__main__':
    languages = [Language.ENGLISH, Language.SPANISH]
    detector = LanguageDetectorBuilder.from_languages(*languages).build()


    examples2()
    run_on_dataset()
    print(global_cs_counter)
