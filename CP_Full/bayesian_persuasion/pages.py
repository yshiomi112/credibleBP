from otree.api import *
from .models import C
import random

# ══════════ 共通関数 ═════════════════════════════════
def round_label(player):
    if player.round_number in C.PRACTICE_ROUNDS:
        idx = C.PRACTICE_ROUNDS.index(player.round_number) + 1
        return f"練習ラウンド {idx}"
    idx = player.round_number - len(C.PRACTICE_ROUNDS)
    return f"ラウンド {idx}"

def show_next_button(r):
    return (r != max(C.PRACTICE_ROUNDS)) and (r != C.NUM_ROUNDS)

# ══════════ 役割確認 (練習 / 本番前) ═════════════════
class RolePractice(Page):
    form_model, form_fields = 'player', []
    def is_displayed(self): return self.round_number in C.PRACTICE_ROUNDS
    def vars_for_template(self):
        role_jp = '送信者' if self.player.player_role=='sender' else '受信者'
        return dict(round_label=round_label(self.player), role_jp=role_jp)

class RoleMain(Page):
    form_model, form_fields = 'player', []
    def is_displayed(self):
        first_main = min(set(range(1,C.NUM_ROUNDS+1))-set(C.PRACTICE_ROUNDS))
        return self.round_number == first_main
    def vars_for_template(self):
        role_jp = '送信者' if self.player.player_role=='sender' else '受信者'
        return dict(role_jp=role_jp)

class RoleIntroWait(WaitPage):
    wait_for_all_groups=True
    title_text,body_text="しばらくお待ちください","他の参加者をお待ちください"
    def is_displayed(self):
        first_main=min(set(range(1,C.NUM_ROUNDS+1))-set(C.PRACTICE_ROUNDS))
        return self.round_number in (*C.PRACTICE_ROUNDS,first_main)

# ══════════ Sender ══════════════════════════════════
class SenderPage(Page):
    #timeout_seconds = 10                     # 動作確認用
    form_model,form_fields='player',['pi_r_given_R','pi_r_given_B']
    def is_displayed(self): return self.player.player_role=='sender'
    def vars_for_template(self): return dict(round_label=round_label(self.player))
    def error_message(self,values):
        if values['pi_r_given_R'] is None or values['pi_r_given_B'] is None:
            return '両方の確率を入力してください。'
    def before_next_page(self):
        if self.timeout_happened:
            self.player.pi_r_given_R = 0.5
            self.player.pi_r_given_B = 0.5


class WaitSender(WaitPage): pass

# ══════════ Receiver ════════════════════════════════
class ReceiverPage(Page):
    form_model,form_fields='player',['action_if_r','action_if_b']
    def is_displayed(self): return self.player.player_role=='receiver'
    def vars_for_template(self):
        sender = next(p for p in self.group.get_players() if p.player_role=='sender')
        r_r = sender.field_maybe_none('pi_r_given_R'); r_b = sender.field_maybe_none('pi_r_given_B')
        if r_r is None: r_r=0.5
        if r_b is None: r_b=0.5
        prior_r,prior_b=C.PRIOR['Red'],C.PRIOR['Blue']
        marg_r=round(100*(r_r*prior_r+r_b*prior_b))
        return dict(
            round_label=round_label(self.player),
            pi_r_given_R=int(r_r*100), pi_r_given_B=int(r_b*100),
            pi_b_given_R=100-int(r_r*100), pi_b_given_B=100-int(r_b*100),
            marginal_r=marg_r, marginal_b=100-marg_r,
        )
    def before_next_page(self):
        if self.timeout_happened:
            self.player.action_if_r='red'; self.player.action_if_b='red'
class WaitReceiver(WaitPage): pass

# ══════════ 利得計算 & 調整 ══════════════════════════
class MyWaitPage(WaitPage):
    wait_for_all_groups=False
    def after_all_players_arrive(self):
        g=self.group
        g.state=random.choices(C.STATES,weights=[C.PRIOR['Red'],C.PRIOR['Blue']])[0]
        g.set_payoffs()

        for pl in g.get_players():
            # 本番ラウンドは保存
            if self.round_number not in C.PRACTICE_ROUNDS:
                pl.participant.vars[f'payoff_r{self.round_number}']=pl.payoff

            # ─── 支払対象外ラウンドなら即差し引く ───
            if self.round_number != pl.participant.vars['paying_round']:
                pl.participant.payoff -= pl.payoff   # 加算分を打ち消す

class RoundSyncWaitPage(WaitPage):
    wait_for_all_groups=True
    title_text,body_text="お待ちください","他のペアが選択を終えるまで、しばらくお待ちください…"

# ══════════ 結果ページ ══════════════════════════════
# ① ──────────────────────────────────────────
# 追加：練習ラウンド専用結果ページ
# ────────────────────────────────────────────
class PracticeResults(Page):
    """練習 1・2 専用。Next ボタン表示は既存の show_next_button に従う"""
    form_model, form_fields = 'player', []
    template_name = 'bayesian_persuasion/ResultsPage.html'

    def is_displayed(self):
        return self.round_number in C.PRACTICE_ROUNDS

    def vars_for_template(self):
        players   = self.group.get_players()
        sender    = next(p for p in players if p.player_role == 'sender')
        receiver  = next(p for p in players if p.player_role == 'receiver')
        return dict(
            round_label     = round_label(self.player),
            state           = self.group.state,
            message         = self.group.field_maybe_none('message') or '—',
            chosen_action   = receiver.chosen_action or '—',
            sender_payoff   = sender.payoff,
            receiver_payoff = receiver.payoff,
            show_next       = show_next_button(self.round_number),
            practice_done=self.round_number == max(C.PRACTICE_ROUNDS),
            main_done=False,  # 練習ラウンドでは本番終了ではない
        )

    # ボタン制御（練習2では None を返してボタン非表示）
    def get_form_fields(self):
        return [] if not show_next_button(self.round_number) else None


# ② ──────────────────────────────────────────
# 既存 ResultsPage は「本番ラウンド専用」に限定
# ────────────────────────────────────────────
class ResultsPage(Page):
    form_model, form_fields = 'player', []
    template_name = 'bayesian_persuasion/ResultsPage.html'

    def is_displayed(self):
        return self.round_number not in C.PRACTICE_ROUNDS

    def vars_for_template(self):
        players   = self.group.get_players()
        sender    = next(p for p in players if p.player_role == 'sender')
        receiver  = next(p for p in players if p.player_role == 'receiver')
        return dict(
            round_label     = round_label(self.player),
            state           = self.group.state,
            message         = self.group.field_maybe_none('message') or '—',
            chosen_action   = receiver.chosen_action or '—',
            sender_payoff   = sender.payoff,
            receiver_payoff = receiver.payoff,
            show_next       = show_next_button(self.round_number),
            practice_done=self.round_number == max(C.PRACTICE_ROUNDS),
            main_done=(self.round_number == C.NUM_ROUNDS),
        )

    def get_form_fields(self):
        return [] if not show_next_button(self.round_number) else None

class AfterResultsWait(WaitPage):
    wait_for_all_groups=True
    title_text,body_text="お待ちください","次のラウンドを待っています…"






# ══════════ ページシーケンス ═════════════════════════
page_sequence=[
    RolePractice,RoleMain,RoleIntroWait,
    SenderPage,WaitSender,
    ReceiverPage,WaitReceiver,
    MyWaitPage, PracticeResults,
    ResultsPage,AfterResultsWait,
]
