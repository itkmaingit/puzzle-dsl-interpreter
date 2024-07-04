from __future__ import annotations

import os
import re


def replace_leading_spaces_with_single_tab(directory):
    # 指定されたディレクトリ内のすべての.pzlファイルを探索
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pzl"):
                file_path = os.path.join(root, file)
                # ファイルを読み込み、各行の処理を行う
                with open(file_path, encoding="utf-8") as file:
                    lines = file.readlines()

                # 行頭のスペースを単一のタブに置換、空行は無視
                with open(file_path, "w", encoding="utf-8") as file:
                    for line in lines:
                        if line.strip():  # 空行でない場合のみ処理
                            # 行頭のスペースを単一のタブに置換
                            modified_line = re.sub(r"^\s+", "\t", line)
                            # 行内の2つ以上のスペースを1つのスペースに置換
                            modified_line = re.sub(r"[ ]{2,}", " ", modified_line)
                        else:
                            # 空行はそのまま保持
                            modified_line = line
                        file.write(modified_line)


# 使い方例
directory_path = "/home/node/works"
replace_leading_spaces_with_single_tab(directory_path)
