import pandas as pd
import numpy as np
import json
import os
import altair as alt
from collections import defaultdict

root_folder = r"data/prolific/"
version_details = {'2.1.0_0_p': 'Rule Based navigator Bot',
                   '2.1.0_p': 'GPT based navigator bot. the human had 5 minutes timer',
                   '2.1.1_p': 'GPT based navigator bot the human had 7 minutes timer'}

experiments_short_names = {'2.1.0_0_p': 'rb navigator',
                           '2.1.0_p': 'GPT navigator, 5',
                           '2.1.1_p': 'GPT navigator, 7'}

#TODO: select questions:

def read_games_data():
    agg_data = defaultdict(lambda : defaultdict(list))
    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')
        data = json.load(json_file)

        client_version = data['clinet_version']
        experiment = experiments_short_names.get(client_version, 'err')

        for game_data in data['games_data']:
            for qa in game_data['survey']:
                question = qa['question']
                answer = qa['answer']
                agg_data[experiment][question].append(answer)

    flat_exp = []
    flat_q = []
    flat_mean_ans = []
    flat_median_ans = []
    samples = {}
    for exp in agg_data:

        for question in agg_data[exp]:
            answers = agg_data[exp][question]
            flat_exp.append(exp)
            flat_q.append(question)
            flat_mean_ans.append(np.mean(answers))
            flat_median_ans.append(np.median(answers))
            samples[exp] = len(agg_data[exp][question])

    return pd.DataFrame({
        "Experiment": flat_exp,
        "Question": flat_q,
        "Mean": flat_mean_ans,
        "Median": flat_median_ans
    }), samples


data, game_samples = read_games_data()

# display_ex_details = {experiments_short_names[key]: version_details[key] for key in experiments_short_names}
display_ex_details = {}
for key in experiments_short_names:
    name_key = experiments_short_names[key]
    display_ex_details[name_key] = {'details': version_details[key], 'samples': game_samples[name_key]}

df = pd.DataFrame(display_ex_details)

med_games_data = data[['Experiment', 'Question', 'Median']]


alt.Chart(data).mark_bar().encode(
    x="Question:N",
    y="Mean:Q",
    xOffset="Experiment:N",
    color="Experiment:N"
).interactive()
