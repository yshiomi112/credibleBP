from otree.api import *


# 共通 choices 定義
INEQ_CHOICES = [
    ('unequal', '不平等案'),   # 自分 800〜1200円 / 相手 1300円
    ('equal',   '平等案'),     # 自分 1000円 / 相手 1000円
]

# くじの左右
RISK_CHOICES = [('left', '左くじ'), ('right', '右くじ')]

class C(BaseConstants):
    NAME_IN_URL        = 'preference'
    PLAYERS_PER_GROUP  = None
    NUM_ROUNDS         = 1
    NUM_CARDS          = 10
    MULTIPLIER         = 10          # 申告数字×10 pt

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):



    # ────────── Inequity Aversion (5 問) ──────────
    # Inequity 5 問
    ineq_q1 = models.StringField(choices=INEQ_CHOICES, blank=True)
    ineq_q2 = models.StringField(choices=INEQ_CHOICES, blank=True)
    ineq_q3 = models.StringField(choices=INEQ_CHOICES, blank=True)
    ineq_q4 = models.StringField(choices=INEQ_CHOICES, blank=True)
    ineq_q5 = models.StringField(choices=INEQ_CHOICES, blank=True)

    # ★ 新フィールド：スイッチングポイント (1-6)
    ineq_switch = models.IntegerField()


    # ── Inequity 2 ──★ NEW
    ineq2_q1 = models.StringField(choices=INEQ_CHOICES, blank=True)
    ineq2_q2 = models.StringField(choices=INEQ_CHOICES, blank=True)
    ineq2_q3 = models.StringField(choices=INEQ_CHOICES, blank=True)
    ineq2_q4 = models.StringField(choices=INEQ_CHOICES, blank=True)
    ineq2_q5 = models.StringField(choices=INEQ_CHOICES, blank=True)
    ineq2_switch = models.IntegerField()



    # Risk (10 問)
    risk_q1  = models.StringField(choices=RISK_CHOICES, blank=True)
    risk_q2  = models.StringField(choices=RISK_CHOICES, blank=True)
    risk_q3  = models.StringField(choices=RISK_CHOICES, blank=True)
    risk_q4  = models.StringField(choices=RISK_CHOICES, blank=True)
    risk_q5  = models.StringField(choices=RISK_CHOICES, blank=True)
    risk_q6  = models.StringField(choices=RISK_CHOICES, blank=True)
    risk_q7  = models.StringField(choices=RISK_CHOICES, blank=True)
    risk_q8  = models.StringField(choices=RISK_CHOICES, blank=True)
    risk_q9  = models.StringField(choices=RISK_CHOICES, blank=True)
    risk_q10 = models.StringField(choices=RISK_CHOICES, blank=True)

    risk_switch = models.IntegerField()   # 1-11 (右→左に切替わる位置)


