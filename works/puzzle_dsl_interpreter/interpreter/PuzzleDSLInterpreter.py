from __future__ import annotations

from antlr4 import (
    CommonTokenStream,
    InputStream,
)
from interpreter.CustomPuzzleDSLParserVisitor import (
    CustomPuzzleDSLParserVisitor as Visitor,
)
from parser.PuzzleDSLLexer import PuzzleDSLLexer
from parser.PuzzleDSLParser import PuzzleDSLParser


class PuzzleDSLInterpreter:
    def __init__(self, input_stream: InputStream):
        self.__lexer = PuzzleDSLLexer(input_stream)
        self.__stream = CommonTokenStream(self.__lexer)
        self.__parser = PuzzleDSLParser(self.__stream)
        tree = self.__parser.file_()
        self.__visitor = Visitor(self.__parser)
        self.__visitor.visit(tree)
