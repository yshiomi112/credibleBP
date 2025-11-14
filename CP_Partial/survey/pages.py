from otree.api import *
import random
from .models import C
from sender_receiver_game.models import C as GameC   # PRACTICE_ROUNDS を参照


class Survey(Page):
    form_model, form_fields = 'player', []

    def vars_for_template(self):
        is_sender = getattr(self.participant, 'role_fixed', None) == 'sender'
        return dict(is_sender=is_sender)


class WTP(Page):
    form_model  = 'player'
    form_fields = ['WTP']

    def vars_for_template(self):
        is_sender = getattr(self.participant, 'role_fixed', None) == 'sender'
        return dict(
            treatment=self.session.config.get('treatment'),
            is_sender=is_sender,
        )

    # ★ Sender に割り当てられた参加者しか表示しない
    def is_displayed(self):
        # sender_receiver_game の本番準備中に participant.role_fixed がセット済み
        return getattr(self.participant, 'role_fixed', None) == 'sender'

    def error_message(self, values):
        if values.get('WTP') is None:
            return "0〜200 の整数で回答してください。"


class BNT_1(Page):
    form_model  = 'player'
    form_fields = ['bnt_answer']

    def vars_for_template(self):
        is_sender = getattr(self.participant, 'role_fixed', None) == 'sender'
        return dict(is_sender=is_sender)

    def error_message(self, values):
        if values.get('bnt_answer') is None:
            return "0〜100 の整数で回答してください。"

    def before_next_page(self):
        self.player.grade_bnt()


class BNT_2(Page):
    form_model  = 'player'
    form_fields = ['bnt2_answer']

    def vars_for_template(self):
        is_sender = getattr(self.participant, 'role_fixed', None) == 'sender'
        return dict(is_sender=is_sender)

    def error_message(self, values):
        if values.get('bnt2_answer') is None:
            return "0〜100 の整数で回答してください。"

    def before_next_page(self):
        self.player.grade_bnt2()


class FinalPayoffPage(Page):
    # 明示的にテンプレートを指定
    template_name = "survey/templates/survey/FinalPayoffPage.html"
    form_model, form_fields = 'player', []

    def vars_for_template(self):
        is_sender = getattr(self.participant, 'role_fixed', None) == 'sender'

        # 実験パート1（ゲーム）の支払ラウンド
        pr = self.participant.vars['paying_round']
        game_pts_num = self.participant.vars.get(f'payoff_r{pr}', 0)  # 数値（ポイント）

        # 実験パート2（preference）の情報（PrefIncentiveComputeで保存済み）
        pv = self.participant.vars
        pref_group   = pv.get('pref_group')                 # "Ineq" / "Risk" / None
        pref_q       = pv.get('pref_question')              # 1/2/3 / None
        pref_idx     = pv.get('pref_index')                 # int / None
        pref_role    = pv.get('pref_role')                  # "自分"/"相手"/None
        pref_amount  = int(pv.get('pref_amount_yen', 0))    # 円

        # ラベルは保存済みがあればそれを、なければフォールバック辞書で決める
        # 質問1 -> 質問1a
        # 質問2 -> 質問1b
        # 質問3 -> 質問2
        pref_question_label = pv.get('pref_question_label') or {
            1: '質問1a',
            2: '質問1b',
            3: '質問2',
        }.get(pref_q, '—')

        pref_show_role = bool(pv.get('pref_show_role', (pref_q in (1, 2) and pref_role)))

        # 換金
        rate = self.session.config.get('real_world_currency_per_point', 1.0)
        base = self.session.config.get('participation_fee', 0.0)

        money_add   = int(game_pts_num * rate)                  # 実験パート1（ゲーム）の換金額（円）
        money_total = int(base + money_add + pref_amount)       # 参加費 + ゲーム換金 + preference円

        # 「ラウンド X」表記（練習ラウンド分を引く）
        label = f"ラウンド {pr - len(GameC.PRACTICE_ROUNDS)}"

        # 重要：participant.payoff は PrefIncentiveCompute で最終確定済み。ここでは上書きしない。

        return dict(
            is_sender          = is_sender,
            round_label        = label,
            gp                 = game_pts_num,      # ゲームポイント
            rate               = rate,
            participation_fee  = int(base),
            money_additional   = money_add,         # ゲーム由来の追加報酬（円）
            total_money        = money_total,

            # ▼ preference 表示用
            pref_group          = pref_group,
            pref_question       = pref_q,
            pref_index          = pref_idx,
            pref_role           = pref_role,
            pref_amount_yen     = pref_amount,
            pref_question_label = pref_question_label,
            pref_show_role      = pref_show_role,
        )


# ────────── ページ遷移順 ──────────
page_sequence = [
    Survey,
    WTP,
    BNT_1, BNT_2,
    FinalPayoffPage,
]
