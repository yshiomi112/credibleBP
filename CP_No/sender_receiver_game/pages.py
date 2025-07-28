from otree.api import *
from .models import C
import random

# ────────── 共通ヘルパー ──────────
def round_label(player):
    if player.round_number in C.PRACTICE_ROUNDS:
        idx = C.PRACTICE_ROUNDS.index(player.round_number) + 1
        return f"練習ラウンド {idx}"
    idx = player.round_number - len(C.PRACTICE_ROUNDS)
    return f"ラウンド {idx}"

def show_next_button(r):
    return (r != max(C.PRACTICE_ROUNDS)) and (r != C.NUM_ROUNDS)

# ────────── 役割確認（練習／本番冒頭） ──────────
class RolePractice(Page):
    def is_displayed(self): return self.round_number in C.PRACTICE_ROUNDS
    def vars_for_template(self):
        role_jp = '送信者' if self.player.player_role == 'sender' else '受信者'
        return dict(round_label=round_label(self.player), role_jp=role_jp)

class RoleMain(Page):
    def is_displayed(self):
        first_main = min(set(range(1, C.NUM_ROUNDS + 1)) - set(C.PRACTICE_ROUNDS))
        return self.round_number == first_main
    def vars_for_template(self):
        role_jp = '送信者' if self.player.player_role == 'sender' else '受信者'
        return dict(role_jp=role_jp)

class RoleIntroWait(WaitPage):
    wait_for_all_groups = True
    def is_displayed(self):
        first_main = min(set(range(1, C.NUM_ROUNDS + 1)) - set(C.PRACTICE_ROUNDS))
        return self.round_number in (*C.PRACTICE_ROUNDS, first_main)

# ────────── 送信者：初期プラン設計 ──────────
class SenderPage(Page):
    form_model = 'player'
    form_fields = ['pi1_r_given_R', 'pi1_r_given_B']
    def is_displayed(self): return self.player.player_role == 'sender'
    def before_next_page(self):
        if self.timeout_happened:
            self.player.pi1_r_given_R = 0.5
            self.player.pi1_r_given_B = 0.5
    def vars_for_template(self):
        rR = self.player.field_maybe_none('pi1_r_given_R') or 0.5
        rB = self.player.field_maybe_none('pi1_r_given_B') or 0.5
        return dict(
            round_label=round_label(self.player),
            pi1_r_given_R=int(rR * 100),
            pi1_r_given_B=int(rB * 100),
        )

class WaitSender(WaitPage):
    pass

# ────────── 受信者：行動戦略入力 ──────────
class ReceiverPage(Page):
    form_model = 'player'
    form_fields = ['action_if_r', 'action_if_b']
    def is_displayed(self): return self.player.player_role == 'receiver'
    def before_next_page(self):
        if self.timeout_happened:
            self.player.action_if_r = 'red'
            self.player.action_if_b = 'red'
    def vars_for_template(self):
        sender = next(p for p in self.group.get_players() if p.player_role == 'sender')
        rR = sender.pi1_r_given_R if sender.pi1_r_given_R is not None else 0.5
        rB = sender.pi1_r_given_B if sender.pi1_r_given_B is not None else 0.5
        prior_r, prior_b = C.PRIOR['Red'], C.PRIOR['Blue']
        m_r = prior_r * rR + prior_b * rB
        m_pct = int(round(100 * m_r))
        return dict(
            round_label=round_label(self.player),
            marginal_r=m_pct,
            marginal_b=100 - m_pct,
        )


class WaitReceiver(WaitPage):
    pass

# ────────── 受信者：π1に基づくプラン推測 ──────────
class ReceiverPredict(Page):
    form_model = 'player'
    form_fields = ['hat_pi_r_given_R', 'hat_pi_r_given_B']
    def is_displayed(self): return self.player.player_role == 'receiver'
    def before_next_page(self):
        if self.timeout_happened:
            self.player.hat_pi_r_given_R = 0.5
            self.player.hat_pi_r_given_B = 0.5
    def vars_for_template(self):
        sender = next(p for p in self.group.get_players() if p.player_role == 'sender')
        init_R = sender.pi1_r_given_R if sender.pi1_r_given_R is not None else 0.5
        init_B = sender.pi1_r_given_B if sender.pi1_r_given_B is not None else 0.5
        PR, PB = C.PRIOR['Red'], C.PRIOR['Blue']
        marginal = init_R * PR + init_B * PB
        m_pct = int(round(marginal * 100))
        rR_min = max(0, (marginal - PB) / PR) * 100
        rR_max = min(1, marginal / PR) * 100
        rB_min = max(0, (marginal - PR) / PB) * 100
        rB_max = min(1, marginal / PB) * 100
        return dict(
            round_label=round_label(self.player),
            init_r_given_R=int(init_R * 100),
            init_r_given_B=int(init_B * 100),
            marginal_r_initial=m_pct,
            marginal_b_initial=100 - m_pct,
            PRIOR_R=PR,
            PRIOR_B=PB,
            rR_min=rR_min,
            rR_max=rR_max,
            rB_min=rB_min,
            rB_max=rB_max,
        )
    def error_message(self, values):
        if values.get('hat_pi_r_given_R') is None or values.get('hat_pi_r_given_B') is None:
            return '両方の確率を入力してください。'

# ────────── メッセージ抽選＆ペイオフ計算 ──────────
class WaitResults(WaitPage):
    def after_all_players_arrive(self):
        self.group.state = random.choices(
            C.STATES, weights=[C.PRIOR['Red'], C.PRIOR['Blue']]
        )[0]
        self.group.set_payoffs()

# ────────── 結果表示 ──────────
class ResultsPage(Page):
    template_name = 'sender_receiver_game/ResultsPage.html'
    def vars_for_template(self):
        players = self.group.get_players()
        sender = next(p for p in players if p.player_role == 'sender')
        receiver = next(p for p in players if p.player_role == 'receiver')
        chosen = receiver.field_maybe_none('chosen_action') or '—'
        data = dict(
            round_label=round_label(self.player),
            state=self.group.field_maybe_none('state') or '—',
            message=self.group.field_maybe_none('message') or '—',
            chosen_action=chosen,
            sender_payoff=sender.payoff,
            receiver_payoff=receiver.payoff,
            show_next=show_next_button(self.round_number),
            prediction_points_fmt=None,
            practice_done=(self.round_number == max(C.PRACTICE_ROUNDS)),
            main_done=(self.round_number == C.NUM_ROUNDS),
        )
        if self.player.player_role == 'receiver' and receiver.prediction_points is not None:
            data['prediction_points_fmt'] = int(receiver.prediction_points) \
                if receiver.prediction_points == int(receiver.prediction_points) \
                else round(receiver.prediction_points, 2)
        return data
    def get_form_fields(self):
        return [] if not show_next_button(self.round_number) else None


class WaitRound(WaitPage):
    wait_for_all_groups = True

# ────────── ページ遷移順 ──────────
page_sequence = [
    RolePractice, RoleMain, RoleIntroWait,
    SenderPage, WaitSender,
    ReceiverPage, ReceiverPredict,
    WaitResults, ResultsPage, WaitRound,
]
