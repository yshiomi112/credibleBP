from otree.api import *
import random
from .models import C
from sender_receiver_game.models import C as GameC   # PRACTICE_ROUNDS を参照

class Survey(Page):
    form_model = 'player'
    def vars_for_template(self):
        is_sender = getattr(self.participant, 'role_fixed', None) == 'sender'
        return dict(is_sender=is_sender)

class WTP(Page):
    form_model  = 'player'
    form_fields = ['WTP']

    def vars_for_template(self):
        is_sender = getattr(self.participant, 'role_fixed', None) == 'sender'
        return dict(
            is_sender=is_sender,
            treatment=self.session.config.get('treatment'),  # ここを追加
        )

    # ★ Sender に割り当てられた参加者しか表示しない
    def is_displayed(self):
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

# ────────── BNT 2 ページ ──────────
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



class Inequity1(Page):
    #timeout_seconds = 120
    form_model  = 'player'
    form_fields = ['ineq_q1','ineq_q2','ineq_q3','ineq_q4','ineq_q5']

    def vars_for_template(self):
        is_sender = getattr(self.participant, 'role_fixed', None) == 'sender'
        # 左＝平等 (1000/1000)、右＝不平等 (800–1200/1300)
        return dict(
            is_sender=is_sender,
            pairs=[
            (1, '自分 1000円 / 相手 1000円', '自分 800円  / 相手 1300円'),
            (2, '自分 1000円 / 相手 1000円', '自分 900円  / 相手 1300円'),
            (3, '自分 1000円 / 相手 1000円', '自分 1000円 / 相手 1300円'),
            (4, '自分 1000円 / 相手 1000円', '自分 1100円 / 相手 1300円'),
            (5, '自分 1000円 / 相手 1000円', '自分 1200円 / 相手 1300円'),
        ])
    def before_next_page(self):
        if self.timeout_happened:
            # ここで「デフォルト値」をセット
            self.player.ineq_q1 = 'equal'
            self.player.ineq_q2 = 'equal'
            self.player.ineq_q3 = 'equal'
            self.player.ineq_q4 = 'equal'
            self.player.ineq_q5 = 'equal'

        answers = [
            self.player.ineq_q1,
            self.player.ineq_q2,
            self.player.ineq_q3,
            self.player.ineq_q4,
            self.player.ineq_q5,
        ]
        try:
            sp = answers.index('unequal') + 1   # 最初に左を選んだ行
        except ValueError:
            sp = 0                              # すべて右
        self.player.ineq_switch = sp

class Inequity2(Page):
    #timeout_seconds = 120
    form_model = 'player'
    form_fields = ['ineq2_q1', 'ineq2_q2', 'ineq2_q3', 'ineq2_q4', 'ineq2_q5']

    def vars_for_template(self):
        is_sender = getattr(self.participant, 'role_fixed', None) == 'sender'
        return dict(
            is_sender=is_sender,
            pairs=[
            (1, '自分 1000円 / 相手 1000円', '自分 800円  / 相手 700円'),
            (2, '自分 1000円 / 相手 1000円', '自分 900円  / 相手 700円'),
            (3, '自分 1000円 / 相手 1000円', '自分 1000円 / 相手 700円'),
            (4, '自分 1000円 / 相手 1000円', '自分 1100円 / 相手 700円'),
            (5, '自分 1000円 / 相手 1000円', '自分 1200円 / 相手 700円'),
        ])

    def before_next_page(self):
        if self.timeout_happened:
            # ここで「デフォルト値」をセット
            self.player.ineq2_q1 = 'equal'
            self.player.ineq2_q2 = 'equal'
            self.player.ineq2_q3 = 'equal'
            self.player.ineq2_q4 = 'equal'
            self.player.ineq2_q5 = 'equal'

        answers = [
            self.player.ineq2_q1,
            self.player.ineq2_q2,
            self.player.ineq2_q3,
            self.player.ineq2_q4,
            self.player.ineq2_q5,
        ]
        try:
            sp = answers.index('unequal') + 1   # 最初に左を選んだ行
        except ValueError:
            sp = 0                              # すべて右
        self.player.ineq2_switch = sp



