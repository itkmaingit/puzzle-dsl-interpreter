from __future__ import annotations

import re

from antlr4 import (
    CommonTokenStream,
    InputStream,
    RecognitionException,
    Recognizer,
)
from antlr4.error.ErrorListener import ErrorListener
from interpreter.CustomPuzzleDSLParserVisitor import (
    CustomPuzzleDSLParserVisitor as Visitor,
)
from parser.PuzzleDSLLexer import PuzzleDSLLexer
from parser.PuzzleDSLParser import PuzzleDSLParser
from pydantic import BaseModel


class SyntaxErrorModel(BaseModel):
    line: int
    char_position_in_line: int
    msg: str


class CustomErrorListener2(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        currentContext = recognizer._ctx
        expected_tokens = recognizer.getExpectedTokens().toString(
            recognizer.literalNames,
            recognizer.symbolicNames,
        )
        # 現在のコンテキストから次の可能なコンテキストを取得
        nextContexts = self.getNextContexts(recognizer)
        print(
            f"Syntax error at line {line}:{column}. Next possible contexts: {nextContexts}",
        )
        print(f"Expected tokens: {expected_tokens}")

    def getNextContexts(self, recognizer):
        atn = recognizer.atn
        currentState = atn.states[recognizer.state]
        nextContexts = []
        for transition in currentState.transitions:
            if hasattr(transition.target, "ruleIndex"):
                ruleName = recognizer.ruleNames[transition.target.ruleIndex]
                if ruleName not in nextContexts:
                    nextContexts.append(ruleName)
        return nextContexts


class CustomErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors: list[SyntaxErrorModel] = []

    def syntaxError(  # noqa: PLR0913
        self,
        recognizer: Recognizer,
        offendingSymbol,  # noqa: N803
        line: int,
        charPositionInLine: int,  # noqa: N803
        msg: str,
        e: RecognitionException,
    ):
        print(msg)
        self.errors.append(
            SyntaxErrorModel(
                line=line,
                char_position_in_line=charPositionInLine,
                msg=msg,
            ),
        )

    def parse_first_error_message(self):
        if not self.errors:
            return None
        msg = self.errors[0].msg
        # 'mismatched input'の後の文字を抽出
        mismatched_input_match = re.search(r"mismatched input '([^']*)'", msg)

        if mismatched_input_match:
            mismatched_input = mismatched_input_match.group(1)
        else:
            mismatched_input = None

        # 'expecting'の後のセットまたは単一の値を抽出
        expecting_match = re.search(r"expecting ({.*?}|\S+)", msg)
        if expecting_match:
            expecting_content = expecting_match.group(1)
            if expecting_content.startswith("{"):
                # セットから文字を取り出す
                expecting_list = re.findall(r"'([^']*)'", expecting_content)
            else:
                # 単一の値をリストに追加
                expecting_list = [expecting_content.strip("'")]
        else:
            expecting_list = []

        return mismatched_input, expecting_list


class PuzzleDSLInterpreter:
    def __init__(self, input_stream: InputStream):
        self.__lexer = PuzzleDSLLexer(input_stream)
        self.__stream = CommonTokenStream(self.__lexer)
        self.__parser = PuzzleDSLParser(self.__stream)
        self.__parser.removeErrorListeners()  # 既存のエラーリスナーを削除
        error_listener = CustomErrorListener2()
        self.__parser.addErrorListener(error_listener)  # カスタムエラーリスナーを追加
        tree = self.__parser.file_()

        self.__visitor = Visitor(self.__parser)

        self.__result = self.__visitor.visit(tree)
