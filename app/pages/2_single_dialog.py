import streamlit as st
from streamlit_elements import dashboard, mui, elements, html
from PIL import Image
import json
import os
import datetime

# root_folder = r"data/gpt_bot_navigator/english/"
root_folder = r"data/prolific/"

version_details = {'2.1.0_0_p': 'Rule Based navigator Bot',
                   '2.1.0_p': 'GPT based navigator bot. the human had 5 minutes timer',
                   '2.1.1_p': 'GPT based navigator bot the human had 7 minutes timer'}

def read_raw_data():
    data_list = []
    for file_name in os.listdir(root_folder):
        json_file = open(os.path.join(root_folder, file_name), encoding='utf8')
        data = json.load(json_file)
        for game_data in data['games_data']:
            chat = game_data['chat']
            for chat_ele in chat:
                timestamp = chat_ele['timestamp']

                date_obj = datetime.datetime.fromtimestamp(timestamp / 1000.0)
                date_of_chat = date_obj.strftime("%D")
                chat_ele['time'] = date_obj.strftime("%H:%M:%S")
                data['date'] = date_of_chat

        data_list.append(data)
    return data_list


data_list = read_raw_data()
st.set_page_config(page_title="singleDialog", page_icon="📈  ", layout="wide")
st.sidebar.success("Single Dialog")


if 'file_idx' not in st.session_state:
    st.session_state.file_idx = 0
if 'game_idx' not in st.session_state:
    st.session_state.game_idx = 0


def next_call_click():
    if st.session_state.file_idx == len(data_list) - 1:
        return
    st.session_state.file_idx += 1
    st.session_state.game_idx = 0

def last_call_click():
    if st.session_state.file_idx == 0:
        return
    st.session_state.file_idx -= 1
    st.session_state.game_idx = 0

def next_game_click():
    games_data = data_list[st.session_state.file_idx]['games_data']
    if st.session_state.game_idx == len(games_data) - 1:
        return
    st.session_state.game_idx += 1

def last_game_click():
    if st.session_state.game_idx == 0:
        return
    st.session_state.game_idx -= 1


st.header(f'Call: {st.session_state.file_idx+1}/{len(data_list)}')
map_img_col, general_info_col, nav_btns_col = st.columns([0.4,0.4,0.4])

with map_img_col:
    map_idx = st.session_state.game_idx
    image = Image.open(f"maps/map{map_idx+1}_1.jpg")
    st.image(image, width=450, caption=f'Map: {map_idx+1}')


with general_info_col:
    call_data = data_list[st.session_state.file_idx]
    curr_game_data = call_data['games_data'][st.session_state.game_idx]
    client_version = call_data['clinet_version']

    st.subheader('General info')
    st.markdown(f"Human role: {curr_game_data['config']['game_role']} 🧭")
    st.text(f"Experiment: {version_details.get(client_version, '')}")
    st.text(f"Code-switch strategy: {call_data['cs_strategy']} ")
    st.text(f"Date: {call_data['date']} 📅")
    st.text(f"Game time: {curr_game_data['game_time']} seconds ⌛")
    st.text(f"Client version: {client_version} ")
    st.text(f"Server Version: {call_data['server_version']} ")
    st.text(f"Prolific id: {call_data['prolific']['prolific_id']} ")


with nav_btns_col:
    st.subheader('Navigate')

    prev_col, next_col = st.columns([0.5, 0.5])
    with prev_col:
        last_call = st.button('⏮️ Previous Call ', on_click=last_call_click)
        last_game = st.button('⏮️⏮️ Previous Map', on_click=last_game_click)
    with next_col:
        next_call = st.button('Next Call ⏭️️', on_click=next_call_click)
        next_game = st.button('Next Map ⏭️⏭️️', on_click=next_game_click)


def render_chat():
    curr_chat = data_list[st.session_state.file_idx]['games_data'][st.session_state.game_idx]['chat']
    with mui.Paper(key="dialog", sx={
                "display": 'flex',
                "flexDirection": 'column',
                "overflowY": 'auto'}):
        with mui.Typography:
            for chat_ele in curr_chat:
                side = 'flex-end' if chat_ele['id'] == 'navigator' else 'flex-start'
                textAlign = 'end' if chat_ele['id'] == 'navigator' else 'start'
                bg_color = 'rgb(72, 70, 68)' if chat_ele['id'] == 'navigator' else 'rgb(63, 81, 181)'
                html.div(
                    html.div(
                        html.p(f"{chat_ele['id']}: ", css={'fontWeight':'700'}),
                        html.p(f"{chat_ele['msg']}"),
                        html.p(f"{chat_ele['time']}", css={'font-size':'14px', 'margin-bottom': '14px'}),
                        css={
                            "display": "flex",
                            "gap": '0.5em',
                            "align-items": 'center',
                            "padding": '0.5em',
                            "margin": '0.5em',
                            'color': 'white',
                            'background-color': bg_color,
                            'border-radius': '8px',
                            'width': 'fit-content',
                            'text-align': textAlign
                        },
                    ),
                    css={
                        "display": "flex",
                        'justify-content': side,
                    }
                )

def render_survey(dash_key: str):
    call_data = data_list[st.session_state.file_idx]
    curr_game_data = call_data['games_data'][st.session_state.game_idx]

    survey_header = 'General survey:' if dash_key == 'general_survey' else 'Game survey:'
    survey_data = call_data['general_survey'] if dash_key == 'general_survey' else curr_game_data['survey']

    with mui.Paper(key=dash_key, sx={
                "display": 'flex',
                "flexDirection": 'column',
                "overflowY": 'auto'}):
        html.p(f'{survey_header}', css={'font-size':'18px', 'fontWeight':'700'})
        for qa in survey_data:
            html.div(
                html.p(f"Q: {qa['question']}", css={'margin': '0.5em'}),
                html.p(f"A: {qa['answer']}", css={'margin': '0.5em'}),
                css={
                    "display": "flex",
                    "flexDirection": 'column',
                    "width": 'fit-content',
                    'border-bottom': '1px solid gray',
                    'margin': '0.5em'
                },
            )

with elements("dashboard"):
    layout = [
        # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
        # https://react-grid-layout.github.io/react-grid-layout/examples/0-showcase.html
        dashboard.Item("general_survey", 0, 0, 4, 3, isDraggable=False, moved=False, isResizable=False),
        dashboard.Item("dialog", 4, 0, 6, 3, isDraggable=False, moved=False, isResizable=False),
        dashboard.Item("game_survey", 0, 6, 10, 3, isDraggable=False, moved=False, isResizable=False),

    ]

    with dashboard.Grid(layout):
        render_survey('general_survey')
        render_survey('game_survey')
        render_chat()
