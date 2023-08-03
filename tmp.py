import pandas as pd
import numpy as np
import json
import os
from collections import defaultdict
import datetime
import math

from app.pages.common.gt_path import levenshtein_distance
from app.pages.common.versions import root_folder, experiments_short_names, time_success_metric, version_details

default_rating_range = 'not at all: 0 -> extremely: 100'
rating_likely_range = 'not at all likely: 0 -> extremely likely: 100'
knowledge_range = 'no knowledge at all: 0 -> perfect, like a native speaker: 100'
time_range = 'never: 0 -> always: 100'
enjoy_range = 'not at all: 0 -> yes very much: 100'

questions_ranges = {
    'How likely is your partner to be a fluent speaker of English?': rating_likely_range,
    'How likely do you think it was that you were talking to a chatbot rather than a human?': rating_likely_range,
    'How likely is your partner to be a fluent speaker of Spanish?': rating_likely_range,
    'How likely do you think it is that your partner is bilingual?': rating_likely_range,
    'Do you enjoy mixing languages in conversation?': enjoy_range,
    'Age': ''
}


def get_question_range_metadata(question: str):
    if question.startswith('Please rate how likely you are to use your'): return rating_likely_range
    if question.startswith('How would you rate your fluency in your '): return knowledge_range
    if question.startswith('When you switch languages'): return time_range
    return questions_ranges.get(question, default_rating_range)


def agg_dict_data_to_df(agg_data: dict):
    flat_exp = []
    flat_q = []
    flat_q_range = []
    flat_mean_ans = []
    flat_median_ans = []

    for exp in agg_data:
        for question in agg_data[exp]:
            answers = agg_data[exp][question]
            flat_exp.append(exp)
            flat_q.append(question)
            flat_q_range.append(get_question_range_metadata(question))
            flat_mean_ans.append(np.mean(answers))
            flat_median_ans.append(np.median(answers))

    return pd.DataFrame({
        "Experiment": flat_exp,
        "Question": flat_q,
        "Range": flat_q_range,
        "Mean": flat_mean_ans,
        "Median": flat_median_ans
    })

def read_games_data() -> tuple[pd.DataFrame, dict]:
    agg_data = defaultdict(lambda: defaultdict(list))
    agg_time_nav = defaultdict(list)
    agg_time_success_nav = defaultdict(list)

    agg_time_ins = defaultdict(list)
    agg_time_success_ins = defaultdict(list)

    agg_dist_score = defaultdict(list)
    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')
        data = json.load(json_file)

        client_version = data['clinet_version']
        experiment = experiments_short_names.get(client_version, 'err')

        for game_data in data['games_data']:
            agg_time = agg_time_ins
            agg_time_success = agg_time_success_ins

            if game_data['config']['game_role'] == 'navigator':
                dist_score = levenshtein_distance(game_data['config']['map_index'],
                                                  game_data['user_map_path'])
                agg_dist_score[experiment].append(dist_score)

                # write to correct role
                agg_time = agg_time_nav
                agg_time_success = agg_time_success_nav


            game_time = game_data['game_time']
            agg_time[experiment].append(game_time)

            max_game_time = time_success_metric(client_version)
            is_time_success = 1 if game_time < max_game_time else 0
            agg_time_success[experiment].append(is_time_success)

            for qa in game_data['survey']:
                question = qa['question']
                answer = qa['answer']
                agg_data[experiment][question].append(answer)

    more_data = defaultdict(lambda: defaultdict(dict))
    for exp in agg_data:
        print(exp)

        ins_samples = len(agg_time_ins[exp])
        if ins_samples > 0:
            more_data[exp]['ins_game_time_mean'] = np.mean(agg_time_ins[exp])
            more_data[exp]['ins_game_time_median'] = np.median(agg_time_ins[exp])
            game_time_success_abs = np.count_nonzero(agg_time_success_ins[exp])
            more_data[exp]['ins_game_time_success_abs'] = game_time_success_abs
            more_data[exp]['ins_game_time_success_perc'] = round((game_time_success_abs / ins_samples) * 100, 2)

        nav_samples = len(agg_time_nav[exp])
        if nav_samples > 0:
            more_data[exp]['nav_game_time_mean'] = np.mean(agg_time_nav[exp])
            more_data[exp]['nav_game_time_median'] = np.median(agg_time_nav[exp])
            game_time_success_abs = np.count_nonzero(agg_time_success_nav[exp])
            more_data[exp]['nav_game_time_success_abs'] = game_time_success_abs
            more_data[exp]['nav_game_time_success_perc'] = round((game_time_success_abs / len(agg_time_nav[exp])) * 100, 2)

            more_data[exp]['navigator_dist_score'] = np.mean(agg_dist_score[exp])
        more_data[exp]['samples'] = nav_samples + ins_samples

    df = agg_dict_data_to_df(agg_data)
    return df, more_data


