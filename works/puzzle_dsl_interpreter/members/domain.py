from __future__ import annotations

import contextlib


def validate_domain_set(self, elements):
    if not self.check_unique(elements):
        raise Exception("Duplicate elements are not allowed")
    for element in elements:
        with contextlib.suppress(ValueError):
            value = int(element)
            if value > 100:
                raise Exception("The numbers in domain are too large!")
