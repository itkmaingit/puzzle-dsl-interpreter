from __future__ import annotations


def check_unique(self, elements):
    seen = set()
    for e in elements:
        if e in seen:
            return False
        seen.add(e)
    return True


def validate_relationship_set(self, elements):
    if not (1 <= len(elements) <= 3):
        raise Exception("The set must contain between 1 and 3 elements")
    if not self.check_unique(elements):
        raise Exception("Duplicate elements are not allowed")
