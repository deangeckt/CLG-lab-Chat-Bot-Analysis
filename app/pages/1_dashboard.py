import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import altair as alt
from collections import defaultdict
import datetime
import math

from pages.common.versions import *
from pages.common.gt_path import *
from pages.common.dialog_analysis import *


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
    'Do you enjoy mixing languages in conversation?':enjoy_range,
    'Age': ''
}

question_to_table = ['How much did you enjoy the task?',
                    "How successful do you think you were at completing the task?"]

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

def mean_and_format_str(arr: list) -> str:
    return f"{np.mean(arr):.2f}"

def avg_role_metadata(agg_metadata: defaultdict):
    samples = len(agg_metadata['game_time'])
    if samples == 0:
        return None

    res = {
        'number of games': samples,
        'mean game time': game_time_format(np.mean(agg_metadata['game_time'])),
        'median game time': game_time_format(np.median(agg_metadata['game_time']))
    }
    game_time_success_abs = np.count_nonzero(agg_metadata['is_time_success'])
    res['number of games finished before time is over'] = game_time_success_abs
    res['percentage of games finished before time is over'] = f'{round((game_time_success_abs / samples) * 100, 2)}%'

    # dialog
    res['human - mean number of utterances'] = mean_and_format_str(agg_metadata['user_num_of_uter'])
    res['human - mean mean utterance length'] = mean_and_format_str(agg_metadata['user_mean_uter'])
    res['human - mean total number of tokens'] = mean_and_format_str(agg_metadata['user_total_uter'])

    res['human - mean number of eng utterances'] = mean_and_format_str(agg_metadata['user_num_of_en'])
    res['human - mean number of es utterances'] = mean_and_format_str(agg_metadata['user_num_of_es'])
    res['human - mean number of mixed utterances'] = mean_and_format_str(agg_metadata['user_num_of_mix'])
    res['human - mean number of inter-sentential cs'] = mean_and_format_str(agg_metadata['user_num_of_inter_cs'])

    res['bot - mean number of utterances'] = mean_and_format_str(agg_metadata['bot_num_of_uter'])
    res['bot - mean mean utterance length'] = mean_and_format_str(agg_metadata['bot_mean_uter'])
    res['bot - mean total number of tokens'] = mean_and_format_str(agg_metadata['bot_total_uter'])

    res['bot - mean number of eng utterances'] = mean_and_format_str(agg_metadata['bot_num_of_en'])
    res['bot - mean number of es utterances'] = mean_and_format_str(agg_metadata['bot_num_of_es'])
    res['bot - mean number of mixed utterances'] = mean_and_format_str(agg_metadata['bot_num_of_mix'])
    res['bot - mean number of inter-sentential cs'] = mean_and_format_str(agg_metadata['bot_num_of_inter_cs'])



    for q in question_to_table:
        res[f"{q} [mean]"] = mean_and_format_str(agg_metadata[q])

    if 'dist_score' in agg_metadata:
        res['mean levenshtein distance'] = f"{np.mean(agg_metadata['dist_score']):.2f}"
    return res

