from __future__ import annotations


class NotGivenChoicesError(Exception):
    pass


class NotGivenRuleError(Exception):
    pass


class NotGivenOrderError(Exception):
    pass


class NotGivenTokenError(Exception):
    pass


class NotDeletableError(Exception):
    pass


class DuplicationVariableError(Exception):
    pass


class ForbiddenOperationError(Exception):
    pass


class NotMatchContextError(Exception):
    pass


class UnableToContinueError(Exception):
    pass
