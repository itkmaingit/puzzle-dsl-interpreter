from __future__ import annotations

from antlr4 import ParserRuleContext


def decorate_error_message(ctx: ParserRuleContext, message):
    return f"Column: {ctx.start.line}, {message}"


class PuzzleDSLBaseError(Exception):
    def __init__(self, ctx: ParserRuleContext, message: str):
        self.message = f"Column: {ctx.start.line}, {message}"
        super().__init__(self.message)


class DuplicationStructDefinitionError(PuzzleDSLBaseError):
    pass


class InvalidRelationshipSetError(PuzzleDSLBaseError):
    pass


class NotDefinitionStructError(PuzzleDSLBaseError):
    pass


class NotEnoughDomainHiddenDefinitionStructsError(PuzzleDSLBaseError):
    pass


class ExistsUndefinedStructError(PuzzleDSLBaseError):
    pass


class InsufficientStructError(PuzzleDSLBaseError):
    pass


class SubsetViolationError(PuzzleDSLBaseError):
    pass


class EvaluationError(PuzzleDSLBaseError):
    pass


class UndefinedStructError(PuzzleDSLBaseError):
    pass


class UndefinedValueError(PuzzleDSLBaseError):
    pass
