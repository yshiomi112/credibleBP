from otree.api import *


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

    # ────────── WTP 質問 ──────────
    WTP = models.IntegerField(
        label="0〜200 の整数で入力してください:",
        min=0,
        max=200,
        blank=True
    )

    # ────────── BNT (数的推論テストなど) ──────────
    bnt_answer = models.IntegerField(
        label="0〜100 の整数で入力してください:",
        min=0,
        max=100,
        blank=True
    )
    bnt_correct = models.BooleanField()

    def grade_bnt(self):
        # 正解は 25%
        self.bnt_correct = (self.bnt_answer == 25)

    # ────────── BNT_2 ──────────
    bnt2_answer = models.IntegerField(
        label="0〜100 の整数で入力してください:",
        min=0,
        max=100,
        blank=True
    )
    bnt2_correct = models.BooleanField()

    def grade_bnt2(self):
        # 正解は 50%
        self.bnt2_correct = (self.bnt2_answer == 50)
