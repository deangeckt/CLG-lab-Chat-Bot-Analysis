import json
import os
import re
import pandas as pd
from lingua import Language, LanguageDetectorBuilder
import langid
from codeswitch.codeswitch import LanguageIdentification
from collections import Counter
import codecs

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, precision_score
import matplotlib.pyplot as plt


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
    return 'none'


def pred_sentence_via_token_lvl(sentence: str, pred_token: callable):
    langs = [pred_token(token) for token in sentence.split(' ')]
    return cs_clf_heuristic(langs)


def pred_sentence_bert(sentence: str):
    # https://huggingface.co/sagorsarker/codeswitch-spaeng-lid-lince
    result = lid.identify(sentence)
    langs = []
    for r in result:
        lng = r['entity']
        if lng == 'en':
            langs.append('eng')
        elif lng == 'spa':
            langs.append('es')
    return cs_clf_heuristic(langs)

def pred_sentence_lingua(sentence: str):
    result = lingua_detector.detect_multiple_languages_of(sentence)
    if len(result) == 1:
        return 'eng' if result[0].language == Language.ENGLISH else 'es'
    else:
        return 'mix'


def __clf_map_task_dataset_uter_sent(uter: str):
    uter = uter.replace('*finished*', '').strip()
    uter = re.sub("(Ok,|OK,|ok,|Ok|OK|ok)", '', uter).strip()
    return pred_sentence_bert(uter)


def __clf_map_task_dataset_uter_cong_switch(uter: str) -> list[str]:
    """
    :return: list of switched per sentences: type of switch are either 'noun' or 'noun_det'
    'noun' for an english token switched w/o its previous determiner. i.e: 'el dog'
    'noun_det' with the determiner. i.e: 'the dog'
    """
    lng_tokens = lid.identify(uter)
    counts = Counter([ele['entity'] for ele in lng_tokens])
    if counts['spa'] < counts['en']:
        return []

    switches = []
    eng_tokens = [(ele['word'], idx) for idx, ele in enumerate(lng_tokens) if ele['entity'] == 'en']
    for eng_token, idx in eng_tokens:
        if eng_token not in eng_nouns:
            continue

        if idx == 0:
            switches.append('noun')
            continue

        prev_token = lng_tokens[idx-1]
        if prev_token['word'] == 'the':
            switches.append('noun_det')
        else:
            switches.append('noun')

    return switches

def clf_map_task_dataset():
    root_folder = r"data/prolific/"
    output_folder = r'data/prolific_lang_ids'

    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')

        # if os.path.exists(os.path.join(output_folder, file_name)):
        #     continue

        print(f'do: {file_name}')

        data = json.load(json_file)
        for game in data['games_data']:
            chat = game['chat']
            for chat_ele in chat:
                chat_ele['lang'] = __clf_map_task_dataset_uter_sent(chat_ele['msg'])
                chat_ele['cong_cs'] = __clf_map_task_dataset_uter_cong_switch(chat_ele['msg'])

        with open(os.path.join(output_folder, file_name), 'w') as f:
            json.dump(data, f)


def show_examples():
    sents = [
        'Go around the bottom of teh tiger and travel accross to the island with the parrot and elephant',
        'debe empezar',
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
    ]

    sents = [
        "Ve con el tiger",
        "ok aqui llegue con el perro",
        "OK ¿y ahora qué?",
        "Ok ¿y ahora qué?",
        "ok, aqui llegue con el perro",
        "OK, ¿y ahora qué?",
        "Ok, ¿y ahora qué?",
        "Ok , ¿y ahora qué?",
        '*finished* gracias por las instrucciones!',
        "Great job! Now, veer slightly left and start heading northwest. Remember to cross between the red tent and the larger speaker. Once you've done that, describe what you see next.",
        "Compra souvenirs en la tienda de regalos",
        'cruza por el stick hacia el tigre',
        "despues tienes que cruzar el alligator"
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
        sent = sentence.replace('*finished*', '').strip()
        sent = re.sub("(Ok,|OK,|ok,|Ok|OK|ok)", '', sent).strip()
        print(sentence, '->', pred_sentence_bert(sent).upper())
    print()


def eval_on_custom_dataset():
    def display_and_print(pred, title):
        cm = confusion_matrix(pred, gt, labels=labels)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
        disp.plot()
        plt.title(title)
        plt.show()

        print(title)
        prec = precision_score(gt, y_pred=pred, average='weighted')
        print(f'accuracy: {accuracy_score(gt, y_pred=pred)}')
        print(f'precision: {prec}')
        print()

    labels = ['eng', 'es', 'mix']
    df = pd.read_csv(r'offline/language/cs_dataset.csv', encoding='utf-8')
    gt = list(df['label'])
    sentences = list(df['text'])

    lingua_token_pred = [pred_sentence_via_token_lvl(sent, pred_token_lingua) for sent in sentences]
    langid_token_pred = [pred_sentence_via_token_lvl(sent, pred_token_langid) for sent in sentences]
    lingua_sent_pred = [pred_sentence_lingua(sent) for sent in sentences]
    bert_linsec_pred = [pred_sentence_bert(sent) for sent in sentences]

    # display_and_print(lingua_token_pred, 'lingua token-lvl')
    # display_and_print(langid_token_pred, 'langid token-lvl')
    # display_and_print(lingua_sent_pred, 'lingua sentence-lvl')
    display_and_print(bert_linsec_pred, 'bert-lince sentence-lvl')

    # explore mistakes
    for idx, y_pred in enumerate(bert_linsec_pred):
        y_true = gt[idx]
        sent = sentences[idx]
        if y_pred != y_true:
            print(f'gt: {y_true} pred: {y_pred} sent: {sent}')

            if y_true == 'eng':
                pred_sentence_bert(sent)


if __name__ == '__main__':
    """
    run from root repo
    """
    languages = [Language.ENGLISH, Language.SPANISH]
    lingua_detector = LanguageDetectorBuilder.from_languages(*languages).build()
    langid.set_languages(['en', 'es'])
    lid = LanguageIdentification('spa-eng')

    nouns_file = codecs.open('offline/nouns/spanish_nouns_set.txt', "r", "utf-8")
    es_to_eng_nouns = {n.strip().split('_')[0]: n.strip().split('_')[1] for n in nouns_file.readlines()}
    eng_nouns = set(list(es_to_eng_nouns.values()))

    show_examples()
    # eval_on_custom_dataset()
    # clf_map_task_dataset()
