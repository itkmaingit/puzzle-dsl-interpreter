from __future__ import annotations

import numpy as np
from generator.definitions.rules import BaseRule, Range


def lottery(choices: list[type[BaseRule]]) -> type[BaseRule]:
    weights = [1 / choice.WEIGHT for choice in choices]
    weights_normalized = np.array(weights) / sum(weights)
    rng = np.random.default_rng()
    choice = rng.choice(choices, p=weights_normalized)
    choice.WEIGHT += 1
    return choice


def repeat(rule: type[BaseRule], repeat_range: Range) -> list[BaseRule]:
    result: list[BaseRule] = []
    for _ in repeat_range.generate():
        append_rule = rule()
        result.append(append_rule)
    return result
