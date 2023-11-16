"""
CSV format:
Each row in a single experiment-game
Each column is a "feature" e.g.: game_time, number of utterance
Extra columns: experiment name, human/bot and game role (navigator/instructor)
"""
import pandas as pd
import numpy as np
import json
import os
import datetime
import math
from collections import defaultdict

from app.pages.common.dialog_analysis import analysis_game_chat
from app.pages.common.gt_path import levenshtein_distance
from app.pages.common.versions import experiments_short_names, root_folder, time_success_metric

question_to_table = ['How much did you enjoy the task?',
                    "How successful do you think you were at completing the task?"]

def read_games_data() -> tuple[pd.DataFrame, dict, dict]:
    df = pd.DataFrame()

    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')
        data = json.load(json_file)

        version = data['server_version']
        experiment = experiments_short_names.get(version, 'err')

        game_data_dict = {}

        for game_data in data['games_data']:
            game_role = game_data['config']['game_role']

            game_data_dict['experiment'] = experiment
            game_data_dict['human_role'] = game_role

            if game_role == 'navigator':
                dist_score = levenshtein_distance(game_data['config']['map_index'], game_data['user_map_path'])
                game_data_dict['dist_score'] = dist_score


            game_time = game_data['game_time']
            max_game_time = time_success_metric(version=version)
            is_time_success = 1 if int(game_time) < max_game_time else 0
            game_data_dict['game_time'] = game_time
            game_data_dict['is_time_success'] = is_time_success

            user_dialog, bot_dialog = analysis_game_chat(game_data['config']['game_role'], game_data['chat'])
            game_data_dict['user_num_of_uter'] = user_dialog['number of utterances']
            game_data_dict['user_mean_uter'] = user_dialog['mean utterance length']
            game_data_dict['user_total_uter'] = user_dialog['total number of tokens']

            game_data_dict['user_num_of_en'] = user_dialog['number of eng utterances']
            game_data_dict['user_num_of_es']= user_dialog['number of es utterances']
            game_data_dict['user_num_of_mix'] = user_dialog['number of mix utterances']
            game_data_dict['user_num_of_inter_cs'] = user_dialog['number of inter-sentential cs']
            game_data_dict['% entrainment - all dialog'] = user_dialog['% entrainment - all dialog']
            game_data_dict['% entrainment - on bot inter-sentential cs'] = user_dialog['% entrainment - on bot inter-sentential cs']

            game_data_dict['bot_num_of_uter'] = bot_dialog['number of utterances']
            game_data_dict['bot_mean_uter'] = bot_dialog['mean utterance length']
            game_data_dict['bot_total_uter'] = bot_dialog['total number of tokens']

            game_data_dict['bot_num_of_en'] = bot_dialog['number of eng utterances']
            game_data_dict['bot_num_of_es'] = bot_dialog['number of es utterances']
            game_data_dict['bot_num_of_mix'] = bot_dialog['number of mix utterances']
            game_data_dict['bot_num_of_inter_cs'] = bot_dialog['number of inter-sentential cs']


            for qa in game_data['survey']:
                question = qa['question']
                answer = qa['answer']

                if question in question_to_table:
                    game_data_dict[question] = answer

        df = pd.concat([df, pd.DataFrame.from_dict(game_data_dict, orient='index')], ignore_index=True)


read_games_data()