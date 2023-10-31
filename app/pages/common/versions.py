version_details = {
    '2.1.0_0_p': 'Rule Based navigator Bot - experiment #1',
    '2.1.0_p': 'GPT based navigator bot - experiment #1. the human had 5 minutes timer',
    '2.1.1_p': 'GPT based navigator bot - experiment #2. the human had 7 minutes timer',
    '2.2.2_p': 'GPT based instructor bot - experiment #1. the human had 7 minutes timer',
    '2.2.3_p': 'GPT based instructor bot - experiment #2. step by step prompt. the human had 7 minutes timer',
    '2.2.4_p': 'Ins,Nav,Ins,Nav - 4 maps. English new instructions',  # +retry mechanism when calling API
    '2.2.5_p': 'Ins,Nav,Ins,Nav - 4 maps. Mixed new instructions - prolific failed to filter correct spanish',
    '2.2.6_p': 'First - Spanish, Fluent - English. Mixed new instructions. (LOC - US)',
    '2.2.7_p': 'First - English, Fluent - Spanish. Mixed new instructions. (LOC - US)',
    '2.3.0_p': 'GPT 4 + informal prompts. Fluent - ES || EN. Mixed new instructions. prolific add in ES only. (LOC - US). new Navigation mechanism.',
    '2.3.1_p': 'BASELINE (Alternation #6 - fix to ES only, in US)',
    '2.3.2_p': 'Random Code-switch alternation strategy - switch on the turn level',
    '2.3.3_p': 'Short-context based Code-switch alternation strategy - switch on the utterance level',
    '2.3.4_p': 'Switch Last User based Code-switch alternation strategy - switch on the turn level'
}

experiments_short_names = {
    '2.1.0_0_p': 'RB navigator #1',
    '2.1.0_p': 'GPT navigator #1',
    '2.1.1_p': 'GPT navigator #2',
    '2.2.2_p': 'GPT instructor #1',
    '2.2.3_p': 'GPT instructor #2',
    '2.2.4_p': 'Alternation #1',
    '2.2.5_p': 'Alternation #2',
    '2.2.6_p': 'Alternation #3',
    '2.2.7_p': 'Alternation #4',
    '2.3.0_p': 'Alternation #5',
    '2.3.1_p': 'Baseline',
    '2.3.2_p': 'Random CS #1',
    '2.3.3_p': 'Short-context CS #1',
    '2.3.4_p': 'Switch Last User CS #1',
}


def time_success_metric(version: str) -> int:
    if version == '2.1.0_0_p' or version == '2.1.0_p':
        return 300
    return 420


root_folder = r"data/prolific_lang_ids"
