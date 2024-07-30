from __future__ import annotations

import sys

from antlr4 import FileStream
from interpreter.PuzzleDSLInterpreter import PuzzleDSLInterpreter


def main(argv):
    input_stream = FileStream(argv[1], encoding="utf-8")
    interpreter = PuzzleDSLInterpreter(input_stream)


if __name__ == "__main__":
    main(sys.argv)