class Risk(Page):
    #timeout_seconds = 120
    form_model  = 'player'
    form_fields = [f'risk_q{i}' for i in range(1,11)]

    def vars_for_template(self):
        is_sender = getattr(self.participant, 'role_fixed', None) == 'sender'
        # (行番号, 左くじ, 右くじ)
        pairs = [
            (1,  '10%で200円, 90%で160円',  '10%で385円, 90%で10円'),
            (2,  '20%で200円, 80%で160円',  '20%で385円, 80%で10円'),
            (3,  '30%で200円, 70%で160円',  '30%で385円, 70%で10円'),
            (4,  '40%で200円, 60%で160円',  '40%で385円, 60%で10円'),
            (5,  '50%で200円, 50%で160円',  '50%で385円, 50%で10円'),
            (6,  '60%で200円, 40%で160円',  '60%で385円, 40%で10円'),
            (7,  '70%で200円, 30%で160円',  '70%で385円, 30%で10円'),
            (8,  '80%で200円, 20%で160円',  '80%で385円, 20%で10円'),
            (9,  '90%で200円, 10%で160円',  '90%で385円, 10%で10円'),
            (10, '100%で200円, 0%で160円', '100%で385円, 0%で10円'),
        ]
        return dict(
            is_sender=is_sender,
            pairs=pairs)

    def before_next_page(self):

        if self.timeout_happened:
            self.player.risk_q1 = 'left'
            self.player.risk_q2 = 'left'
            self.player.risk_q3 = 'left'
            self.player.risk_q4 = 'left'
            self.player.risk_q5 = 'left'
            self.player.risk_q6 = 'left'
            self.player.risk_q7 = 'left'
            self.player.risk_q8 = 'left'
            self.player.risk_q9 = 'left'
            self.player.risk_q10 = 'left'

        answers = [getattr(self.player, f'risk_q{i}') for i in range(1,11)]
        # 最初に right が出た位置＋1 がスイッチポイント
        try:
            sp = answers.index('right') + 1
        except ValueError:
            sp = 11                      # 全部 left の場合
        self.player.risk_switch = sp




class FinalPayoffPage(Page):
    # 明示的にテンプレートを指定
    template_name = "survey/templates/survey/FinalPayoffPage.html"
    form_model, form_fields = 'player', []

    def vars_for_template(self):
        is_sender = getattr(self.participant, 'role_fixed', None) == 'sender'
        pr           = self.participant.vars['paying_round']
        game_pts_num = self.participant.vars.get(f'payoff_r{pr}', 0)   # ← 数値
        bonus_pts_num= self.participant.vars.get('lying_bonus', 0) if is_sender else 0
        total_pts = game_pts_num + bonus_pts_num

        rate  = self.session.config.get('real_world_currency_per_point', 1.0)
        base  = self.session.config.get('participation_fee', 0.0)
        money_add = int(total_pts * rate)
        money_total = int(base + money_add)

        label = f"ラウンド {pr - len(GameC.PRACTICE_ROUNDS)}"


        # Payments 画面と整合
        self.participant.payoff = total_pts

        return dict(
            is_sender          = is_sender,
            round_label        = label,
            gp                 = game_pts_num,     # ← 新しいキー
            bp                 = bonus_pts_num,    # ← 新しいキー
            rate               = rate,
            money_additional   = money_add,
            participation_fee  = int(base),
            total_money        = money_total,
        )


# ────────── ページ遷移順 ──────────
page_sequence = [
    Survey,
    WTP,
    BNT_1, BNT_2,
    Inequity1,
    Inequity2,
    Risk,
    FinalPayoffPage,
]