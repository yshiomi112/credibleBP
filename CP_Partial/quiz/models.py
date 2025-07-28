from otree.api import *

doc = "事前理解度クイズ（問1〜問5）"


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
        label='本番12ラウンド中、同じペアで課題を繰り返す。',
        widget=widgets.CheckboxInput, blank=True)
    q1_opt5 = models.BooleanField(
        label='割り当てられた役割は、本番12ラウンド中変更されない。',
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
    #  問3
    # ───────────────────────────────────────────
    q3_opt1 = models.BooleanField(
        label='受信者に送信されるメッセージは、修正後のメッセージプランから送信される。',
        widget=widgets.CheckboxInput, blank=True)
    q3_opt2 = models.BooleanField(
        label='全体でのメッセージ送信確率は、修正前後で変更されない。',
        widget=widgets.CheckboxInput, blank=True)
    q3_opt3 = models.BooleanField(
        label='送信者はメッセージプランを自由に修正できる。',
        widget=widgets.CheckboxInput, blank=True)
    q3_opt4 = models.BooleanField(
        label='修正後のメッセージプランは受信者に公開される。',
        widget=widgets.CheckboxInput, blank=True)
    q3_opt5 = models.BooleanField(
        label='ステージ１でのメッセージプランと全体でのメッセージ送信確率は受信者に公開される。',
        widget=widgets.CheckboxInput, blank=True)
    q3_correct = models.BooleanField(initial=False)

    # ───────────────────────────────────────────
    #  問4
    # ───────────────────────────────────────────
    q4_opt1 = models.BooleanField(
        label='受信者の課題は「玉の色の推測」と「修正後のメッセージプランの推測」の２つである。',
        widget=widgets.CheckboxInput, blank=True)
    q4_opt2 = models.BooleanField(
        label='送信者が公開したメッセージプランは、ステージ２で送信者が修正する可能性がある。',
        widget=widgets.CheckboxInput, blank=True)
    q4_opt3 = models.BooleanField(
        label='送信者が公開した全体でのメッセージ送信確率は、ステージ２で送信者が修正する可能性がある。',
        widget=widgets.CheckboxInput, blank=True)
    q4_opt4 = models.BooleanField(
        label='受信者は、玉の色の推測に応じて獲得できるポイントとは別に、修正後のメッセージプランの推測の精度に応じて、ポイントを獲得することができる。',
        widget=widgets.CheckboxInput, blank=True)
    q4_opt5 = models.BooleanField(
        label='受信者は玉の色の推測の際に、送信されたメッセージを観察できる。',
        widget=widgets.CheckboxInput, blank=True)
    q4_correct = models.BooleanField(initial=False)

    # ───────────────────────────────────────────
    #  問5（選択肢 4 個）
    # ───────────────────────────────────────────
    q5_opt1 = models.BooleanField(
        label='追加報酬の換算には本番12ラウンドの中からランダムに選ばれた１ラウンドの結果が用いられる。',
        widget=widgets.CheckboxInput, blank=True)
    q5_opt2 = models.BooleanField(
        label='受信者は２種類の獲得ポイントが両方とも追加報酬に換算される。',
        widget=widgets.CheckboxInput, blank=True)
    q5_opt3 = models.BooleanField(
        label='１ポイント＝10円のレートで追加報酬に換算される。',
        widget=widgets.CheckboxInput, blank=True)
    q5_correct = models.BooleanField(initial=False)
