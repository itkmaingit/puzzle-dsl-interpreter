from __future__ import annotations

import random
from abc import ABC, abstractmethod
from enum import IntEnum, auto

import numpy as np
from generator.definitions.errors import (
    NotGivenChoicesError,
    NotGivenOrderError,
    NotGivenRuleError,
    NotGivenTokenError,
)
from generator.definitions.token import Token
from pydantic import BaseModel


class BaseRule(ABC):
    WEIGHT = 1

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def generate(self) -> list[Token]:
        pass


class Range(BaseModel):
    min: int = 1
    max: int = 1

    def generate(self) -> range:
        # 範囲の差を取得
        range_diff = self.max - self.min + 1

        # 重みを計算(minに近いほど重い)
        weights = [1 / (x + 1) ** 2 for x in range(range_diff)]
        total_weight = sum(weights)

        # 正規化された重みを使用してランダムな値を選択
        chosen_weight = random.uniform(0, total_weight)
        cumulative_weight = 0
        for i, weight in enumerate(weights):
            cumulative_weight += weight
            if cumulative_weight >= chosen_weight:
                return range(self.min + i)

        return range(self.min)


# 生Token
class RawToken(BaseRule):
    def __init__(self, token: Token):
        if token is None:
            raise NotGivenTokenError("Tokenが与えられていません。")
        self.__token = token

    def generate(self) -> list[Token]:
        return [self.__token]


# or実行
class AlternativeRule(BaseRule):
    def __init__(self, choices: list[type[BaseRule]]):
        if choices is None:
            raise NotGivenChoicesError(
                "選択肢となるset[BaseRule]が初期化されていません。",
            )
        weights = [1 / choice.WEIGHT for choice in choices]
        weights_normalized = np.array(weights) / sum(weights)
        rng = np.random.default_rng()
        choice = rng.choice(choices, p=weights_normalized)
        choice.WEIGHT += 1
        self.__choice = choice

    def generate(self) -> list[Token]:
        return self.__choice().generate()


# 複数回実行
class MultipleRule(BaseRule):
    def __init__(
        self,
        rule: type[BaseRule],
        range: Range,
    ):
        if rule is None:
            raise NotGivenRuleError("複数回実行するBaseRuleが与えられていません。")
        if range is None:
            range = Range(min=1, max=1)
        self.__rule = rule
        self.__range = range

    def generate(self) -> list[Token]:
        result: list[Token] = []
        for _ in self.__range.generate():
            result.extend(self.__rule().generate())
        return result


# 直列実行
class OrderRule(BaseRule):
    def __init__(
        self,
        order: list[type[BaseRule]],
    ):
        if order is None:
            raise NotGivenOrderError("直列実行するset[BaseRule]が与えられていません。")
        self.__order: list[type[BaseRule]] = order

    def generate(
        self,
    ) -> list[Token]:
        result: list[Token] = []
        for rule in self.__order:
            result.extend(
                rule().generate(),
            )

        return result


class RuleType(IntEnum):
    file = auto()
    structsDeclaration = auto()
    domainHiddenDeclaration = auto()
    constraintsDeclaration = auto()
    structID = auto()
    newStructID = auto()
    structDefinitionBody = auto()
    structDefinition = auto()
    structDefinitions = auto()
    relationshipID = auto()
    relationshipSetBody = auto()
    relationshipSet = auto()
    pID = auto()
    cID = auto()
    epID = auto()
    ecID = auto()
    intDomainValue = auto()
    rangeValue = auto()
    domainValue = auto()
    domainSetBody = auto()
    domainSet = auto()
    hiddenValue = auto()
    hiddenSetBody = auto()
    hiddenSet = auto()
    domainDefinitionBody = auto()
    pDefinition = auto()
    cDefinition = auto()
    epDefinition = auto()
    ecDefinition = auto()
    customStructDefinition = auto()
    domainDefinitions = auto()
    int = auto()
    primitiveValue = auto()
    set = auto()
    solutionFunction = auto()
    bFunction = auto()
    crossFunction = auto()
    cycleFunction = auto()
    allDifferentFunction = auto()
    isRectangleFunction = auto()
    isSquareFunction = auto()
    connectFunction = auto()
    noOverlapFunction = auto()
    fillFunction = auto()
    quantifier = auto()
    index = auto()
    quantifierIndex = auto()
    indexFunction = auto()
    structElement = auto()
    generationSet = auto()
    boolean = auto()
    singleBoolean = auto()
    notBoolean = auto()
    parenthesizedBoolean = auto()
    quantifierBoolean = auto()
    compoundBoolean = auto()
    constraint = auto()
    constraintDefinition = auto()
    constraintsDefinitions = auto()
