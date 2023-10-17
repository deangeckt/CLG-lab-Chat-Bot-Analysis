import numpy as np
import datetime



def get_tokens(utterances: list[str]):
    return [uter.split(' ') for uter in utterances]


def analysis_role_aux(elements):
    utterances = [ele['msg'] for ele in elements]
    tokens = get_tokens(utterances)
    tokens_amount = [len(uter_tokens) for uter_tokens in tokens]
    avg_uter_len = np.mean(tokens_amount)
    sum_tokens = np.sum(tokens_amount)

    if len(tokens_amount) == 0:
        avg_uter_len = 0

    counts_dict = {
        'number of utterances': len(utterances),
        'mean utterance length': avg_uter_len,
        'total number of tokens': sum_tokens,
    }

    # languages
    langs = [ele['lang'] for ele in elements]
    keys = ['eng', 'es', 'mix']
    lang_dict = {k: 0 for k in keys}
    for lang in langs:
        lang_dict[lang] += 1

    lang_dict_format = {f'number of {k} utterances': lang_dict[k] for k in lang_dict}

    num_of_uter_switch = 0
    if len(langs) > 1:
        prev_lang = langs[0]
        for lang in langs[1:]:
            if lang != prev_lang and lang != 'mix' and prev_lang != 'mix':
                num_of_uter_switch += 1
            prev_lang = lang

    lang_dict_format['number of utterances-switch'] = num_of_uter_switch

    return {**counts_dict, **lang_dict_format}


def analysis_game_chat(role: str, chat: list):
    last_bot_timestamp = None
    user_utterances = []
    bot_utterances = []
    user_time_diff = []

    for ele in chat:
        if ele['id'] != role:
            last_bot_timestamp = datetime.datetime.fromtimestamp(ele['timestamp']/1000)
            bot_utterances.append(ele)
            continue
        user_utterances.append(ele)
        if last_bot_timestamp is not None:
            user_time_diff.append(datetime.datetime.fromtimestamp(ele['timestamp']/1000) - last_bot_timestamp)

    user_res = analysis_role_aux(user_utterances)
    bot_res = analysis_role_aux(bot_utterances)

    # date_obj = datetime.fromtimestamp(timestamp / 1000.0)

    return user_res, bot_res


if __name__ == '__main__':
    import os, json
    from app.pages.common.versions import root_folder

    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')
        data = json.load(json_file)
        chat = data['games_data'][0]['chat']
        role = 'instructor'

        analysis_game_chat(role, chat)
