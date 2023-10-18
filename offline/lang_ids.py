import json
import os
from lingua import Language, LanguageDetectorBuilder
import langid
from codeswitch.codeswitch import LanguageIdentification


def pred_token_lingua(token: str):
    lang = lingua_detector.detect_language_of(token)
    return 'eng' if lang == Language.ENGLISH else 'es'


def pred_token_langid(text):
    res = langid.classify(text)
    return 'eng' if res[0] == 'en' else 'es'


def cs_clf_heuristic(langs: list):
    if 'eng' in langs and 'es' in langs:
        return 'mix'
    if 'eng' in langs:
        return 'eng'
    if 'es' in langs:
        return 'es'
    return 'both'


def pred_sentence_via_token_lvl(sentence: str, pred_token: callable):
    langs = [pred_token(token) for token in sentence.split(' ')]
    return cs_clf_heuristic(langs)


def pred_sentence_bert(sentence: str):
    # https://huggingface.co/sagorsarker/codeswitch-spaeng-lid-lince
    result = lid.identify(sentence)
    langs = ['eng' if r['entity'] == 'en' else 'es' for r in result]
    return cs_clf_heuristic(langs)


def pred_sentence_lingua(sentence: str):
    result = lingua_detector.detect_multiple_languages_of(sentence)
    if len(result) == 1:
        return 'eng' if result[0].language == Language.ENGLISH else 'es'
    else:
        return 'mix'


def clf_map_task_dataset():
    root_folder = r"../data/prolific/"
    output_folder = r'../data/prolific_lang_ids'

    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')

        # if os.path.exists(os.path.join(output_folder, file_name)):
        #     print(f'skip: {file_name}')
        #     continue

        data = json.load(json_file)
        for game in data['games_data']:
            chat = game['chat']
            for chat_ele in chat:
                uter = chat_ele['msg']
                uter_lng = pred_sentence_bert(uter)
                chat_ele['lang'] = uter_lng

        # with open(os.path.join(output_folder, file_name), 'w') as f:
        #     json.dump(data, f)


def show_examples():
    sents = [
        'go down al la isla con el snake y ya llegastes',
        'donde empizo',
        'human',
        'car',
        'a car',
        'hi there! que comience el juego!!',  # correct
        'go and make a u-turn',
        'hey, q tal? empezamos el juego?',
        'hi there, empezamos?',
        'hola, q tal? ready to go?',  # mistake
        'si debe empezar at the tent',  # mistake here
        'ok',
        'si',
        'parrot',
        'hello',
        'genial, he llegado a la isla con el tesoro',
        'debe empezar',
    ]

    print('token-lvl predication using lingua')
    for sentence in sents:
        print(sentence, '->', pred_sentence_via_token_lvl(sentence, pred_token_lingua).upper())
    print()

    print('token-lvl predication using langid')
    for sentence in sents:
        print(sentence, '->', pred_sentence_via_token_lvl(sentence, pred_token_langid).upper())
    print()

    print('sentence-lvl predication using lingua')
    for sentence in sents:
        print(sentence, '->', pred_sentence_lingua(sentence).upper())
    print()

    print('sentence-lvl predication using lince-bert')
    for sentence in sents:
        print(sentence, '->', pred_sentence_bert(sentence).upper())
    print()


if __name__ == '__main__':
    languages = [Language.ENGLISH, Language.SPANISH]
    lingua_detector = LanguageDetectorBuilder.from_languages(*languages).build()

    langid.set_languages(['en', 'es'])

    lid = LanguageIdentification('spa-eng')

    show_examples()

    # run_on_dataset()
