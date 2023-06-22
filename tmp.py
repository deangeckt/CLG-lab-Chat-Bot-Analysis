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
                   '2.1.1_p': 'GPT based navigator bot the human had 7 minutes timer'}

experiments_short_names = {'2.1.0_0_p': 'rb navigator',
                           '2.1.0_p': 'GPT navigator, 5',
                           '2.1.1_p': 'GPT navigator, 7'}

import sys
from PIL import Image, ImageDraw, ImageFont
map_idx = 2

rows= 18
cols= 24

user_path = [
    {
        "r": 3,
        "c": 9
    },
    {
        "r": 4,
        "c": 9
    },
    {
        "r": 5,
        "c": 9
    },
    {
        "r": 6,
        "c": 9
    },
    {
        "r": 7,
        "c": 9
    },
    {
        "r": 7,
        "c": 10
    },
    {
        "r": 7,
        "c": 11
    },
    {
        "r": 7,
        "c": 12
    },
    {
        "r": 7,
        "c": 13
    },
    {
        "r": 7,
        "c": 14
    },
    {
        "r": 7,
        "c": 13
    },
]

with Image.open(f"maps/map{map_idx+1}_1.jpg") as im:
    fnt = ImageFont.truetype("font/arial.ttf", 40)

    draw = ImageDraw.Draw(im)
    width, height = im.size
    col_size = width / cols
    row_size = height / rows
    for idx, user_coord in enumerate(user_path):
        color = ''
        if idx % 4 == 0:
            color = 'white'
        elif idx % 4 == 1:
            color = 'red'
        elif idx % 4 == 2:
            color = 'blue'
        else:
            color = 'orange'
        row = user_coord['r']
        col = user_coord['c']
        text = f'{idx+1}'
        x = col_size * col
        y = row_size * row
        draw.text((x, y), text, font=fnt, fill=color)

    im.show()
    # im.save(sys.stdout, "PNG")