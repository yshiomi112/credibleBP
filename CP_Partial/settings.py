# settings.py
from os import environ

# ───────────────────────────────────────────
# セッション設定
# ───────────────────────────────────────────
SESSION_CONFIGS = [
    {
        'name': 'bp_experiment',
        'display_name': "Bayesian Persuasion Experiment",
        'num_demo_participants': 2,
        # ★アプリの実行順★
        'app_sequence': ['quiz', 'sender_receiver_game', 'survey'],
        'treatment': 'CP', #CP or NP
    },
]

# ───────────────────────────────────────────
# デフォルト（すべての SESSION_CONFIG に共通）
# ───────────────────────────────────────────
SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 10,   # 1 点 = 10 円
    'participation_fee': 1500,             # 参加報酬（定額）
    'doc': "",                             # ドキュメント欄（任意）
}

# ───────────────────────────────────────────
# 追加の participant / session 変数
# ───────────────────────────────────────────
PARTICIPANT_FIELDS = [
    'practice_role',
    'role_fixed',
    'lying_bonus',          # ←★追加：Lying ボーナス
]
SESSION_FIELDS = []

# ───────────────────────────────────────────
# グローバル設定
# ───────────────────────────────────────────
LANGUAGE_CODE = 'ja'   # UI 言語
REAL_WORLD_CURRENCY_CODE = 'JPY'
USE_POINTS = True

# ───────────────────────────────────────────
# 管理者ログイン
# ───────────────────────────────────────────
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


# ───────────────────────────────────────────
# その他
# ───────────────────────────────────────────
DEMO_PAGE_INTRO_HTML = ""   # デモ一覧ページの説明文（任意）
SECRET_KEY = 'xyz123'       # 適宜ランダム文字列に変更してください

# oTree 本体
INSTALLED_APPS = ['otree']

