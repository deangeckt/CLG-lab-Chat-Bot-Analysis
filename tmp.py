import streamlit as st
from streamlit_elements import dashboard, mui, elements, html
from PIL import Image, ImageDraw, ImageFont
import json
import os
import datetime

root_folder = r"data/prolific/"

version_details = {'2.1.0_0_p': 'Rule Based navigator Bot',
                   '2.1.0_p': 'GPT based navigator bot. the human had 5 minutes timer',
                   '2.1.1_p': 'GPT based navigator bot. the human had 7 minutes timer',
                   '2.2.2_p': 'GPT based instructor bot. the human had 7 minutes timer'}
experiments_short_names = {'2.1.0_0_p': 'rb navigator',
                           '2.1.0_p': 'GPT navigator, 5',
                           '2.1.1_p': 'GPT navigator, 7',
                           '2.2.2_p': 'GPT instructor 7'}

def read_raw_data():
    data_list = []
    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')
        data = json.load(json_file)
        for game_data in data['games_data']:
            # fix chat times
            chat = game_data['chat']
            for chat_ele in chat:
                timestamp = chat_ele['timestamp']

                date_obj = datetime.datetime.fromtimestamp(timestamp / 1000.0)
                date_of_chat = date_obj.strftime("%D")
                chat_ele['time'] = date_obj.strftime("%H:%M:%S")
                data['date'] = date_of_chat

        data_list.append(data)
    return data_list


def foo(data_ele):
    curr = 'GPT instructor 7'
    short_name = experiments_short_names[data_ele['clinet_version']]
    return short_name == curr


data_list = read_raw_data()
fdata = list(filter(foo, data_list))
print(3)