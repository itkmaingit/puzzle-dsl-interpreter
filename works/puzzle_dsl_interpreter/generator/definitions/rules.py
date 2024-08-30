from __future__ import annotations

from abc import ABC, abstractmethod
from enum import IntEnum, auto
from random import choices, randint

from generator.definitions.errors import (
    NotGivenChoicesError,
    NotGivenOrderError,
    NotGivenRuleError,
    NotGivenTokenError,
)
from generator.definitions.token import Token
from pydantic import BaseModel


class BaseRule(ABC):
    def __init__(self, weight: int = 1):
        self.weight = weight

    @classmethod
    @abstractmethod
    def generate(cls) -> list[Token]:
        pass


# 生Token
class RawToken(BaseRule):
    def __init__(self, token: Token | None = None, weight: int = 1):
        if token is None:
            raise NotGivenTokenError("Tokenが与えられていません。")
        self.__token = token
        super().__init__(weight=weight)

    def generate(self) -> list[Token]:
        return [self.__token]


class Range(BaseModel):
    min: int = 1
    max: int = 1

    def decline(self):
        self.max = max(min - 1, max - 1)

    def callable(self) -> bool:
        return min <= max

    def clone(self) -> Range:
        return Range(min=self.min, max=self.max)

    def dec_clone(self) -> Range:
        return Range(min=self.min, max=self.max - 1)


# or実行
class AlternativeRule(BaseRule):
    def __init__(self, choices: set[BaseRule] | None = None, weight: int = 1):
        if choices is None:
            raise NotGivenChoicesError(
                "選択肢となるset[BaseRule]が初期化されていません。",
            )
        self.__choices = choices
        super().__init__(weight=weight)

    def generate(self) -> list[Token]:
        # 各候補の重みに基づいて一つを確率的に選択
        # https://magazine.techacademy.jp/magazine/33531
        chosen_rule = choices(
            list(self.__choices),
            weights=[1 / choice.weight for choice in self.__choices],
            k=1,
        )[0]
        chosen_rule.weight += 1
        return chosen_rule.generate()


# 複数回実行
class MultipleRule(BaseRule):
    def __init__(
        self,
        rule: BaseRule | None = None,
        range: Range | None = None,
        weight: int = 1,
    ):
        if rule is None:
            raise NotGivenRuleError("複数回実行するBaseRuleが与えられていません。")
        if range is None:
            range = Range(min=1, max=1)
        self.__rule = rule
        self.__range = range
        super().__init__(weight=weight)

    def generate(self) -> list[Token]:
        result: list[Token] = []
        for _ in randint(self.__range.min, self.__range.max):
            result.extend(self.__rule.generate())
        return result


# 直列実行
class OrderRule(BaseRule):
    def __init__(
        self,
        order: list[BaseRule] | None = None,
        weight: int = 1,
    ):
        if order is None:
            raise NotGivenOrderError("直列実行するset[BaseRule]が与えられていません。")
        self.__order = order
        super().__init__(weight=weight)

    def generate(
        self,
    ) -> list[Token]:
        result: list[Token] = []
        for rule in self.__order:
            result.extend(
                rule.generate(),
            )  # Execute the function and collect its results

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
