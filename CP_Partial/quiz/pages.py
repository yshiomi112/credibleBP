from otree.api import *
from .models import C, Subsession, Group, Player


# ─────────────────────────────────────────────
# 共通ミックスイン（重複ロジックをまとめる）
# ─────────────────────────────────────────────
class MultiSelectMixin(Page):

    question_num: int                  # サブクラスで設定
    correct_set: set                   #   〃
    option_labels: list                #   〃
    explanations: dict                 #   〃  { idx : exp_str }（正解には含めない）

    def error_message(self, values):
        selected = {i for i, f in enumerate(self.form_fields, 1) if values[f]}

        if (selected - self.correct_set):
            return '誤った選択肢が選択されています。実験説明を読み直し、もう一度回答して下さい。'
        if not self.correct_set.issubset(selected):
            return '正しい選択肢を全て選んでください'

    def before_next_page(self):
        selected = {i for i, f in enumerate(self.form_fields, 1)
                    if getattr(self.player, f)}
        setattr(self.player, f'q{self.question_num}_correct',
                selected == self.correct_set)


class ExplainMixin(Page):

    question_num: int                  # サブクラスで設定
    option_labels: list                #   〃
    explanations: dict                 #   〃

    def is_displayed(self):
        return getattr(self.player, f'q{self.question_num}_correct')

    def vars_for_template(self):
        opts = []
        for idx, text in enumerate(self.option_labels, 1):
            if idx in self.explanations:               # 誤答
                opts.append({
                    'text': text,
                    'result': '誤',
                    'exp': self.explanations[idx],
                })
            else:                                      # 正解
                opts.append({
                    'text': text,
                    'result': '正',
                    'exp': '',        # 正解は解説なし
                })
        return dict(options=opts)


# ─────────────────────────────────────────────
#  問1
# ─────────────────────────────────────────────
class Q1(MultiSelectMixin):
    question_num = 1
    form_model = 'player'
    form_fields = [f'q1_opt{i}' for i in range(1, 6)]
    correct_set = {1, 2, 5}
    option_labels = [
        '参加者は「送信者」か「受信者」の役割にランダムに割り当てられる。',
        'コンピュータは赤玉3個、青玉7個の中からランダムに1つの玉を引く。',
        'コンピュータが引いた玉の色は、すぐに参加者に公開される。',
        '本番12ラウンド中、同じペアで課題を繰り返す。',
        '割り当てられた役割は、本番12ラウンド中変更されない。',
    ]
    explanations = {
        3: '送信者、受信者ともにそのラウンドの結果が公開されるまで、玉の色を知ることはできません。',
        4: '毎ラウンドごとに、相手がランダムに変わる仕組みになっています。',
    }


class Explanation1(ExplainMixin):
    question_num = 1
    option_labels = Q1.option_labels
    explanations = Q1.explanations


# ─────────────────────────────────────────────
#  問2
# ─────────────────────────────────────────────
class Q2(MultiSelectMixin):
    question_num = 2
    form_model = 'player'
    form_fields = [f'q2_opt{i}' for i in range(1, 6)]
    correct_set = {1, 2, 4, 5}
    option_labels = [
        '参加者が獲得できるポイントは、「引かれた玉の色」と「受信者が推測する玉の色」によって決まる。',
        '受信者は玉の色を正しく推測した場合、150ポイントを獲得できる。',
        '受信者が赤色を推測した場合、送信者は引かれた玉の色に関わらず100ポイントを得る。',
        '受信者が青色を推測した場合、送信者は引かれた玉の色に関わらず80ポイントを得る。',
        '送信者が獲得できるポイントは「受信者が赤色を推測した場合」のほうが「受信者が青色を推測した場合」よりも常に多い。',
    ]
    explanations = {
        3: '送信者の獲得ポイントは玉の色に応じて 100 または 200 になります。',
    }


class Explanation2(ExplainMixin):
    question_num = 2
    option_labels = Q2.option_labels
    explanations = Q2.explanations


# ─────────────────────────────────────────────
#  問3
# ─────────────────────────────────────────────
class Q3(MultiSelectMixin):
    question_num = 3
    form_model = 'player'
    form_fields = [f'q3_opt{i}' for i in range(1, 6)]
    correct_set = {1, 2, 5}
    option_labels = [
        '受信者に送信されるメッセージは、修正後のメッセージプランから送信される。',
        '全体でのメッセージ送信確率は、修正前後で変更されない。',
        '送信者はメッセージプランを自由に修正できる。',
        '修正後のメッセージプランは受信者に公開される。',
        'ステージ１でのメッセージプランと全体でのメッセージ送信確率は受信者に公開される。',
    ]
    explanations = {
        3: '修正は全体でのメッセージ送信確率がステージ１で公開したメッセージプランと一致する範囲内に制限されています。',
        4: '修正後のメッセージプランは受信者に公開されません。',
    }


class Explanation3(ExplainMixin):
    question_num = 3
    option_labels = Q3.option_labels
    explanations = Q3.explanations


# ─────────────────────────────────────────────
#  問4
# ─────────────────────────────────────────────
class Q4(MultiSelectMixin):
    question_num = 4
    form_model = 'player'
    form_fields = [f'q4_opt{i}' for i in range(1, 6)]
    correct_set = {1, 2, 4}
    option_labels = [
        '受信者の課題は「玉の色の推測」と「修正後のメッセージプランの推測」の２つである。',
        '送信者が公開したメッセージプランは、ステージ２で送信者が修正する可能性がある。',
        '送信者が公開した全体でのメッセージ送信確率は、ステージ２で送信者が修正する可能性がある。',
        '受信者は、玉の色の推測に応じて獲得できるポイントとは別に、修正後のメッセージプランの推測の精度に応じて、ポイントを獲得することができる。',
        '受信者は玉の色の推測の際に、送信されたメッセージを観察できる。',
    ]
    explanations = {
        3: '送信者はメッセージプランは修正できますが、全体でのメッセージ送信確率を変更することはできません。',
        5: '受信者はメッセージを観察せずに、メッセージが「赤色」である場合と「青色」である場合に分けて、玉の色を推測します。',
    }


class Explanation4(ExplainMixin):
    question_num = 4
    option_labels = Q4.option_labels
    explanations = Q4.explanations


# ─────────────────────────────────────────────
#  問5
# ─────────────────────────────────────────────
class Q5(MultiSelectMixin):
    question_num = 5
    form_model = 'player'
    form_fields = [f'q5_opt{i}' for i in range(1, 5)]
    correct_set = {1, 3, 4}
    option_labels = [
        '追加報酬の換算には本番12ラウンドの中からランダムに選ばれた１ラウンドの結果が用いられる。',
        '受信者は２種類の獲得ポイントが両方とも追加報酬に換算される。',
        '１ポイント＝10円のレートで追加報酬に換算される。',
        '練習ラウンドの結果が追加報酬に換算されることはない。',
    ]
    explanations = {
        2: '２種類のうち１つだけがランダムに選ばれて換算対象になります。両方は換算されません。',
    }


class Explanation5(ExplainMixin):
    question_num = 5
    option_labels = Q5.option_labels
    explanations = Q5.explanations


# ─────────────────────────────────────────────
#  ページ遷移
# ─────────────────────────────────────────────
page_sequence = [
    Q1, Explanation1,
    Q2, Explanation2,
    Q3, Explanation3,
    Q4, Explanation4,
    Q5, Explanation5,
]

