from otree.api import *

# ============================================================
# models.py content
# ============================================================

doc = "事前理解度クイズ（問1〜問4）"


class C(BaseConstants):
    NAME_IN_URL = 'quiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # ───────────────────────────────────────────
    #  問1
    # ───────────────────────────────────────────
    q1_opt1 = models.BooleanField(
        label='参加者は「送信者」か「受信者」の役割にランダムに割り当てられる。',
        widget=widgets.CheckboxInput, blank=True)
    q1_opt2 = models.BooleanField(
        label='コンピュータは赤玉3個、青玉7個の中からランダムに1つの玉を引く。',
        widget=widgets.CheckboxInput, blank=True)
    q1_opt3 = models.BooleanField(
        label='コンピュータが引いた玉の色は、すぐに参加者に公開される。',
        widget=widgets.CheckboxInput, blank=True)
    q1_opt4 = models.BooleanField(
        label='本番20ラウンド中、同じペアで課題を繰り返す。',
        widget=widgets.CheckboxInput, blank=True)
    q1_opt5 = models.BooleanField(
        label='割り当てられた役割は、本番20ラウンド中変更されない。',
        widget=widgets.CheckboxInput, blank=True)
    q1_correct = models.BooleanField(initial=False)

    # ───────────────────────────────────────────
    #  問2
    # ───────────────────────────────────────────
    q2_opt1 = models.BooleanField(
        label='参加者が獲得できるポイントは、「コンピュータに引かれた玉の色」と「受信者が推測する玉の色」によって決まる。',
        widget=widgets.CheckboxInput, blank=True)
    q2_opt2 = models.BooleanField(
        label='受信者は玉の色を正しく推測した場合、150ポイントを獲得できる。',
        widget=widgets.CheckboxInput, blank=True)
    q2_opt3 = models.BooleanField(
        label='受信者が赤色を推測した場合、送信者は引かれた玉の色に関わらず100ポイントを得る。',
        widget=widgets.CheckboxInput, blank=True)
    q2_opt4 = models.BooleanField(
        label='受信者が青色を推測した場合、送信者は引かれた玉の色に関わらず80ポイントを得る。',
        widget=widgets.CheckboxInput, blank=True)
    q2_opt5 = models.BooleanField(
        label='送信者が獲得できるポイントは「受信者が赤色を推測した場合」のほうが「受信者が青色を推測した場合」よりも常に多い。',
        widget=widgets.CheckboxInput, blank=True)
    q2_correct = models.BooleanField(initial=False)

    # ───────────────────────────────────────────
    #  問3 (updated: 4 options)
    # ───────────────────────────────────────────
    q3_opt1 = models.BooleanField(
        label='受信者に送信されるメッセージは、引かれた玉の色とメッセージプランで設定した確率に従って送信される。',
        widget=widgets.CheckboxInput, blank=True)
    q3_opt2 = models.BooleanField(
        label='全体でのメッセージ送信確率は送信者が設計したメッセージプランに従って自動的に計算される。',
        widget=widgets.CheckboxInput, blank=True)
    q3_opt3 = models.BooleanField(
        label='送信者が設計したメッセージプランと全体でのメッセージ送信確率はともに受信者に公開される。',
        widget=widgets.CheckboxInput, blank=True)
    q3_opt4 = models.BooleanField(
        label='受信者は玉の色の推測の際に、送信されたメッセージを観察できる。',
        widget=widgets.CheckboxInput, blank=True)
    q3_correct = models.BooleanField(initial=False)

    # ───────────────────────────────────────────
    #  問4 (was 問5, 4 options)
    # ───────────────────────────────────────────
    q4_opt1 = models.BooleanField(
        label='追加報酬の換算には本番20ラウンドの中からランダムに選ばれた１ラウンドの結果が用いられる。',
        widget=widgets.CheckboxInput, blank=True)
    q4_opt2 = models.BooleanField(
        label='受信者は２種類の獲得ポイントが両方とも追加報酬に換算される。',
        widget=widgets.CheckboxInput, blank=True)
    q4_opt3 = models.BooleanField(
        label='１ポイント＝10円のレートで追加報酬に換算される。',
        widget=widgets.CheckboxInput, blank=True)
    q4_correct = models.BooleanField(initial=False)
