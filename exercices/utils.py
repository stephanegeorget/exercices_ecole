"""Small helpers used by the different lessons.

This module centralises behaviour that is shared by several exercises,
such as displaying long pieces of text in a scrollable box.
"""

from __future__ import annotations

import pydoc


def scroll_text(text: str) -> None:
    """Display ``text`` inside a scrollable pager.

    The user can navigate with the arrow keys when the content is longer
    than the terminal size.  Execution returns once the user exits the
    pager (usually by pressing ``q``).
    """

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

