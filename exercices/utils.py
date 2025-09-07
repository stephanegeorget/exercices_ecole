"""Small helpers used by the different lessons.

This module centralises behaviour that is shared by several exercises,
such as displaying long pieces of text in a scrollable box.
"""

from __future__ import annotations

import subprocess
import pydoc


def scroll_text(text: str) -> None:
    """Display ``text`` inside a scrollable pager.

    The function prefers the ``less`` pager so that ANSI colours and
    Unicode characters are rendered correctly.  If ``less`` is not
    available, it falls back to :func:`pydoc.pager`.

    Parameters
    ----------
    text:
        The content to display.
    """

    try:
        # ``-R`` preserves raw control characters (colours).
        subprocess.run(["less", "-R"], input=text, text=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        pydoc.pager(text)


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

