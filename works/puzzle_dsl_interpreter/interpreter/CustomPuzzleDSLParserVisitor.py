from __future__ import annotations

from parser.PuzzleDSLParser import PuzzleDSLParser
from parser.PuzzleDSLParserVisitor import PuzzleDSLParserVisitor


class CustomPuzzleDSLParserVisitor(PuzzleDSLParserVisitor):
    def __init__(self, parser: PuzzleDSLParser):
        self.__parser = parser

    def visitStructDefinitions(self, ctx: PuzzleDSLParser.StructDefinitionsContext):
        print("struct: ", ctx.getChildCount())
        print()
        for child in ctx.getChildren():
            print(child.getText())
        return super().visitStructDefinitions(ctx)

    def visitDomainDefinitions(self, ctx: PuzzleDSLParser.DomainDefinitionsContext):
        print()
        print("domain: ", ctx.getChildCount())
        print()
        for child in ctx.getChildren():
            print(child.getText())
        return super().visitStructDefinitions(ctx)

    def visitConstraintsDefinitions(
        self,
        ctx: PuzzleDSLParser.ConstraintsDefinitionsContext,
    ):
        print()
        print("constraints: ", ctx.getChildCount())
        print()
        for child in ctx.getChildren():
            print(child.getText())
        return super().visitConstraintsDefinitions(ctx)


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
