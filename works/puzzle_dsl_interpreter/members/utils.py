from __future__ import annotations


def checkUnique(self, elements):
    seen = set()
    for e in elements:
        if e in seen:
            return False
        seen.add(e)
    return True


def validateSet(self, elements):
    if not (1 <= len(elements) <= 3):
        raise Exception("The set must contain between 1 and 3 elements")
    if not self.checkUnique(elements):
        raise Exception("Duplicate elements are not allowed")
