#!/bin/bash

# 引数としてディレクトリのパスを受け取る
directory="/home/node/works/rules"

# 指定されたディレクトリ内の全ファイルに対してループ処理
find "$directory" -type f | while read filepath; do
    echo "Running: make run INPUT=$filepath"
    make run INPUT="$filepath"
    echo -e "\n"
done
