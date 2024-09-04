from __future__ import annotations

from generator.definitions.token import Token
from generator.PuzzleDSLRandomGenerator import File


def to_text(tokens: list[Token]):
    sentence = ""
    for token in tokens:
        sentence += token.text
    print(sentence)


test = File()
to_text(test.generate())
