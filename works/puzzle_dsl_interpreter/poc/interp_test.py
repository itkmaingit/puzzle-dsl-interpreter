from __future__ import annotations

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from parser.PuzzleDSLLexer import PuzzleDSLLexer
from parser.PuzzleDSLParser import PuzzleDSLParser


class CustomErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # カスタムエラーメッセージやログ処理など
        print(f"Syntax error at line {line}:{column} - {msg}")


def main(argv):
    input_stream = InputStream(argv[1])
    lexer = PuzzleDSLLexer()
    lexer.removeErrorListeners()  # デフォルトのリスナーを削除
    lexer.addErrorListener(CustomErrorListener())  # カスタムリスナーを追加
    lexer.__init__(input_stream)
    # for token in lexer.getAllTokens():
    #     print(token.text)

    # トークンストリームのセットアップ
    token_stream = CommonTokenStream(lexer)
    parser = PuzzleDSLParser(token_stream)
    # print(parser._interp.atn.states[2].transitions)
    for state in parser._interp.atn.states:
        for transition in state.transitions:
            print("Transition to state:", transition.target.stateNumber)
            if transition.isEpsilon:
                print("Epsilon transition")
            else:
                print("Transition label:", transition.label)

    # initial_state = parser._interp.atn.states[parser._interp.state]
    # current_token = parser._input.LA(1)
    # next_transitions = initial_state.transitions
    # for transition in next_transitions:
    #     print("Next state:", transition.target.stateNumber)
    #     if transition.isEpsilon:
    #         print("Epsilon transition")
    #     else:
    #         print("Transition on symbol:", transition.serializationType)
    # print("Next token type:", parser.symbolicNames[next_token_type])
    # token_stream.fill()
    # for token in token_stream.tokens:
    #     print(f"Token type: {lexer.symbolicNames[token.type]}, Text: '{token.text}'")
    # tree = parser.file_()

    # トークンを1つずつ読み込み、その内容を表示


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
	fill()
"""
    main([None, input_str])
