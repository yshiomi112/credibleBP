from otree.api import *
import random
from .models import C
from bayesian_persuasion.models import C as GameC   # PRACTICE_ROUNDS を参照


class Preference(Page):
    form_model, form_fields = 'player', []

    def vars_for_template(self):
        is_sender = getattr(self.participant, 'role_fixed', None) == 'sender'
        return dict(
            is_sender=is_sender,
        )


class Inequity1(Page):
    #timeout_seconds = 120
    form_model  = 'player'
    form_fields = ['ineq_q1','ineq_q2','ineq_q3','ineq_q4','ineq_q5']

    def vars_for_template(self):
        is_sender = getattr(self.participant, 'role_fixed', None) == 'sender'
        # 左＝平等 (1000/1000)、右＝不平等 (800–1200/1300)
        return dict(
            is_sender = is_sender,
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
            (1,  '10%で820円, 90%で660円',  '10%で1590円, 90%で40円'),
            (2,  '20%で820円, 80%で660円',  '20%で1590円, 80%で40円'),
            (3,  '30%で820円, 70%で660円',  '30%で1590円, 70%で40円'),
            (4,  '40%で820円, 60%で660円',  '40%で1590円, 60%で40円'),
            (5,  '50%で820円, 50%で660円',  '50%で1590円, 50%で40円'),
            (6,  '60%で820円, 40%で660円',  '60%で1590円, 40%で40円'),
            (7,  '70%で820円, 30%で660円',  '70%で1590円, 30%で40円'),
            (8,  '80%で820円, 20%で660円',  '80%で1590円, 20%で40円'),
            (9,  '90%で820円, 10%で660円',  '90%で1590円, 10%で40円'),
            (10, '100%で820円, 0%で660円', '100%で1590円, 0%で40円'),
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


# ─────────────────────────────────────────
# ★ 新規：preference インセンティブ計算 WaitPage
# ─────────────────────────────────────────
class PrefIncentiveCompute(WaitPage):
    wait_for_all_groups = True
    title_text = "お待ちください"
    body_text = "他の参加者が選択を終えるまでお待ちください。"

    def after_all_players_arrive(self):
        players = self.subsession.get_players()
        shuffled = players[:]
        random.shuffle(shuffled)

        n = len(shuffled)
        half = n // 2
        ineq_players = shuffled[:half]
        risk_players = shuffled[half:]

        # Ineq が奇数なら最後の1名を Risk へ移動（安全弁）
        if len(ineq_players) % 2 == 1:
            risk_players.append(ineq_players.pop())

        # グループ保存
        for p in ineq_players:
            p.participant.vars['pref_group'] = 'Ineq'
        for p in risk_players:
            p.participant.vars['pref_group'] = 'Risk'

        # ── Ineq：ペアリング → 役割 → 問題抽選 → 円額確定 ──
        amount_list = [800, 900, 1000, 1100, 1200]
        pair_id = 0
        for i in range(0, len(ineq_players), 2):
            a = ineq_players[i]
            b = ineq_players[i + 1]
            pair_id += 1

            # 役割
            roles = ['自分', '相手']
            random.shuffle(roles)
            a.participant.vars['pref_role'] = roles[0]
            b.participant.vars['pref_role'] = roles[1]
            a.participant.vars['pref_show_role'] = True
            b.participant.vars['pref_show_role'] = True

            # 10問から1問（1-5: 質問1, 6-10: 質問2）
            choice = random.randint(1, 10)
            if choice <= 5:
                qnum, idx = 1, choice
            else:
                qnum, idx = 2, choice - 5

            for p in (a, b):
                pv = p.participant.vars
                pv['pref_question'] = qnum
                pv['pref_index'] = idx
                pv['pref_pair_id'] = pair_id
                # ラベルの割り当てを変更：
                # 質問1 -> 質問1a
                # 質問2 -> 質問1b
                if qnum == 1:
                    pv['pref_question_label'] = '質問1a'
                else:
                    pv['pref_question_label'] = '質問1b'

            # 「自分」役の回答を取得
            self_player = a if a.participant.vars['pref_role'] == '自分' else b
            other_player = b if self_player is a else a

            if qnum == 1:
                ans = getattr(self_player, f'ineq_q{idx}')
                if ans == 'equal':
                    self_amt, other_amt = 1000, 1000
                else:
                    self_amt, other_amt = amount_list[idx - 1], 1300
            else:  # qnum == 2
                ans = getattr(self_player, f'ineq2_q{idx}')
                if ans == 'equal':
                    self_amt, other_amt = 1000, 1000
                else:
                    self_amt, other_amt = amount_list[idx - 1], 700

            self_player.participant.vars['pref_amount_yen'] = int(self_amt)
            other_player.participant.vars['pref_amount_yen'] = int(other_amt)

        # ── Risk：各参加者ごとに抽選・実行 ──
        for p in risk_players:
            idx = random.randint(1, 10)
            choice = getattr(p, f'risk_q{idx}')
            prob = idx / 10.0
            r = random.random()

            if choice == 'left':
                amount = 820 if r < prob else 660
            else:
                amount = 1590 if r < prob else 40

            pv = p.participant.vars
            pv['pref_question'] = 3
            pv['pref_index'] = idx
            pv['pref_pair_id'] = None
            pv['pref_role'] = None
            pv['pref_show_role'] = False
            pv['pref_amount_yen'] = int(amount)
            # ラベルの割り当てを変更：
            # 質問3 -> 質問2
            pv['pref_question_label'] = '質問2'

        # ── Payments を PrefIncentiveCompute 終了時点で最終額に更新 ──
        rate = self.session.config.get('real_world_currency_per_point', 1.0)  # 例: 1pt=10円
        for p in self.subsession.get_players():
            pp = p.participant
            pr = pp.vars.get('paying_round')
            game_pts = int(pp.vars.get(f'payoff_r{pr}', 0))           # ゲームの支払ラウンドのポイント
            pref_yen = int(pp.vars.get('pref_amount_yen', 0))         # preference の円額
            pref_pts = int(round(pref_yen / rate))                    # 円→ポイント
            pp.payoff = game_pts + pref_pts                           # Payments の Payoff(bonus) に反映

    def is_displayed(self):
        # 1ラウンドのみ（このアプリは1ラウンド想定）
        return True


# ────────── ページ遷移順 ──────────
page_sequence = [
    Preference,
    Inequity1,
    Inequity2,
    Risk,
    PrefIncentiveCompute,   # ★追加
]
