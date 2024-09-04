from __future__ import annotations

from generator.definitions.rules import Range

# 使用例
range_instance = Range(min=0, max=9)

for _ in range(10000):
    print(range_instance.generate())
