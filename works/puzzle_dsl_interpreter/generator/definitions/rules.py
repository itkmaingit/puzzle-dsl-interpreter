from __future__ import annotations

import random
from abc import ABC, abstractmethod
from enum import IntEnum, auto
from typing import NoReturn

from generator.definitions.errors import (
    NotGivenOrderError,
    NotGivenTokenError,
)
from generator.definitions.token import Token
from pydantic import BaseModel


class BaseRule(ABC):
    WEIGHT = 1

    @abstractmethod
    def generate(self) -> list[Token]:
        pass


class Range(BaseModel):
    min: int = 1
    max: int = 1

    def generate(self) -> range:
        if self.max < self.min:
            return range(0)
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
    def __init__(self, token: Token) -> NoReturn:
        if token is None:
            raise NotGivenTokenError("Tokenが与えられていません。")
        # if store.exists_ok():
        #     choice = random.choice(store.ok)
        #     token.re_construct(choice)
        # elif store.exists_ng():
        #     while token.text in store.ng:
        #         token.re_lottery()
        self.__token = token

    def generate(self) -> list[Token]:
        return [self.__token]


class AlternativeRule(BaseRule):
    def __init__(self, choice: BaseRule):
        self.__choice = choice

    def generate(self) -> list[Token]:
        return self.__choice.generate()


# 複数回実行
class MultipleRule(BaseRule):
    def __init__(self, order: list[BaseRule]):
        self.__order = order

    def generate(self) -> list[Token]:
        result: list[Token] = []
        for el in self.__order:
            result += el.generate()
        return result


# 直列実行
class OrderRule(BaseRule):
    def __init__(
        self,
        order: list[BaseRule],
    ):
        if order is None:
            raise NotGivenOrderError("直列実行するset[BaseRule]が与えられていません。")
        self.__order: list[BaseRule] = order

    def generate(
        self,
    ) -> list[Token]:
        result: list[Token] = []
        for rule in self.__order:
            result += rule.generate()
        return result


class SingleRule(BaseRule):
    def __init__(
        self,
        rule: BaseRule,
    ):
        self.__rule = rule

    def generate(self) -> list[Token]:
        return self.__rule.generate()


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