def read_games_data() -> tuple[pd.DataFrame, dict, dict]:
    # first hierarchy is the experiment, 2nd is the survey
    agg_data = defaultdict(lambda: defaultdict(list))
    # first hierarchy is the experiment, 2nd is some metric we calculate
    agg_metadata_nav = defaultdict(lambda: defaultdict(list))
    agg_metadata_ins = defaultdict(lambda: defaultdict(list))

    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')
        data = json.load(json_file)

        client_version = data['clinet_version']
        experiment = experiments_short_names.get(client_version, 'err')

        for game_data in data['games_data']:
            agg_meta = agg_metadata_ins

            if game_data['config']['game_role'] == 'navigator':
                # update to correct role
                agg_meta = agg_metadata_nav

                dist_score = levenshtein_distance(game_data['config']['map_index'], game_data['user_map_path'])
                agg_meta[experiment]['dist_score'].append(dist_score)

            game_time = game_data['game_time']
            agg_meta[experiment]['game_time'].append(game_time)
            max_game_time = time_success_metric(client_version)
            is_time_success = 1 if int(game_time) < max_game_time else 0
            agg_meta[experiment]['is_time_success'].append(is_time_success)

            user_dialog, bot_dialog = analysis_game_chat(game_data['config']['game_role'], game_data['chat'])
            agg_meta[experiment]['user_num_of_uter'].append(user_dialog['number of utterances'])
            agg_meta[experiment]['user_mean_uter'].append(user_dialog['mean utterance length'])
            agg_meta[experiment]['user_total_uter'].append(user_dialog['total number of tokens'])

            agg_meta[experiment]['user_num_of_en'].append(user_dialog['number of eng utterances'])
            agg_meta[experiment]['user_num_of_es'].append(user_dialog['number of es utterances'])
            agg_meta[experiment]['user_num_of_mix'].append(user_dialog['number of mix utterances'])
            agg_meta[experiment]['user_num_of_inter_cs'].append(user_dialog['number of inter-sentential cs'])

            agg_meta[experiment]['bot_num_of_uter'].append(bot_dialog['number of utterances'])
            agg_meta[experiment]['bot_mean_uter'].append(bot_dialog['mean utterance length'])
            agg_meta[experiment]['bot_total_uter'].append(bot_dialog['total number of tokens'])

            agg_meta[experiment]['bot_num_of_en'].append(bot_dialog['number of eng utterances'])
            agg_meta[experiment]['bot_num_of_es'].append(bot_dialog['number of es utterances'])
            agg_meta[experiment]['bot_num_of_mix'].append(bot_dialog['number of mix utterances'])
            agg_meta[experiment]['bot_num_of_inter_cs'].append(bot_dialog['number of inter-sentential cs'])


            for qa in game_data['survey']:
                question = qa['question']
                answer = qa['answer']
                agg_data[experiment][question].append(answer)

                if question in question_to_table:
                    agg_meta[experiment][question].append(answer)

    nav_more_data = defaultdict(lambda: defaultdict(dict))
    ins_more_data = defaultdict(lambda: defaultdict(dict))

    for exp in agg_data:
        nav_more_data[exp] = avg_role_metadata(agg_metadata_nav[exp])
        ins_more_data[exp] = avg_role_metadata(agg_metadata_ins[exp])

    df = agg_dict_data_to_df(agg_data)
    return df, nav_more_data, ins_more_data

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
    agg_data = defaultdict(lambda : defaultdict(list))
    count = defaultdict(int)
    more_data = defaultdict(lambda : defaultdict(dict))

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

def plot_chart(data, title, cols):
    selected_dfs = []
    for selected_ex in st.session_state.selected_ex:
        selected_dfs.append(data.loc[data['Experiment'] == selected_ex])
    if len(selected_dfs) == 0:
        return
    data = pd.concat(selected_dfs)

    sub_data = data[cols]
    chart = alt.Chart(sub_data, title=title).mark_bar().encode(
        x="Question:N",
        y=f"{title}:Q",
        xOffset="Experiment:N",
        color="Experiment:N",
        tooltip=cols

    )
    st.altair_chart(chart, use_container_width=True)


st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.sidebar.success("Dashboard")

st.subheader("Experiments")



all_experiments = list(experiments_short_names.values())
selected_started_ex = []
for short_name in experiments_short_names:
    if 'Alternation' in experiments_short_names[short_name]:
        selected_started_ex.append(experiments_short_names[short_name])

if 'selected_ex' not in st.session_state:
    st.session_state.selected_ex = selected_started_ex

st.session_state.selected_ex = st.multiselect('Choose experiment:',  all_experiments, selected_started_ex)

games_data, navigator_ex_details, instructor_ex_details = read_games_data()
general_data, general_more_data = read_general_data()


general_ex_details = {}
navigator_det_copy = {} # refresh on selected experiments
instructor_det_copy = {}
for key in experiments_short_names:
    name_key = experiments_short_names[key]
    if name_key not in st.session_state.selected_ex:
        continue
    if name_key not in general_more_data:
        continue
    general_ex_details[name_key] = {
                            'details': version_details[key],
                            'human role': general_more_data[name_key]['human_role'],
                            'participants': general_more_data[name_key]['participants'],
                            'date': general_more_data[name_key]['date']
    }
    navigator_det_copy[name_key] = navigator_ex_details[name_key]
    instructor_det_copy[name_key] = instructor_ex_details[name_key]

display_details_table = pd.DataFrame.from_dict(general_ex_details)
st.table(display_details_table)

st.subheader("Navigator")
nav_table = pd.DataFrame.from_dict(navigator_det_copy)
st.table(nav_table)
st.subheader("Instructor")
ins_table = pd.DataFrame.from_dict(instructor_det_copy)
st.table(ins_table)


st.subheader("Game Survey")
plot_chart(games_data, 'Mean', ['Question', 'Mean', 'Experiment', 'Range'])
plot_chart(games_data, 'Median', ['Question', 'Median', 'Experiment', 'Range'])

st.subheader("General Survey")
plot_chart(general_data, 'Mean', ['Question', 'Mean', 'Experiment', 'Range'])
plot_chart(general_data, 'Median', ['Question', 'Median', 'Experiment', 'Range'])
