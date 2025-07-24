from os import environ

SESSION_CONFIGS = [
    {
        'name': 'bp_test',
        'display_name': "Bayesian Persuasion Full",
        'num_demo_participants': 2,
        'app_sequence': ['quiz', 'bayesian_persuasion', 'survey'],
        'treatment': 'CF',  # 'CF' または 'NF'
    },
]

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 10,
    'participation_fee': 1500,
    'doc': "",
}

PARTICIPANT_FIELDS = [
    'practice_role',   # 練習ラウンド1でランダム役割 → 2ラウンド目で反転
    'role_fixed',      # 本番用に固定した役割
]
SESSION_FIELDS = []

LANGUAGE_CODE = 'ja'
REAL_WORLD_CURRENCY_CODE = 'JPY'
USE_POINTS = True


ROOMS = [
    dict(name="pclab", display_name="pclab", participant_label_file="_rooms/pclab.txt")
]

# ROOMS = [
#     dict(
#         name='econ101',
#         display_name='Econ 101 class',
#         participant_label_file='_rooms/econ101.txt',
#     ),
#     dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
# ]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = ""
SECRET_KEY = 'xyz123'

INSTALLED_APPS = ['otree']