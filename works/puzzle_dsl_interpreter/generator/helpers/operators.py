from __future__ import annotations

from math import inf

import numpy as np
from generator.definitions.rules import BaseRule, Range
from generator.stores.context import Context
from generator.stores.store import store
from generator.utils.logger import logger


def lottery(choices: list[type[BaseRule]], cls_name: str) -> type[BaseRule]:
    weight_diff = (
        1
        - min(
            choices,
            key=lambda rule: rule.WEIGHT,
        ).WEIGHT
    )
    weights = [choice.WEIGHT + weight_diff for choice in choices]
    weights_normalized = np.array(weights) / sum(weights)
    rng = np.random.default_rng()
    choice = rng.choice(choices, p=weights_normalized)
    choice.WEIGHT -= 1
    logger.info(
        f"CHOICE: [yellow]{cls_name} -> {choice.__name__}[/yellow] (in {store.context.name})",
    )
    return choice


def repeat(rule: type[BaseRule], repeat_range: Range) -> list[BaseRule]:
    result: list[BaseRule] = []
    for _ in repeat_range.generate():
        append_rule = rule()
        result.append(append_rule)
    return result


def in_which_context(
    contexts: list[Context],
    check_lst: list[list[Context]],
) -> list[Context]:
    result: list[Context] = []
    match_index = inf
    for check in check_lst:
        for index, ctx in contexts:
            for check_ctx in check:
                if check_ctx == ctx and index < match_index:
                    match_index = index
                    result = check

    return result
