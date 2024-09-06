from __future__ import annotations

import sys
from argparse import ArgumentParser
from pathlib import Path

from antlr4 import FileStream
from errors.error import InvalidArgumentsError
from generator.PuzzleDSLRandomGenerator import File
from interpreter.PuzzleDSLInterpreter import PuzzleDSLInterpreter


def generate(filepath: str):
    sys.setrecursionlimit(2000)
    generator = File()
    sentence = ""
    for token in generator.generate():
        sentence += token.text
    if filepath:
        with Path(filepath).open(mode="w", encoding="utf-8") as f:
            f.write(sentence)
    else:
        print(sentence)


def interpret(filepath: str):
    input_stream = FileStream(filepath, encoding="utf-8")
    PuzzleDSLInterpreter(input_stream)


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
        generate(filepath)
