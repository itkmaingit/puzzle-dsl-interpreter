from __future__ import annotations


def escape_special_chars(text):
    # 特殊文字とそのエスケープシーケンスの辞書
    escape_dict = {
        "\a": "\\a",  # ベル
        "\b": "\\b",  # バックスペース
        "\f": "\\f",  # フォームフィード
        "\n": "\\n",  # 改行
        "\r": "\\r",  # キャリッジリターン
        "\t": "\\t",  # タブ
        "\v": "\\v",  # 垂直タブ
        '"': '\\"',  # ダブルクオート
        "'": "\\'",  # シングルクオート
        "\\": "\\\\",  # バックスラッシュ
    }

    # 入力テキストの特殊文字をエスケープシーケンスに置き換え
    return "".join(escape_dict.get(c, c) for c in text)


# 使用例
input_text = """structs:
	A1 = combine ( C , { H, V } );
	A2 = combine ( C , { H, V } );

domain-hidden:
	P <-> { null } -> { null };
	C <-> { null } -> { null };
	Ep <-> { null } -> { null };
	Ec <-> { null } -> { null };
	A1 <-> { 1 ... n * m } -> { 1 ... n * m };
	A2 <-> { 1 ... n * m } -> { 1 ... n * m };

constraints:
	fill(A1, A2);
	All(a1) <- B(A1), !is_rectangle(a) && solution(a1) == |a1|;
	All(a2) <- B(A2), is_rectangle(a) && solution(a2) == |a2|;"""
escaped_text = escape_special_chars(input_text)
print(escaped_text)
