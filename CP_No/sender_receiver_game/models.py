from otree.api import *
import random, math


# ──────────────────────────
# 補助関数
# ──────────────────────────
def epsilon_from_treatment(treatment_code: str) -> int:
    """treatment が CN なら +50、NN なら -50 を返す"""
    return 50 if treatment_code == 'CN' else -50


# ──────────────────────────
# 定数
# ──────────────────────────
class C(BaseConstants):
    NAME_IN_URL       = 'sender_receiver_game'
    PLAYERS_PER_GROUP = 2

    NUM_MAIN_ROUNDS   = 12
    PRACTICE_ROUNDS   = [1, 2]
    NUM_ROUNDS        = NUM_MAIN_ROUNDS + len(PRACTICE_ROUNDS)

    STATES   = ['Red', 'Blue']
    MESSAGES = ['r', 'b']
    ACTIONS  = ['red', 'blue']

    PRIOR = {'Red': .3, 'Blue': .7}
    VS, VR = 150, 150


# ──────────────────────────
# Subsession
# ──────────────────────────
class Subsession(BaseSubsession):
    epsilon = models.IntegerField()

    def creating_session(self):
        # ε を treatment から決定
        self.epsilon = epsilon_from_treatment(
            self.session.config.get('treatment', 'CN')
        )

        # Round 1 で RIS ラウンド抽選
        if self.round_number == 1:
            for pp in self.session.get_participants():
                pp.payoff = 0
                mains = [r for r in range(1, C.NUM_ROUNDS + 1) if r not in C.PRACTICE_ROUNDS]
                pp.vars['paying_round'] = random.choice(mains)

        # ─── 練習ラウンド設定 ───
        if self.round_number in C.PRACTICE_ROUNDS:
            if self.round_number == C.PRACTICE_ROUNDS[0]:
                # 練習①：ランダムペア＋役割付与
                players = self.get_players()
                random.shuffle(players)
                matrix = [players[i:i + 2] for i in range(0, len(players), 2)]
                self.set_group_matrix(matrix)
                for g in self.get_groups():
                    g.get_player_by_id(1).participant.practice_role = 'sender'
                    g.get_player_by_id(2).participant.practice_role = 'receiver'
                # 後の練習②用に id を保存
                self.session.vars['practice_matrix_ids'] = [
                    [p.id_in_subsession for p in row] for row in matrix
                ]
            else:
                # 練習②：同じペアで役割反転
                id_matrix = self.session.vars['practice_matrix_ids']
                matrix = [[self.get_players()[pid - 1] for pid in row] for row in id_matrix]
                self.set_group_matrix(matrix)

        # ─── 本番ラウンド設定 ───
        else:
            players = self.get_players()
            first_main = min(set(range(1, C.NUM_ROUNDS + 1)) - set(C.PRACTICE_ROUNDS))

            # 一度だけ固定役割を決定
            if self.round_number == first_main:
                parts = self.session.get_participants()
                half  = len(parts) // 2
                roles = ['sender'] * half + ['receiver'] * (len(parts) - half)
                random.shuffle(roles)
                for pp, role in zip(parts, roles):
                    pp.role_fixed = role

            # 各ラウンドで sender / receiver を別々にシャッフル
            senders   = [p for p in players if p.participant.role_fixed == 'sender']
            receivers = [p for p in players if p.participant.role_fixed == 'receiver']
            min_len   = min(len(senders), len(receivers))
            senders, receivers = senders[:min_len], receivers[:min_len]
            random.shuffle(senders); random.shuffle(receivers)
            self.set_group_matrix([[s, r] for s, r in zip(senders, receivers)])

        # 役割フラグをセット（練習①ではまだ practice_role が無い可能性がある）
        for p in self.get_players():
            p.set_role()


# ──────────────────────────
# Group
# ──────────────────────────
class Group(BaseGroup):
    state   = models.StringField(choices=C.STATES)
    message = models.StringField(choices=C.MESSAGES)

    def set_payoffs(self):
        s = next(p for p in self.get_players() if p.player_role == 'sender')
        r = next(p for p in self.get_players() if p.player_role == 'receiver')

        # ① π₁ に基づきメッセージ抽選
        prob_r = s.pi1_r_given_R if self.state == 'Red' else s.pi1_r_given_B
        self.message = random.choices(C.MESSAGES, weights=[prob_r, 1 - prob_r])[0]

        # ② 受信者行動
        act = r.action_if_r if self.message == 'r' else r.action_if_b
        r.chosen_action = act

        # ③ ペイオフ
        eps = self.subsession.epsilon
        if self.state == 'Red' and act == 'red':
            s.payoff, r.payoff = C.VS + eps, C.VR
        elif self.state == 'Red':
            s.payoff = r.payoff = 80
        elif self.state == 'Blue' and act == 'red':
            s.payoff, r.payoff = C.VS - eps, 80
        else:
            s.payoff, r.payoff = 80, C.VR

        # ④ 推測スコア（π₁ と hat π）
        rR, rB, hat_rR = s.pi1_r_given_R, s.pi1_r_given_B, r.hat_pi_r_given_R
        if None not in (rR, rB, hat_rR):
            m = C.PRIOR['Red'] * rR + C.PRIOR['Blue'] * rB
            rR_min = max(0, (m - C.PRIOR['Blue']) / C.PRIOR['Red'])
            rR_max = min(1,  m / C.PRIOR['Red'])
            L = max((rR_max - rR_min) ** 2, 1e-6)
            r.prediction_points = math.ceil(max(80, 150 - 1120 * (rR - hat_rR) ** 2 / L))

        # ⑤ RIS 用保存
        for p in self.get_players():
            key = f'payoff_r{p.round_number}'
            if p.player_role == 'receiver':
                p.participant.vars[key] = (
                    r.prediction_points if random.random() < .5 else p.payoff
                )
            else:
                p.participant.vars[key] = p.payoff


# ──────────────────────────
# Player
# ──────────────────────────
class Player(BasePlayer):
    # 送信者プラン π₁
    pi1_r_given_R = models.FloatField(min=0, max=1, blank=True, null=True)
    pi1_r_given_B = models.FloatField(min=0, max=1, blank=True, null=True)

    # 受信者行動
    action_if_r = models.StringField(choices=[('red', '赤玉'), ('blue', '青玉')], blank=True)
    action_if_b = models.StringField(choices=[('red', '赤玉'), ('blue', '青玉')], blank=True)
    chosen_action = models.StringField(choices=C.ACTIONS, blank=True)

    # 受信者推測
    hat_pi_r_given_R = models.FloatField(min=0, max=1, blank=True, null=True)
    hat_pi_r_given_B = models.FloatField(min=0, max=1, blank=True, null=True)
    prediction_points = models.FloatField(blank=True)

    # 内部フラグ
    player_role = models.StringField()

    # 周辺確率 (補助)
    @property
    def marginal_r(self):
        rR = self.pi1_r_given_R or .5
        rB = self.pi1_r_given_B or .5
        return C.PRIOR['Red'] * rR + C.PRIOR['Blue'] * rB

    # 役割決定（KeyError 保険付き）
    def set_role(self):
        if self.round_number == C.PRACTICE_ROUNDS[0]:
            pr = getattr(self.participant, 'practice_role', None)
            self.player_role = pr if pr else 'sender'        # 未設定なら仮に sender
        elif self.round_number == C.PRACTICE_ROUNDS[1]:
            pr = getattr(self.participant, 'practice_role', None)
            self.player_role = 'sender' if pr == 'receiver' else 'receiver'
        else:
            self.player_role = self.participant.role_fixed

