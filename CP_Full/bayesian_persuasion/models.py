from otree.api import *
import random

def epsilon_from_treatment(t):
    return 50 if t == 'CF' else -50             #関数epsilon_from_treatment(t)を定義

# ────────────────────────────────────────────
# 定数
# ────────────────────────────────────────────
class C(BaseConstants):
    NAME_IN_URL = 'bayesian_persuasion'
    PLAYERS_PER_GROUP = 2                       # Sender + Receiver
    NUM_ROUNDS = 22                             # 練習 2 + 本番 2（拡張可）
    PRACTICE_ROUNDS = [1, 2]                    # 練習ラウンド番号
    STATES   = ['Red', 'Blue']
    MESSAGES = ['r', 'b']
    ACTIONS  = ['red', 'blue']
    PRIOR    = {'Red': 0.3, 'Blue': 0.7}
    VS = 150
    VR = 150

# ────────────────────────────────────────────
# Subsession
# ────────────────────────────────────────────
class Subsession(BaseSubsession):  #各ラウンドで使うものを定義するクラス
    epsilon = models.IntegerField()

    #def creating_session(self): #ラウンド１開始時に全ての参加者のpayoffを0に
        #if self.round_number == 1:
            #for pp in self.session.get_participants():
                #pp.payoff = 0

    def is_main_round(self): #当該ラウンドが練習ラウンドでないならTrueそれ以外はFalse
        return self.round_number not in C.PRACTICE_ROUNDS

    def creating_session(self):
        # 0) 利得構造 ε を保存
        self.epsilon = epsilon_from_treatment(
            self.session.config.get('treatment', 'CF')
        )

        # 1) 本番支払ラウンドを Round1 で抽選
        if self.round_number == 1:
            mains = [r for r in range(1, C.NUM_ROUNDS + 1)
                     if r not in C.PRACTICE_ROUNDS]
            for pp in self.session.get_participants():
                pp.vars['paying_round'] = random.choice(mains)

        # 2) 練習ラウンド ─────────────────────
        if self.round_number in C.PRACTICE_ROUNDS:

            # Round1: ランダムペアを作成・保存、役割決定
            if self.round_number == C.PRACTICE_ROUNDS[0]:
                players = self.get_players()
                random.shuffle(players)
                matrix = [players[i:i + 2] for i in range(0, len(players), 2)]
                self.set_group_matrix(matrix)

                # 役割割り当て（id_in_group = 1 → Sender）
                for g in self.get_groups():
                    g.get_player_by_id(1).participant.practice_role = 'sender'
                    g.get_player_by_id(2).participant.practice_role = 'receiver'

                # ペア情報を保持（Round2 で再利用）
                self.session.vars['practice_matrix_ids'] = [
                    [p.id_in_subsession for p in row] for row in matrix
                ]

            # Round2: 同じペアで役割反転
            else:
                id_matrix = self.session.vars['practice_matrix_ids']
                matrix = [
                    [self.get_players()[pid - 1] for pid in row] for row in id_matrix
                ]
                self.set_group_matrix(matrix)

        # 3) 本番ラウンド ─────────────────────
        else:
            players = self.get_players()

            # 3-a) Round3（本番開始前）で固定役割を決定
            if self.round_number == min(set(range(1, C.NUM_ROUNDS + 1))
                                        - set(C.PRACTICE_ROUNDS)):
                participants = self.session.get_participants()
                half = len(participants) // 2
                roles = ['sender'] * half + ['receiver'] * (len(participants) - half)
                random.shuffle(roles)
                for pp, role in zip(participants, roles):
                    pp.role_fixed = role

            # 3-b) 毎ラウンド：Sender と Receiver を別々にシャッフルしてペア
            senders   = [p for p in players if p.participant.role_fixed == 'sender']
            receivers = [p for p in players if p.participant.role_fixed == 'receiver']

            # 参加者数が奇数の場合の安全策（あまりを無視する）
            min_len = min(len(senders), len(receivers))
            senders, receivers = senders[:min_len], receivers[:min_len]

            random.shuffle(senders)
            random.shuffle(receivers)
            matrix = [[s, r] for s, r in zip(senders, receivers)]
            self.set_group_matrix(matrix)

        # 4) 各 Player に役割をセット
        for p in self.get_players():
            p.set_role()


# ────────────────────────────────────────────
# Group
# ────────────────────────────────────────────
class Group(BaseGroup):
    state   = models.StringField(choices=C.STATES)
    message = models.StringField(choices=C.MESSAGES)

    def set_payoffs(self):
        players  = self.get_players()
        sender   = next((p for p in players if p.player_role == 'sender'), None)
        receiver = next((p for p in players if p.player_role == 'receiver'), None)

        # 送受信者が欠けていれば全員 0 点で終了
        if sender is None or receiver is None:
            for p in players:
                p.payoff = 0
            return

        # メッセージ送信
        r_given_R = sender.field_maybe_none('pi_r_given_R')
        r_given_B = sender.field_maybe_none('pi_r_given_B')
        prob_r = r_given_R if self.state == 'Red' else r_given_B
        self.message = random.choices(C.MESSAGES, weights=[prob_r, 1 - prob_r])[0]

        # 受信者行動
        a_if_r = receiver.field_maybe_none('action_if_r') or 'red'
        a_if_b = receiver.field_maybe_none('action_if_b') or 'red'
        action = a_if_r if self.message == 'r' else a_if_b
        receiver.chosen_action = action

        # 利得計算
        eps = self.subsession.epsilon
        if self.state == 'Red' and action == 'red':
            sender.payoff, receiver.payoff = C.VS + eps, C.VR
        elif self.state == 'Red' and action == 'blue':
            sender.payoff = receiver.payoff = 80
        elif self.state == 'Blue' and action == 'red':
            sender.payoff, receiver.payoff = C.VS - eps, 80
        else:
            sender.payoff, receiver.payoff = 80, C.VR


# ────────────────────────────────────────────
# Player
# ────────────────────────────────────────────
class Player(BasePlayer):

    # 送信者入力
    pi_r_given_R = models.FloatField(min=0, max=1, blank=True)
    pi_r_given_B = models.FloatField(min=0, max=1, blank=True)

    # 受信者入力
    action_if_r = models.StringField(
        choices=[('red', '赤玉'), ('blue', '青玉')], blank=True
    )
    action_if_b = models.StringField(
        choices=[('red', '赤玉'), ('blue', '青玉')], blank=True
    )

    chosen_action = models.StringField(choices=C.ACTIONS, blank=True)
    player_role   = models.StringField()          # 'sender' / 'receiver'

    # 役割決定ロジック（Subsession から呼び出し）
    def set_role(self):
        if self.round_number == C.PRACTICE_ROUNDS[0]:
            self.player_role = self.participant.practice_role
        elif self.round_number == C.PRACTICE_ROUNDS[1]:
            self.player_role = (
                'sender' if self.participant.practice_role == 'receiver'
                else 'receiver'
            )
        else:
            self.player_role = self.participant.role_fixed