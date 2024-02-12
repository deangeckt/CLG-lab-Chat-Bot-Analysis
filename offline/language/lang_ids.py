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


def clean_endings(token: str):
    if token.endswith(('!', '.', '?', '¿', ',')):
        return token[:len(token) - 1]
    return token


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


def __clf_map_task_dataset_uter_lng(uter: str):
    uter = uter.replace('*finished*', '').strip()
    uter = re.sub("(Ok,|OK,|ok,|Ok|OK|ok)", '', uter).strip()
    return pred_sentence_bert(uter)


def __clf_map_task_dataset_uter_cong_switch_per_token(eng_token: str, idx: int, sentence: list[str]):
    if eng_token not in eng_nouns:
        return None

    if idx == 0:
        print(f'{eng_token} in IDX 0')
        return None

    masc_femi_determiners_dict = {
        'el': 'la',  # the singular
        'los': 'las',  # the plural
        'ese': 'esa',  # that
        'este': 'esta',  # this
        'esos': 'esas',  # those
        'estos': 'estas',  # those
        'un': 'una',  # a singular
        'unos': 'unas',  # a plural
        'nuestro': 'nuestra',  # my
        'nuestros': 'nuestras',  # ours
        'vuestro': 'vuestra',  # your
        'vuestros': 'vuestras',  # theirs
        #### ADP
        'del': 'de la',  # to the
        'al': 'a la',  # of / to the (al = a + el shortcut)
    }

    eng_determiners = [
        "the",
        "a",
        "an",
        "this",
        "that",
        "these",
        "those",
        "my",
        "your",
        "his",
        "her",
        "its",
        "our",
        "their",
        "mine",
        "yours",
        "hers",
        "ours",
        "theirs",
        "all",
        "every",
        "each",
        "any",
        "some",
        "several",
        "many",
        "few",
        "numerous",
        "one",
        "two",
        "three",
        "half",
        "a third",
        "three-quarters",
        "enough",
        "lots of",
        "plenty of",
        "most",
        "more",
        "less",
        "little",
        "much",
        "none",
        "no",
        "another",
        "other",
        "both",
        "either",
        "neither",
        "which",
        "what",
        "whose",
        "either",
        "neither",
        "both",
        "all",
        "both",
        "half",
        "twice",
        "double",
        "such",
        "what",
        "rather",
        "quite",
        "one",
        "two",
        "three",
        "first",
        "second",
        "third",
        "single",
        "double",
        "triple",
        "half",
        "third",
        "quarter"
    ]

    prev_token = sentence[idx - 1]
    if prev_token in eng_determiners:
        return 'NP'

    if prev_token in masc_femi_determiners_dict:
        det_gender = 'masc'
    elif prev_token in set(masc_femi_determiners_dict.values()):
        det_gender = 'fem'
    else:
        return 'cong'

    noun_gender = eng_nouns[eng_token]
    if noun_gender == 'amb':
        return f'amb_{det_gender}'

    if noun_gender == 'masc' and det_gender == 'masc':
        return 'cong'
    if noun_gender == 'fem' and det_gender == 'fem':
        return 'cong'
    if noun_gender == 'masc' and det_gender == 'fem':
        return 'incong1'

    return 'incong2'


def __clf_map_task_dataset_uter_cong_switch(uter: str) -> list[str]:
    """
    :return: list of switched per sentences: type of switch are either 'noun' or 'noun_det'
    'noun' for an english token switched w/o its previous determiner. i.e: 'el dog'
    'noun_det' with the determiner. i.e: 'the dog'
    """
    switches = []

    lng_tokens = lid.identify(uter)
    counts = Counter([ele['entity'] for ele in lng_tokens])
    if counts['spa'] < counts['en']:
        return []

    found_by_clf = set()
    eng_tokens = [(ele['word'], idx) for idx, ele in enumerate(lng_tokens) if ele['entity'] == 'en']
    sentence_by_clf = [ele['word'] for ele in lng_tokens]
    for eng_token, idx in eng_tokens:
        label = __clf_map_task_dataset_uter_cong_switch_per_token(eng_token, idx, sentence_by_clf)
        if label is not None:
            switches.append(label)
            # print('clf', eng_token, label)
            found_by_clf.add(eng_token)

    # fallback: when clf is missing
    sentence_by_split = uter.split(' ')
    sentence_by_split = [clean_endings(token) for token in sentence_by_split]
    eng_tokens = [(token, idx) for idx, token in enumerate(sentence_by_split) if token in eng_nouns]
    for eng_token, idx in eng_tokens:
        if eng_token in found_by_clf:
            continue
        label = __clf_map_task_dataset_uter_cong_switch_per_token(eng_token, idx, sentence_by_split)
        if label is not None:
            switches.append(label)
            # print('basic', eng_token, label)

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
                chat_ele['lang'] = __clf_map_task_dataset_uter_lng(chat_ele['msg'])
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
    # languages = [Language.ENGLISH, Language.SPANISH]
    # lingua_detector = LanguageDetectorBuilder.from_languages(*languages).build()
    # langid.set_languages(['en', 'es'])
    lid = LanguageIdentification('spa-eng')

    nouns_file = codecs.open('offline/nouns/english_nouns_gender_set.txt', "r", "utf-8")
    eng_nouns = {n.strip().split('_')[0]: n.strip().split('_')[1] for n in nouns_file.readlines()}

    # show_examples()
    # eval_on_custom_dataset()
    clf_map_task_dataset()

    # print(__clf_map_task_dataset_uter_cong_switch('perfecto, acabo cruzar al pequeño islote con la tiger'))
    # print(__clf_map_task_dataset_uter_cong_switch('pasas por el area verde debajo de la roca negra, y cruces por el palo hacia el parrot'))
    # print(__clf_map_task_dataset_uter_cong_switch('pases encima del parrot y caminas entre el parrot y el elefante. De alli, debajo del parrot y hacia las rocks para cruzar el rio'))

    # print(__clf_map_task_dataset_uter_cong_switch('pases debajo del frog pero cuando pases el frog, darle la U y giras hacia la crocodile'))
    # print(__clf_map_task_dataset_uter_cong_switch('pasaste por el crocodile?'))

    # print(__clf_map_task_dataset_uter_cong_switch('cruzas el twig para llegar a la pequena isla con la tigre en ella'))
    # print(__clf_map_task_dataset_uter_cong_switch('okay regresse adonde empenze mi viaje y estoy al lado del perro y el twig. ahora que hago?'))
    # print(__clf_map_task_dataset_uter_cong_switch('pase el picnic y ahora estoy al frente de un twig que cruzas por donde esta el puente que no pude pasar ahora. quieres que lo cruse? o cruzo el otro twig que estas mas para el sur y tiene una cierva?'))
    # print(__clf_map_task_dataset_uter_lng('le di la vuelta al bush, ahora que?'))
