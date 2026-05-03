"""Low-level terminal display helpers for arithmetic layout exercises.

Provides the 3×3 digit-cell grid used by multiplication, euclidean division,
and similar column-arithmetic exercises.
"""

from __future__ import annotations

import os

# ANSI escape codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def render_digit_cell(
    char: str,
    highlighted: bool = False,
    color: str = "",
) -> tuple[str, str, str]:
    """Return (top_row, mid_row, bot_row) for a single 3×3 character cell.

    Each row is 3 visible characters wide (plus ANSI codes when coloured).
    """
    c = (str(char).strip() or " ")[0]
    if highlighted:
        col = color or YELLOW
        return (
            f"{col}┌─┐{RESET}",
            f"{col}│{BOLD}{c}{RESET}{col}│{RESET}",
            f"{col}└─┘{RESET}",
        )
    return ("   ", f" {c} ", "   ")


def render_number_row(
    total_cols: int,
    cells: list[tuple[str, bool, str]],
    *,
    prefix: str = "   ",
    suffix_mid: str = "",
) -> str:
    """Render a right-aligned sequence of digit cells as a 3-line string.

    Parameters
    ----------
    total_cols:
        Total number of digit columns in the display.
    cells:
        List of ``(char, highlighted, color)`` tuples, right-aligned within
        *total_cols*.
    prefix:
        Exactly 3-character string shown only on the middle (digit) line.
        Top and bottom lines are padded with spaces of the same width.
    suffix_mid:
        Extra text appended only to the middle (digit) line.
    """
    pad = total_cols - len(cells)
    full: list[tuple[str, bool, str]] = [(" ", False, "")] * pad + list(cells)

    tops, mids, bots = [], [], []
    for char, hl, col in full:
        t, m, b = render_digit_cell(char, hl, col)
        tops.append(t)
        mids.append(m)
        bots.append(b)

    blank_prefix = " " * len(prefix)
    return "\n".join([
        blank_prefix + "".join(tops),
        prefix + "".join(mids) + suffix_mid,
        blank_prefix + "".join(bots),
    ])


def render_separator(total_cols: int, *, prefix: str = "   ") -> str:
    """Return a separator line spanning all digit columns."""
    return prefix + "─" * (total_cols * 3)
