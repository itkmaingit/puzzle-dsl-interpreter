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


class CustomErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors: list[SyntaxErrorModel] = []

    def syntaxError(
        self,
        recognizer: Recognizer,
        offendingSymbol,
        line: int,
        charPositionInLine: int,
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


def main(argv):
    input_stream = InputStream(argv[1])
    lexer = PuzzleDSLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PuzzleDSLParser(stream)
    parser.removeErrorListeners()  # 既存のエラーリスナーを削除
    error_listener = CustomErrorListener()
    parser.addErrorListener(error_listener)  # カスタムエラーリスナーを追加
    tree = parser.file_()
    if error_listener.errors:
        print(error_listener.parse_first_error_message())
    # walker = ParseTreeWalker()
    visitor = Visitor(parser)
    # listener = Listener(parser)

    # result = walker.walk(listener, tree)
    result = visitor.visit(tree)


if __name__ == "__main__":
    input_str = """
structs:
	A = combine ( C , { H, V } );
	Ah = combine ( C , { H } );
	Av = combine ( C , { V } );

domain-hidden:
	P <-> { null } -> { null };
	C <-> { 1 ... 9 } -> { 1 ... 9, undecided };
	Ep <-> { null } -> { null };
	Ec <-> { null } -> { null };
	A <-> { null } -> { null };
	Ah <-> { null } -> { null };
	Av <-> { null } -> { null };

constraints:
	fill
"""

    main([None, input_str])
    # main(sys.argv)
