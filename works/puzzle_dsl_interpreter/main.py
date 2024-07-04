from __future__ import annotations

import sys

from antlr4 import CommonTokenStream, FileStream, ParseTreeWalker
from interpreter.CustomPuzzleDSLParserListener import (
    CustomPuzzleDSLParserListener as Listener,
)
from interpreter.CustomPuzzleDSLParserVisitor import (
    CustomPuzzleDSLParserVisitor as Visitor,
)
from parser.PuzzleDSLLexer import PuzzleDSLLexer
from parser.PuzzleDSLParser import PuzzleDSLParser


def main(argv):
    # input_stream = InputStream(argv[1])
    input_stream = FileStream(argv[1])
    lexer = PuzzleDSLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PuzzleDSLParser(stream)
    tree = parser.file_()

    walker = ParseTreeWalker()
    visitor = Visitor(parser)
    listener = Listener(parser)

    result = walker.walk(listener, tree)
    result = visitor.visit(tree)


if __name__ == "__main__":
    # input_str = "{H,D,D}"
    # main([None, input_str])
    main(sys.argv)
