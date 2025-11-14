from otree.api import *
import random
import math


def epsilon_from_treatment(t):
    return 50 if t == 'CP' else -50

# ────────────────────────────────────────────
# 定数
# ────────────────────────────────────────────
class C(BaseConstants):
    NAME_IN_URL        = 'sender_receiver_game'
    PLAYERS_PER_GROUP  = 2
    NUM_MAIN_ROUNDS    = 20           # ★本番ラウンド数をここで調整★
    PRACTICE_ROUNDS    = [1, 2]      # 練習ラウンド
    STATES   = ['Red', 'Blue']
    MESSAGES = ['r', 'b']
    ACTIONS  = ['red', 'blue']
    PRIOR    = {'Red': 0.3, 'Blue': 0.7}
    VS, VR = 150, 150
    NUM_ROUNDS         = len(PRACTICE_ROUNDS) + NUM_MAIN_ROUNDS







# ────────────────────────────────────────────
# Subsession
# ────────────────────────────────────────────
class Subsession(BaseSubsession):
    epsilon = models.IntegerField()

    def creating_session(self):
        # 利得構造 ε の保存
        self.epsilon = epsilon_from_treatment(
            self.session.config.get('treatment', 'CP')
        )

        # Round 1 で累積 payoff をリセット & RIS ラウンド抽選
        if self.round_number == 1:
            for pp in self.session.get_participants():
                pp.payoff = 0
                mains = [
                    r for r in range(1, C.NUM_ROUNDS + 1)
                    if r not in C.PRACTICE_ROUNDS
                ]
                pp.vars['paying_round'] = random.choice(mains)

        # 練習ラウンド
        if self.round_number in C.PRACTICE_ROUNDS:

            # 練習1：ランダムペア・役割決め
            if self.round_number == C.PRACTICE_ROUNDS[0]:
                players = self.get_players()
                random.shuffle(players)
                matrix = [
                    players[i : i + 2] for i in range(0, len(players), 2)
                ]
                self.set_group_matrix(matrix)
                for g in self.get_groups():
                    g.get_player_by_id(1).participant.practice_role = 'sender'
                    g.get_player_by_id(2).participant.practice_role = 'receiver'
                self.session.vars['practice_matrix_ids'] = [
                    [p.id_in_subsession for p in row] for row in matrix
                ]

            # 練習2：同ペアで役割反転
            else:
                id_matrix = self.session.vars['practice_matrix_ids']
                matrix = [
                    [self.get_players()[pid - 1] for pid in row]
                    for row in id_matrix
                ]
                self.set_group_matrix(matrix)

        # 本番ラウンド
        else:
            players = self.get_players()
            first_main = min(
                set(range(1, C.NUM_ROUNDS + 1)) - set(C.PRACTICE_ROUNDS)
            )

            # 本番開始前に固定役割を決定（1回だけ）
            if self.round_number == first_main:
                participants = self.session.get_participants()
                half = len(participants) // 2
                roles = ['sender'] * half + ['receiver'] * (len(participants) - half)
                random.shuffle(roles)
                for pp, role in zip(participants, roles):
                    pp.role_fixed = role

            # 毎ラウンド：役割固定のまま Sender/Receiver を別々にシャッフル
            senders = [p for p in players if p.participant.role_fixed == 'sender']
            receivers = [p for p in players if p.participant.role_fixed == 'receiver']
            min_len = min(len(senders), len(receivers))
            senders, receivers = senders[:min_len], receivers[:min_len]
            random.shuffle(senders)
            random.shuffle(receivers)
            self.set_group_matrix([[s, r] for s, r in zip(senders, receivers)])

        # 最後に各 Player に player_role をセット
        for p in self.get_players():
            p.set_role()


