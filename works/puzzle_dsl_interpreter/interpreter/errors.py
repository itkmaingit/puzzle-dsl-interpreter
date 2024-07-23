from __future__ import annotations


class DuplicationStructDefinitionError(Exception):
    pass


class InvalidRelationshipSetError(Exception):
    pass


class NotDefinitionStructError(Exception):
    pass


class NotEnoughDomainHiddenDefinitionStructsError(Exception):
    pass


class ExistsUndefinedStructError(Exception):
    pass


class InsufficientStructError(Exception):
    pass


class SubsetViolationError(Exception):
    pass


class EvaluationError(Exception):
    pass


class UndefinedStructError(Exception):
    pass


class UndefinedValueError(Exception):
    pass
