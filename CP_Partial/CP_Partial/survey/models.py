from otree.api import *


# 共通 choices 定義
INEQ_CHOICES = [
    ('unequal', '不平等案'),   # 自分 800〜1200円 / 相手 1300円
    ('equal',   '平等案'),     # 自分 1000円 / 相手 1000円
]

# くじの左右
RISK_CHOICES = [('left', '左くじ'), ('right', '右くじ')]

class C(BaseConstants):
    NAME_IN_URL        = 'survey'
    PLAYERS_PER_GROUP  = None
    NUM_ROUNDS         = 1
    NUM_CARDS          = 10
    MULTIPLIER         = 10          # 申告数字×10 pt

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    WTP = models.IntegerField(
        label="0〜200 の整数で入力してください:",
        min=0,
        max=200,
        blank=True
    )

    # カード番号（1〜10）— JS で入力、フォームに含める
    selected_card = models.IntegerField(min=1, max=10, blank=True)

    # 自己申告数字
    reported_number = models.IntegerField(
        label="カードに書かれていた数字を自己申告してください（1〜10）:",
        min=1, max=10
    )

    bonus_points = models.IntegerField()
    prev_points  = models.IntegerField()

    def set_bonus(self):
        self.bonus_points = self.reported_number * C.MULTIPLIER
        self.prev_points  = int(self.participant.payoff)
        self.participant.payoff += self.bonus_points
        self.participant.vars['lying_bonus'] = self.bonus_points



    # ────────── BNT 回答 ──────────
    bnt_answer = models.IntegerField(
        label="0〜100 の整数で入力してください:",
        min=0,
        max=100,
        blank=True
    )
    bnt_correct = models.BooleanField()   # 正誤

    def grade_bnt(self):
        self.bnt_correct = (self.bnt_answer == 25)   # 正解は 25 %


    bnt2_answer = models.IntegerField(
        label="0〜100 の整数で入力してください:",
        min=0, max=100, blank=True
    )
    bnt2_correct = models.BooleanField()

    def grade_bnt2(self):
        self.bnt2_correct = (self.bnt2_answer == 50)  # 正解 50 %

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


