import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import altair as alt
from collections import defaultdict
import datetime


root_folder = r"data/prolific/"
version_details = {'2.1.0_0_p': 'Rule Based navigator Bot',
                   '2.1.0_p': 'GPT based navigator bot. the human had 5 minutes timer',
                   '2.1.1_p': 'GPT based navigator bot. the human had 7 minutes timer'}

experiments_short_names = {'2.1.0_0_p': 'rb navigator',
                           '2.1.0_p': 'GPT navigator, 5',
                           '2.1.1_p': 'GPT navigator, 7'}

time_success_metric = {'2.1.0_0_p': 300,
                       '2.1.0_p': 300,
                       '2.1.1_p': 420
                    }


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
    agg_data = defaultdict(lambda : defaultdict(list))
    agg_time = defaultdict(list)
    agg_time_success = defaultdict(list)
    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')
        data = json.load(json_file)

        client_version = data['clinet_version']
        experiment = experiments_short_names.get(client_version, 'err')

        for game_data in data['games_data']:
            game_time = game_data['game_time']
            agg_time[experiment].append(game_time)

            max_game_time = time_success_metric.get(client_version, 'err')
            is_time_success = 1 if game_time < max_game_time else 0
            agg_time_success[experiment].append(is_time_success)

            for qa in game_data['survey']:
                question = qa['question']
                answer = qa['answer']
                agg_data[experiment][question].append(answer)

    more_data = defaultdict(lambda : defaultdict(dict))
    for exp in agg_data:
        for question in agg_data[exp]:
            more_data[exp]['samples'] = len(agg_data[exp][question])
        more_data[exp]['game_time_mean'] = np.mean(agg_time[exp])
        more_data[exp]['game_time_median'] = np.median(agg_time[exp])
        more_data[exp]['game_time_success'] = f'{np.count_nonzero(agg_time_success[exp])}'

    df = agg_dict_data_to_df(agg_data)
    return df, more_data

def get_ex_date(data):
    game_data = data['games_data'][0]
    chat_ele = game_data['chat'][0]
    timestamp = chat_ele['timestamp']
    date_obj = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    return date_obj.strftime("%D")

def get_human_role(data):
    game_data = data['games_data'][0]
    return game_data['config']['game_role']



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
        more_data[experiment]['human_role'] = get_human_role(data)

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

games_data, game_more_data = read_games_data()
general_data, general_more_data = read_general_data()

ex_details = {}
for key in experiments_short_names:
    name_key = experiments_short_names[key]
    ex_details[name_key] = {'details': version_details[key],
                            'human role': general_more_data[name_key]['human_role'],
                            'participants': general_more_data[name_key]['participants'],
                            'date': general_more_data[name_key]['date'],
                            'mean game time [S]': game_more_data[name_key]['game_time_mean'],
                            'median game time [S]': game_more_data[name_key]['game_time_median'],
                            'number of games': game_more_data[name_key]['samples'],
                            'games finished before time is over': game_more_data[name_key]['game_time_success']
                            }
display_details_table = pd.DataFrame.from_dict(ex_details)

st.subheader("Experiments")
st.table(display_details_table)

st.subheader("Game Survey")
plot_chart(games_data, 'Mean', ['Question', 'Mean', 'Experiment', 'Range'])
plot_chart(games_data, 'Median', ['Question', 'Median', 'Experiment', 'Range'])

st.subheader("General Survey")
plot_chart(general_data, 'Mean', ['Question', 'Mean', 'Experiment', 'Range'])
plot_chart(general_data, 'Median', ['Question', 'Median', 'Experiment', 'Range'])