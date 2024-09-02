from __future__ import annotations

import sys

from generator.definitions.token import Token
from generator.PuzzleDSLRandomGenerator import File

# generator = PuzzleDSLGenerator()
# generated_code = generator.generate()
# print(generated_code)

sys.setrecursionlimit(67108864)  # 64MB


def to_text(tokens: list[Token]):
    sentence = ""
    for token in tokens:
        sentence += token.text
    print(sentence)


test = File()
to_text(test.generate())
