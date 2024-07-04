from __future__ import annotations

from parser.PuzzleDSLParser import PuzzleDSLParser
from parser.PuzzleDSLParserListener import PuzzleDSLParserListener


class CustomPuzzleDSLParserListener(PuzzleDSLParserListener):
    def __init__(self, parser: PuzzleDSLParser):
        self.__parser = parser

    # Enter a parse tree produced by PuzzleDSLParser#structsDeclaration.
    def enterStructsDeclaration(self, ctx: PuzzleDSLParser.StructsDeclarationContext):
        pass

    # Exit a parse tree produced by PuzzleDSLParser#structsDeclaration.
    def exitStructsDeclaration(self, ctx: PuzzleDSLParser.StructsDeclarationContext):
        pass


# ctx method

# getChild(int i)

# 指定したインデックス i の子ノードを取得します。
# getChildCount()

# 子ノードの数を返します。
# getText()

# このノードおよびすべての子ノードのテキストを連結して返します。
# children

# すべての子ノードのリストを返します。
# start

# このコンテキストの開始トークンを返します。
# stop

# このコンテキストの終了トークンを返します。
# getRuleContext(Class<? extends T> ctxType, int i)

# 指定したインデックス i の子ノードを指定したコンテキスト型で取得します。
# accept(ParseTreeVisitor<? extends T> visitor)

# ビジターパターンを使用してこのノードを訪問します。
# toStringTree(Parser parser)
