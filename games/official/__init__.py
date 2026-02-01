"""
Author: Claude Sonnet 4
Date: 2026-01-31
PURPOSE: Official ARC-AGI-3 preview games (ls20, ft09, vc33) downloaded via arc-agi API.
         These are MIT licensed by ARC Prize Foundation. Use for study and modification.
SRP/DRY check: Pass - Package init only
"""

from .ls20 import Ls20
from .ft09 import Ft09
from .vc33 import Vc33

__all__ = ["Ls20", "Ft09", "Vc33"]
