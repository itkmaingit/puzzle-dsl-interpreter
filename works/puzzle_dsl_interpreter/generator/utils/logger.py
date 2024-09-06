from __future__ import annotations

import logging

from rich.logging import RichHandler

logging.basicConfig(
    level=logging.ERROR,
    format="%(message)s",
    handlers=[
        RichHandler(markup=True, rich_tracebacks=True),
    ],
)
logger = logging.getLogger(__name__)
