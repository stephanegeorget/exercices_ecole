"""Small helpers used by the different lessons.

This module centralises behaviour that is shared by several exercises,
such as displaying long pieces of text in a scrollable box.
"""

from __future__ import annotations

import pydoc


def scroll_text(text: str) -> None:
    """Display ``text`` inside a scrollable pager.

    The implementation relies solely on :func:`pydoc.pager` so that the
    behaviour is consistent across platforms.  If a pager cannot be
    launched, the text is simply printed to the terminal.

    Parameters
    ----------
    text:
        The content to display.
    """

    try:
        pydoc.pager(text)
    except Exception:
        print(text)


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