# ────────────────────────────────────────────
# Group
# ────────────────────────────────────────────
class Group(BaseGroup):
    state   = models.StringField(choices=C.STATES)
    message = models.StringField(choices=C.MESSAGES)

    def set_payoffs(self):
        sender = next(p for p in self.get_players() if p.player_role == 'sender')
        receiver = next(p for p in self.get_players() if p.player_role == 'receiver')

        # ① メッセージ送信（修正版プラン π₂ を使用）
        prob_r = (
            sender.pi2_r_given_R
            if self.state == 'Red'
            else sender.pi2_r_given_B
        )
        self.message = random.choices(C.MESSAGES, weights=[prob_r, 1 - prob_r])[0]

        # ② 受信者行動
        action = (
            receiver.action_if_r
            if self.message == 'r'
            else receiver.action_if_b
        )
        receiver.chosen_action = action

        # ③ ペイオフ計算
        eps = self.subsession.epsilon
        if self.state == 'Red' and action == 'red':
            sender.payoff, receiver.payoff = C.VS + eps, C.VR
        elif self.state == 'Red':
            sender.payoff = receiver.payoff = 80
        elif self.state == 'Blue' and action == 'red':
            sender.payoff, receiver.payoff = C.VS - eps, 80
        else:
            sender.payoff, receiver.payoff = 80, C.VR

        # ④ 推測ポイント計算
        # 安全なスコア計算ブロック
        rR = sender.pi2_r_given_R
        rB = sender.pi2_r_given_B
        hat_rR = receiver.hat_pi_r_given_R

        if rR is not None and rB is not None and hat_rR is not None:
            marginal = C.PRIOR['Red'] * rR + C.PRIOR['Blue'] * rB
            rR_min = max(0, (marginal - C.PRIOR['Blue']) / C.PRIOR['Red'])
            rR_max = min(1, marginal / C.PRIOR['Red'])
            L = (rR_max - rR_min) ** 2 if (rR_max - rR_min) > 0 else 1e-6
            sqR = (rR - hat_rR) ** 2
            score = 150 - 1120 * (sqR / L)
            receiver.prediction_points = math.ceil(max(80, score))

        # Group.set_payoffs の最後
        for p in self.get_players():
            key = f'payoff_r{p.round_number}'
            if p.player_role == 'receiver':
                # 50% で信念 or ゲーム
                if random.random() < 0.5:
                    p.participant.vars[key] = p.prediction_points
                else:
                    p.participant.vars[key] = p.payoff
            else:
                p.participant.vars[key] = p.payoff


# ────────────────────────────────────────────
# Player
# ────────────────────────────────────────────
class Player(BasePlayer):

    # ---- 送信者：初期プラン ----
    pi1_r_given_R = models.FloatField(min=0, max=1, blank=True, null=True)
    pi1_r_given_B = models.FloatField(min=0, max=1, blank=True, null=True)

    # ---- 送信者：修正版プラン ----
    pi2_r_given_R = models.FloatField(min=0, max=1, blank=True, null=True)
    pi2_r_given_B = models.FloatField(min=0, max=1, blank=True, null=True)

    # ---- 受信者：行動入力 ----
    action_if_r = models.StringField(choices=[('red', '赤玉'), ('blue', '青玉')], blank=True)
    action_if_b = models.StringField(choices=[('red', '赤玉'), ('blue', '青玉')], blank=True)
    chosen_action = models.StringField(choices=C.ACTIONS, blank=True)

    # ---- 受信者：修正版プラン推測 ----
    hat_pi_r_given_R = models.FloatField(min=0, max=1, blank=True, null=True)
    hat_pi_r_given_B = models.FloatField(min=0, max=1, blank=True, null=True)
    prediction_points = models.FloatField(blank=True)

        # ---- 役割フラグ ----
    player_role = models.StringField()

    @property
    def marginal_r_initial(self):
        r_R = self.field_maybe_none('pi1_r_given_R') or 0.5
        r_B = self.field_maybe_none('pi1_r_given_B') or 0.5
        return C.PRIOR['Red'] * r_R + C.PRIOR['Blue'] * r_B

    @property
    def marginal_r_revision(self):
        r_R = self.field_maybe_none('pi2_r_given_R')
        r_B = self.field_maybe_none('pi2_r_given_B')
        if r_R is None or r_B is None:
            return None
        return C.PRIOR['Red'] * r_R + C.PRIOR['Blue'] * r_B

    # ---- 役割決定ロジック ----
    def set_role(self):
        if self.round_number == C.PRACTICE_ROUNDS[0]:
            self.player_role = self.participant.practice_role
        elif self.round_number == C.PRACTICE_ROUNDS[1]:
            self.player_role = (
                'sender'
                if self.participant.practice_role == 'receiver'
                else 'receiver'
            )
        else:
            self.player_role = self.participant.role_fixed

