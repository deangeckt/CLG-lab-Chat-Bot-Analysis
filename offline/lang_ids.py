import pandas as pd
import json
import os
from lingua import Language, LanguageDetectorBuilder


root_folder = r"../data/prolific/"
output_folder = r'../data/prolific_lang_ids'

def pred_lang_token(token: str):
    confidence_values  = detector.compute_language_confidence_values(token)
    simple_list = [(v.value, v.language) for v in confidence_values]
    conf, lng = max(simple_list)
    return conf, lng

def run_word_lvl_cls():
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
                tokens = uter.split(' ')

                words = []
                for token in tokens:
                    conf, lang = pred_lang_token(token)
                    lang = 'eng' if lang == Language.ENGLISH else 'es'
                    words.append({'token': token, 'lang': lang, 'conf': conf})
                chat_ele['words'] = words

        with open(os.path.join(output_folder, file_name), 'w') as f:
            json.dump(data, f)


def print_deubg(text: str):
    print(text, pred_lang_token(text))
    for token in text.split(' '):
        print(token, pred_lang_token(token))
    print()


if __name__ == '__main__':
    languages = [Language.ENGLISH, Language.SPANISH]
    detector = LanguageDetectorBuilder.from_languages(*languages).build()

    # bad word-lvl cls example. good whole sentence clf
    print_deubg('go and make a u-turn')
    # good word-lvl cls example. bad whole sentence clf
    print_deubg('hi there! que comience el juego!!')