def get_ex_date(data):
    game_data = data['games_data'][0]
    chat_ele = game_data['chat'][0]
    timestamp = chat_ele['timestamp']
    date_obj = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    return date_obj.strftime("%D")


def get_human_role(data, experiment):
    if 'Alternation' in experiment:
        return 'Alternations'
    game_data = data['games_data'][0]
    return game_data['config']['game_role']


def game_time_format(t: int):
    mins = math.floor(t / 60)
    sec = math.floor(t % 60)
    sec = f'{sec}' if sec >= 10 else f'0{sec}'
    return f'{mins}:{sec}'


def read_general_data() -> tuple[pd.DataFrame, dict]:
    agg_data = defaultdict(lambda: defaultdict(list))
    count = defaultdict(int)
    more_data = defaultdict(lambda: defaultdict(dict))

    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')
        data = json.load(json_file)

        client_version = data['clinet_version']
        experiment = experiments_short_names.get(client_version, 'err')
        count[experiment] += 1
        more_data[experiment]['date'] = get_ex_date(data)
        more_data[experiment]['human_role'] = get_human_role(data, experiment)

        for qa in data['general_survey']:
            question = qa['question']
            answer = qa['answer']
            if type(answer) == int:
                agg_data[experiment][question].append(answer)
            elif question == 'Age:':
                agg_data[experiment]['Age'].append(int(answer))

    for ex in more_data:
        more_data[ex]['participants'] = count[ex]

    df = agg_dict_data_to_df(agg_data)
    return df, more_data



games_data, game_more_data = read_games_data()
general_data, general_more_data = read_general_data()

def build_role_table_aux(name_key, role):
   if not f'{role}_game_time_mean' in game_more_data[name_key]:
       return {}

   res = {
        'mean game time': game_time_format(game_more_data[name_key][f'{role}_game_time_mean']),
        'median game time': game_time_format(game_more_data[name_key][f'{role}_game_time_median']),
        'number of games finished before time is over': game_more_data[name_key][f'{role}_game_time_success_abs'],
        'percentage of games finished before time is over': f"{game_more_data[name_key][f'{role}_game_time_success_perc']}%"
   }

   if role == 'nav':
       res['mean levenshtein distance'] = f"{game_more_data[name_key]['navigator_dist_score']:.2f}"
   return res


general_ex_details = {}
navigator_ex_details = {}
instructor_ex_details = {}

for key in experiments_short_names:
    name_key = experiments_short_names[key]
    if name_key not in general_more_data:
        continue
    general_ex_details[name_key] = {'details': version_details[key],
                            'human role': general_more_data[name_key]['human_role'],
                            'participants': general_more_data[name_key]['participants'],
                            'date': general_more_data[name_key]['date'],
                            'number of games': game_more_data[name_key]['samples']}

    navigator_ex_details[name_key] = build_role_table_aux(name_key, 'nav')
    instructor_ex_details[name_key] = build_role_table_aux(name_key, 'ins')



print(general_ex_details)