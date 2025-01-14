from __future__ import annotations

import importlib
import shutil
import subprocess
import sys
import traceback
import uuid
from argparse import ArgumentParser
from pathlib import Path

from antlr4 import FileStream
from errors.error import InvalidArgumentsError
from generator import PuzzleDSLRandomGenerator
from generator.checker.main import generate_code
from interpreter.PuzzleDSLInterpreter import PuzzleDSLInterpreter

success_times = 0
try_times = 0


def generate():
    while True:
        sys.setrecursionlimit(1000)
        while True:
            try:
                importlib.reload(PuzzleDSLRandomGenerator)
                generator = PuzzleDSLRandomGenerator.File()
                break
            except RecursionError as e:
                pass

        sentence = ""
        for token in generator.generate():
            sentence += token.text

        data = generator.to_json()
        try:
            checker_code = generate_code(data)
        except Exception as e:
            print(data)
            print(e)
            print(traceback.format_exc())
            sys.exit(1)
        run_tmp_py(checker_code, sentence)

    # if filepath:
    #     with Path(filepath + ".pzl").open(mode="w", encoding="utf-8") as f:
    #         f.write(sentence)
    #     with Path(filepath + ".json").open(mode="w", encoding="utf-8") as f:
    #         json.dump(data, f, indent=2)
    # else:
    #     print(sentence)
    #     print(json.dumps(data, indent=2))


def interpret(filepath: str):
    input_stream = FileStream(filepath, encoding="utf-8")
    PuzzleDSLInterpreter(input_stream)


def run_tmp_py(code_str: str, pzl_str: str):
    global success_times
    global try_times
    try_times += 1
    tmp_file_path = "puzzle_dsl_interpreter/generator/checker/tmp.py"

    # 1. tmp.py にコードを書き込む
    with Path.open(tmp_file_path, "w", encoding="utf-8") as f:
        f.write(code_str)

    # 2. poetry run python3 puzzle_dsl_interpreter/generator/checker/tmp.py を実行
    process = subprocess.Popen(
        ["poetry", "run", "python3", tmp_file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,  # Python 3.7+ なら、文字列として受け取るために text=True が使えます
    )

    stdout, stderr = process.communicate()
    return_code = process.returncode

    # 3. リターンコードが 1 の場合: tmp.py を削除
    if return_code == 1:
        if stdout == "":
            Path("failed").mkdir(exist_ok=True)
            shutil.copy(tmp_file_path, f"failed/{uuid.uuid4()!s}.py")
            return
        print(
            f"Failed... | {stdout} | 試行回数: {try_times}, 成功回数: {success_times}".replace(
                "\r",
                "",
            ).replace("\n", ""),
        )
        Path.unlink(tmp_file_path)

    # 4. リターンコードが 0 の場合: stdout から成功回数を読み取り、data/[file].txt を作成して書き込む
    if return_code == 0:
        success_times += 1
        success_count = stdout.strip()
        print(f"Success count: {success_count}")

        # 一意な文字列を生成 (例: UUID4)
        unique_id = str(uuid.uuid4())

        # data ディレクトリが存在しない場合は作成しておく
        Path("data").mkdir(exist_ok=True)

        output_file_path = f"data/{unique_id}.txt"
        output_pzl_path = f"data/{unique_id}.pzl"

        with Path.open(output_file_path, "w", encoding="utf-8") as f:
            f.write(success_count)
        with Path.open(output_pzl_path, "w", encoding="utf-8") as f:
            f.write(pzl_str)
        print("############# 成功!!!!!!!!!!!!!!!! ###################")
        print(f"成功回数 : {success_count}")
        print(pzl_str)
        print("######################################################")
        print()


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "-a",
        "--action",
        choices=["generator", "interpreter"],
        help="It can decide whether to use it as an interpreter or a generator.",
        required=True,
    )
    arg_parser.add_argument(
        "-f",
        "--file",
        help="Specify the path of the file you wish to analyse. Either absolute or relative paths are acceptable.",
    )
    arg_parser.add_argument(
        "-o",
        "--output",
        help="Specify the file path to which you want to output the generated puzzle rules. The default output is to standard output.",
    )
    if arg_parser.parse_args().action == "interpreter":
        filepath = arg_parser.parse_args().file
        if filepath == "":
            raise InvalidArgumentsError(
                "You have to execute 'task analyze -- /path/to/analyze.pzl'",
            )
        interpret(filepath)
    else:
        filepath = arg_parser.parse_args().output
        generate()
