from __future__ import annotations

from generator.PuzzleDSLRandomGenerator import PuzzleDSLGenerator

generator = PuzzleDSLGenerator()
generated_code = generator.generate()
print(generated_code)
