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
    keys = ['eng', 'es', 'mix', 'none']
    lang_dict = {k: 0 for k in keys}
    for lang in langs:
        if lang not in keys:
            continue
        lang_dict[lang] += 1

    lang_dict_format = {f'number of {k} utterances': lang_dict[k] for k in lang_dict}

    # inter-sentential cs
    num_of_uter_switch = 0
    if len(langs) > 1:
        no_switch = ['mix', 'none']
        prev_lang = langs[0]
        for lang in langs[1:]:
            if lang != prev_lang and lang not in no_switch and prev_lang not in no_switch:
                num_of_uter_switch += 1
            prev_lang = lang

    lang_dict_format['number of inter-sentential cs'] = num_of_uter_switch

    # Congruent cs
    uter_switch_amount = 0
    switch_amount = 0

    cong_cs_labels = ['cong', 'incong1', 'incong2', 'amb_masc', 'amb_fem']
    cong_cs_labels_dict = {k: 0 for k in cong_cs_labels}

    for uter_ele in elements:
        uter_switches = uter_ele['cong_cs']
        if not uter_switches:  # empty list
            continue
        uter_switch_amount += 1
        switch_amount += len(uter_switches)
        for cong_cs_label in uter_switches:
            cong_cs_labels_dict[cong_cs_label] += 1

    cong_cs_labels_dict_format = {f'number of {k} switches': cong_cs_labels_dict[k] for k in cong_cs_labels_dict}

    cong_dict_format = {'number of utterances with some congruent switch': uter_switch_amount,
                        'number of total congruent switches': switch_amount
                        }
    cong_dict_format = {**cong_dict_format, **cong_cs_labels_dict_format}

    return {**counts_dict, **lang_dict_format, **cong_dict_format}


def squash_bot_chat(role: str, chat: list):
    """
    since some turns of the bot includes 2 utterances, we remove duplicat langauge uters for later easier analysis:
    e.g: bot: 'en', 'en' -> 'en'
    """
    same_lng_turn_bot_indices = []
    for i in range(len(chat) - 1):
        curr_ele = chat[i]
        if curr_ele['id'] == role:
            continue
        next_ele = chat[i + 1]
        if next_ele['id'] != role and next_ele['lang'] == curr_ele['lang']:
            same_lng_turn_bot_indices.append(i)

    for del_idx in sorted(same_lng_turn_bot_indices, reverse=True):
        del chat[del_idx]
    return chat


def analysis_entrainment(role: str, chat: list):
    """
    Counts the number of times a human utterance is the same language as the prev bot language OR
    does it only when the Bot switched language.

    return percentage already
    """
    chat = [{'id': ele['id'], 'lang': ele['lang']} for ele in chat]
    chat = squash_bot_chat(role, chat)

    human_uters = len(list(filter(lambda e: e['id'] == role, chat)))

    last_bot_lng = chat[0]['lang']
    curr_bot_lng = None
    no_switch = ['mix', 'none']
    bot_just_switch = False

    same_as_last_bot_counter = 0
    same_as_last_bot_on_inter_sentential = 0
    bot_inter_sentential_count = 0

    for ele_idx, ele in enumerate(chat[1:]):
        if ele['id'] != role:
            curr_bot_lng = ele['lang']
            if curr_bot_lng != last_bot_lng and curr_bot_lng not in no_switch and last_bot_lng not in no_switch:
                bot_just_switch = True
                if ele_idx < len(chat[1:]) - 1:
                    bot_inter_sentential_count += 1
            else:
                bot_just_switch = False
            last_bot_lng = curr_bot_lng
        else:
            curr_human_lng = ele['lang']
            if last_bot_lng == 'mix' or curr_human_lng == 'mix' or curr_human_lng == last_bot_lng:
                same_as_last_bot_counter += 1
                if bot_just_switch:
                    same_as_last_bot_on_inter_sentential += 1

    entr_on_bot_is_cs = same_as_last_bot_on_inter_sentential / bot_inter_sentential_count if bot_inter_sentential_count > 0 else 0
    entr_all_dialog = same_as_last_bot_counter / human_uters if human_uters > 0 else 0
    return {
        '% entrainment - all dialog': entr_all_dialog,
        '% entrainment - on bot inter-sentential cs': entr_on_bot_is_cs
    }


def analysis_game_chat(role: str, chat: list):
    """
    :param role: role of the human in the given chat
    """
    last_bot_timestamp = None
    user_utterances = []
    bot_utterances = []
    user_time_diff = []

    for ele in chat:
        if ele['id'] != role:
            last_bot_timestamp = datetime.datetime.fromtimestamp(ele['timestamp'] / 1000)
            bot_utterances.append(ele)
            continue
        user_utterances.append(ele)
        if last_bot_timestamp is not None:
            user_time_diff.append(datetime.datetime.fromtimestamp(ele['timestamp'] / 1000) - last_bot_timestamp)

    user_res = None
    if user_utterances:
        user_res = analysis_role_aux(user_utterances)
        user_entrainment = analysis_entrainment(role, chat)
        user_res = {**user_res, **user_entrainment}

    bot_res = analysis_role_aux(bot_utterances)

    # date_obj = datetime.fromtimestamp(timestamp / 1000.0)

    return user_res, bot_res


if __name__ == '__main__':
    import os, json
    from app.pages.common.versions import root_folder

    for file_name in os.listdir(root_folder):
        if file_name != '654e534073c3d26b0f9ef335.json':
            continue
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')
        data = json.load(json_file)
        chat = data['games_data'][0]['chat']
        role = 'instructor'

        analysis_game_chat(role, chat)
