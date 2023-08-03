version_details = {'2.1.0_0_p': 'Rule Based navigator Bot - experiment #1',
                   '2.1.0_p': 'GPT based navigator bot - experiment #1. the human had 5 minutes timer',
                   '2.1.1_p': 'GPT based navigator bot - experiment #2. the human had 7 minutes timer',
                   '2.2.2_p': 'GPT based instructor bot - experiment #1. the human had 7 minutes timer',
                   '2.2.3_p': 'GPT based instructor bot - experiment #2. step by step prompt. the human had 7 minutes timer',
                   '2.2.4_p': 'Ins,Nav,Ins,Nav - 4 maps. English new instructions', # +retry mechanism when calling API
                   '2.2.5_p': 'Ins,Nav,Ins,Nav - 4 maps. Mixed new instructions - prolific failed to filter correct spanish',
                   '2.2.6_p': 'First - Spanish, Fluent - English. Mixed new instructions. (LOC - US)',
                   '2.2.7_p': 'First - English, Fluent - Spanish. Mixed new instructions. (LOC - US)',
                   }
experiments_short_names = {'2.1.0_0_p': 'RB navigator #1',
                           '2.1.0_p': 'GPT navigator #1',
                           '2.1.1_p': 'GPT navigator #2',
                           '2.2.2_p': 'GPT instructor #1',
                           '2.2.3_p': 'GPT instructor #2',
                           '2.2.4_p': 'Alternation #1',
                           '2.2.5_p': 'Alternation #2',
                           '2.2.6_p': 'Alternation #3'
                           }


def time_success_metric(short_name: str) -> int:
    if short_name == '2.1.0_0_p' or short_name == '2.1.0_p':
        return 300
    return 420


root_folder = r"data/prolific/"
