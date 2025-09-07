"""Small helpers used by the different lessons.

This module centralises behaviour that is shared by several exercises,
such as displaying long pieces of text in a scrollable box.
"""

from __future__ import annotations

import os
import shutil
from typing import List

import pydoc
try:  # ``msvcrt`` is only available on Windows
    import msvcrt
except Exception:  # pragma: no cover - import will fail on non-Windows
    msvcrt = None  # type: ignore[assignment]


def scroll_text(text: str, exit_letter: str = "q", hint: str | None = None) -> None:
    """Display ``text`` inside a scrollable pager.

    The pager always shows a hint about which key to press to exit.  On
    Windows a small custom implementation is used so emojis display
    correctly.  Elsewhere :func:`pydoc.pager` is still leveraged but the
    hint is added at the beginning and end of the text so the user knows
    to press ``exit_letter`` to continue.

    Parameters
    ----------
    text:
        The content to display.
    exit_letter:
        Key that closes the pager.
    hint:
        Message shown to the user.  Defaults to ``"Tape '{exit_letter}' pour continuer"``.
    """

    if hint is None:
        hint = f"Tape '{exit_letter}' pour continuer"

    if os.name == "nt" and msvcrt is not None:  # pragma: no cover - can't test on Linux
        # Add the hint to the top of the text and keep another copy on the
        # bottom line that remains visible while scrolling.
        _scroll_text_windows(f"{hint}\n\n{text}", exit_letter, hint)
    else:  # fall back to pydoc's pager elsewhere
        decorated = f"{hint}\n\n{text}\n\n{hint}"
        try:
            pydoc.pager(decorated)
        except Exception:
            print(decorated)


def _scroll_text_windows(text: str, exit_letter: str, hint: str) -> None:  # pragma: no cover - Windows only
    """Simple pager for Windows that keeps emojis intact."""

    lines: List[str] = text.splitlines()
    height = shutil.get_terminal_size().lines - 1
    top = 0

    def clear() -> None:
        os.system("cls")

    while True:
        clear()
        window = lines[top : top + height]
        for line in window:
            print(line)
        # pad with blank lines so the hint stays at the bottom
        for _ in range(height - len(window)):
            print()
        print(hint)

        key = msvcrt.getwch()
        # Arrow keys are reported as a two-character sequence starting
        # with ``\xe0``.  The second character identifies the direction.
        if key in ("\x00", "\xe0"):
            key = msvcrt.getwch()
            if key == "H":  # Up arrow
                top = max(0, top - 1)
            elif key == "P":  # Down arrow
                top = min(len(lines) - height, top + 1)
        elif key.lower() == exit_letter.lower():
            break


def wait_for_letter(letter: str, prompt: str) -> None:
    """Block until ``letter`` is typed by the user.

    Parameters
    ----------
    letter:
        The expected letter (case-insensitive).
    prompt:
        Message displayed to the user.
    """

    while True:
        if input(prompt).strip().lower() == letter.lower():
            break

