from __future__ import annotations

import re

from generator.token import TOKEN_PATTERNS, Token, TokenType


def test_token_text_matches_pattern():
    token_type = TokenType.CONSTANT_ID
    token = Token(type=token_type)
    pattern = TOKEN_PATTERNS[token_type]
    assert re.fullmatch(
        pattern,
        token.text,
    ), f"Generated text '{token.text}' does not match the pattern '{pattern}' for token type '{token_type.name}'"
