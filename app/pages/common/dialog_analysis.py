import numpy as np
import datetime

def get_tokens(utterances: list[str]):
    return [uter.split(' ') for uter in utterances]


def analysis_role_aux(utterances):
    tokens = get_tokens(utterances)
    tokens_amount = [len(uter_tokens) for uter_tokens in tokens]
    avg_uter_len = np.mean(tokens_amount)
    sum_tokens = np.sum(tokens_amount)

    return {
        'number of utterances': len(utterances),
        'mean utterance length': avg_uter_len,
        'total amount of tokens': sum_tokens,
    }


def analysis_game_chat(role: str, chat: list):
    last_bot_timestamp = None
    user_utterances = []
    bot_utterances = []
    user_time_diff = []

    for ele in chat:
        if ele['id'] != role:
            last_bot_timestamp = datetime.datetime.fromtimestamp(ele['timestamp']/1000)
            bot_utterances.append(ele['msg'])
            continue
        user_utterances.append(ele['msg'])
        if last_bot_timestamp is not None:
            user_time_diff.append(datetime.datetime.fromtimestamp(ele['timestamp']/1000) - last_bot_timestamp)

    user_res = analysis_role_aux(user_utterances)
    bot_res = analysis_role_aux(bot_utterances)

    # date_obj = datetime.fromtimestamp(timestamp / 1000.0)

    return user_res, bot_res


if __name__ == '__main__':
    import os, json
    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')
        data = json.load(json_file)
        chat = data['games_data'][0]['chat']
        role = 'instructor'

        analysis_game_chat(role, chat)
