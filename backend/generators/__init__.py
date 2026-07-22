from .base import generate, REGISTRY
from . import matematik  # noqa: F401  (register decorator'lari calissin)
from . import turkce     # noqa: F401

__all__ = ["generate", "REGISTRY"]
