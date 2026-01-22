from __future__ import annotations

from decimal import Decimal
from typing import Any, Optional


def comma(value: Any, *, decimals: int = 0, none_as: str = "-") -> str:
    """Return a human-friendly number with thousands separators.

    - None -> none_as
    - int/Decimal -> commas
    - float -> commas, optional decimals (default 0)

    This is intended for Jinja templates via `|comma`.
    """
    if value is None:
        return none_as

    # Booleans are ints in Python; treat them as non-numeric display here.
    if isinstance(value, bool):
        return str(value)

    try:
        if isinstance(value, int):
            return f"{value:,}"

        if isinstance(value, Decimal):
            # If decimals is 0, show as integer when possible.
            if decimals == 0:
                try:
                    as_int = int(value)
                    if value == as_int:
                        return f"{as_int:,}"
                except Exception:
                    pass
            return f"{value:,.{decimals}f}" if decimals > 0 else f"{value:,}"

        if isinstance(value, float):
            if decimals == 0:
                if value.is_integer():
                    return f"{int(value):,}"
                return f"{value:,.0f}"
            return f"{value:,.{decimals}f}"

        # Strings that look like numbers
        if isinstance(value, str):
            stripped = value.strip()
            if stripped == "":
                return none_as
            # Try int first
            try:
                return f"{int(stripped):,}"
            except Exception:
                pass
            # Try float
            try:
                f = float(stripped)
                if decimals == 0 and f.is_integer():
                    return f"{int(f):,}"
                return f"{f:,.{decimals}f}" if decimals > 0 else f"{f:,.0f}"
            except Exception:
                return value

        # Fallback: try numeric conversion
        return f"{int(value):,}"
    except Exception:
        return str(value)
