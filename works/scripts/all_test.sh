#!/bin/bash

# 引数としてディレクトリのパスを受け取る
directory="/home/node/works/rules"

# 指定されたディレクトリ内の全ファイルに対してループ処理
find "$directory" -type f | while read filepath; do
    task analyze -- $filepath
    echo -e "\n"
done
