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


def scroll_text(text: str) -> None:
    """Display ``text`` inside a scrollable pager.

    On Windows, :mod:`pydoc` may fail to display Unicode characters such
    as emojis because the pager it invokes cannot handle UTF-8.  To make
    sure the colourful lessons render correctly, a small custom pager is
    used when running on Windows.  It supports scrolling with the arrow
    keys and exiting with ``q``.  On other platforms :func:`pydoc.pager`
    is still used to benefit from the user's configured pager.

    Parameters
    ----------
    text:
        The content to display.
    """

    if os.name == "nt" and msvcrt is not None:  # pragma: no cover - can't test on Linux
        _scroll_text_windows(text)
    else:  # fall back to pydoc's pager elsewhere
        try:
            pydoc.pager(text)
        except Exception:
            print(text)


def _scroll_text_windows(text: str) -> None:  # pragma: no cover - Windows only
    """Simple pager for Windows that keeps emojis intact."""

    lines: List[str] = text.splitlines()
    height = shutil.get_terminal_size().lines - 1
    top = 0

    def clear() -> None:
        os.system("cls")

    while True:
        clear()
        for line in lines[top : top + height]:
            print(line)

        key = msvcrt.getwch()
        # Arrow keys are reported as a two-character sequence starting
        # with ``\xe0``.  The second character identifies the direction.
        if key in ("\x00", "\xe0"):
            key = msvcrt.getwch()
            if key == "H":  # Up arrow
                top = max(0, top - 1)
            elif key == "P":  # Down arrow
                top = min(len(lines) - height, top + 1)
        elif key.lower() == "q":
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

