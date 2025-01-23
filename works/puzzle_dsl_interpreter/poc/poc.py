from __future__ import annotations

from jinja2 import Template

# テンプレート文字列
SCOPE = "{ {{ render }} }"  # 文字列としてテンプレート構文を保持

# 第1段階: 最初のテンプレートをレンダリング
template = Template(SCOPE)
data = {"render": "{{ aaa }}"}
rendered_scope = template.render(data)  # "{{ aaa }}"r

# 第2段階: レンダリング結果を新しいテンプレートとして解釈
template2 = Template(rendered_scope)
data2 = {"aaa": "bbb"}
result = template2.render(data2)

print(result)

a = 10**10 - 196**2
b = 196**2 + 200
c = 10 ** (-54)

from decimal import getcontext

# 計算精度を設定
getcontext().prec = 100


def sqrt_decimal(n):
    """Decimal 型の平方根を計算する関数"""
    getcontext().prec += 2  # 途中計算の精度を上げる
    x, last = n / 2, None
    while x != last:
        last = x
        x = (x + n / x) / 2
    getcontext().prec -= 2  # 元の精度に戻す
    return +x  # 符号を正しく処理


import mpmath as mp

# 計算精度を設定（必要に応じて変更可能）
mp.dps = 50  # 小数点以下50桁の精度


# 関数を定義
def f(x):
    return x - mp.mpf("1.96") * mp.sqrt(x * (1 - x) / mp.mpf("100000")) - mp.mpf("1e-5")


# x の範囲を指定（0 と 1 の間）
x_lower = mp.mpf("0")
x_upper = mp.mpf("1")

# 根の探索
# f(x_lower) と f(x_upper) の符号が異なることを確認
if f(x_lower) * f(x_upper) > 0:
    print("指定した範囲に根が存在しません。")
else:
    x0 = mp.findroot(f, (x_lower, x_upper))
    # 結果の表示
    print("根 x0 =", x0)
    print("f(x0) =", f(x0))
