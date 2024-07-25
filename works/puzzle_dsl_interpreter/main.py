from __future__ import annotations

import sys

from antlr4 import CommonTokenStream, FileStream
from interpreter.CustomPuzzleDSLParserVisitor import (
    CustomPuzzleDSLParserVisitor as Visitor,
)
from parser.PuzzleDSLLexer import PuzzleDSLLexer
from parser.PuzzleDSLParser import PuzzleDSLParser


def main(argv):
    input_stream = FileStream(argv[1], encoding="utf-8")
    lexer = PuzzleDSLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PuzzleDSLParser(stream)
    tree = parser.file_()

    visitor = Visitor(parser)

    visitor.visit(tree)


if __name__ == "__main__":
    main(sys.argv)
