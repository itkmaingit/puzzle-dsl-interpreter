#!/bin/bash
# convert_tabs_to_spaces.sh

# ファイルをバックアップしつつタブをスペースに変換する
find puzzle_dsl_interpreter/parser -type f -name "*.py" -exec bash -c 'expand -t 4 "$0" > "$0.tmp" && mv "$0.tmp" "$0"' {} \;
