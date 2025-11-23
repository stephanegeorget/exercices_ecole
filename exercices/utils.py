"""Small helpers used by the different lessons.

This module centralises behaviour that is shared by several exercises,
such as displaying long pieces of text in a scrollable box.
"""

from __future__ import annotations

import os
import shutil
import sys
from typing import List, Sequence, Set

import pydoc
try:  # ``msvcrt`` is only available on Windows
    import msvcrt
except Exception:  # pragma: no cover - import will fail on non-Windows
    msvcrt = None  # type: ignore[assignment]
try:  # Arrow-key handling on POSIX
    import termios
    import tty
except Exception:  # pragma: no cover - not available everywhere
    termios = None  # type: ignore[assignment]
    tty = None  # type: ignore[assignment]


CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


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


def show_lesson(text: str) -> None:
    """Display ``text`` in a pager with a standard quiz hint."""

    scroll_text(text, hint="Tape 'q' pour passer au quiz")


def format_fraction(
    numerator: int | str,
    denominator: int | str,
    *,
    prefix: str = "",
    suffix: str = "",
    bar: str = "─",
) -> str:
    """Return a pretty, multi-line rendering of a fraction.

    Parameters
    ----------
    numerator, denominator:
        Values to show above and below the fraction bar.
    prefix:
        Text displayed to the *left* of the bar (for example ``"2 + "`` for a
        nombre mixte).  The prefix only appears on the middle line; the other
        lines are padded with spaces so the fraction stays aligned.
    suffix:
        Text appended to the middle line, such as an explanatory equality.
    bar:
        Character used to draw the horizontal bar.  Defaults to ``"─"`` which
        renders nicely in most terminals.
    """

    numerator_str = str(numerator)
    denominator_str = str(denominator)
    width = max(len(numerator_str), len(denominator_str), 1)

    top = numerator_str.center(width)
    middle = bar * width
    bottom = denominator_str.center(width)

    left_padding = " " * len(prefix)
    right_padding = " " * len(suffix)

    return "\n".join(
        (
            f"{left_padding}{top}{right_padding}",
            f"{prefix}{middle}{suffix}",
            f"{left_padding}{bottom}{right_padding}",
        )
    )


def ask_choice_with_navigation(
    choices: Sequence[str], *, horizontal_threshold: int = 120
) -> tuple[int, List[str]]:
    """Display choices in roomy boxes and let the learner pick with arrows or letters.

    The layout automatically switches between a horizontal row (controlled with
    the left/right arrows) and a vertical stack (controlled with the up/down
    arrows) depending on the available terminal width.  Regardless of layout,
    the learner can always type the associated letter (a, b, c, …) and press
    Enter.  Returns the selected index and the letter list.
    """

    option_letters = [chr(ord("a") + idx) for idx in range(len(choices))]

    if not sys.stdin.isatty():
        # Non-interactive environments: fall back to a simple prompt but keep
        # the spaced-out display for readability.
        _render_choices(option_letters, choices, selected=-1, layout="vertical")
        answer = input("Votre réponse (lettre) : ").strip().lower()
        try:
            return option_letters.index(answer), option_letters
        except ValueError:
            return -1, option_letters

    layout = _pick_layout(choices, option_letters, horizontal_threshold)
    selected = 0
    previous_lines = 0

    while True:
        lines = _render_choices(option_letters, choices, selected=selected, layout=layout)
        _rewrite_block(lines, previous_lines)
        previous_lines = len(lines)

        key = _read_key()
        if key is None:
            answer = input("Votre réponse (lettre) : ").strip().lower()
            try:
                return option_letters.index(answer), option_letters
            except ValueError:
                return -1, option_letters

        if key in option_letters:
            return option_letters.index(key), option_letters
        if key == "ENTER":
            return selected, option_letters

        if layout == "horizontal":
            if key == "RIGHT":
                selected = (selected + 1) % len(choices)
            elif key == "LEFT":
                selected = (selected - 1) % len(choices)
        else:
            if key == "DOWN":
                selected = (selected + 1) % len(choices)
            elif key == "UP":
                selected = (selected - 1) % len(choices)


def _pick_layout(
    choices: Sequence[str], option_letters: Sequence[str], horizontal_threshold: int
) -> str:
    term_width = shutil.get_terminal_size(fallback=(horizontal_threshold, 24)).columns
    boxes = [_build_box(str(choice), letter) for choice, letter in zip(choices, option_letters)]
    total_width = sum(box.width for box in boxes) + (len(boxes) - 1) * 2
    if len(boxes) <= 3 and total_width <= min(term_width, horizontal_threshold):
        return "horizontal"
    return "vertical"


class _Box:
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.width = max(len(line) for line in lines) if lines else 0


def _build_box(choice_text: str, label: str) -> _Box:
    raw_lines = choice_text.splitlines() or [""]
    labelled = [f"{label}) {raw_lines[0]}"]
    spacer = " " * (len(label) + 2)
    labelled.extend(f"{spacer}{line}" for line in raw_lines[1:])

    inner_width = max(len(line) for line in labelled)
    padded = [line.ljust(inner_width) for line in labelled]
    horizontal = "─" * (inner_width + 2)
    box_lines = [f"┌{horizontal}┐"]
    box_lines.extend(f"│ {line} │" for line in padded)
    box_lines.append(f"└{horizontal}┘")
    return _Box(box_lines)


def _render_choices(
    option_letters: Sequence[str],
    choices: Sequence[str],
    *,
    selected: int,
    layout: str,
) -> List[str]:
    boxes = [_build_box(str(choice), letter) for choice, letter in zip(choices, option_letters)]
    highlight = lambda line: f"{CYAN}{BOLD}{line}{RESET}"
    lines: List[str] = ["Utilise les flèches ou tape la lettre puis Entrée."]

    if layout == "horizontal":
        max_height = max(len(box.lines) for box in boxes)
        normalised: List[List[str]] = []
        for idx, box in enumerate(boxes):
            padded = box.lines + [" " * box.width] * (max_height - len(box.lines))
            if idx == selected:
                padded = [highlight(line) for line in padded]
            normalised.append(padded)

        for row in range(max_height):
            row_chunks = [box[row] for box in normalised]
            lines.append("  ".join(row_chunks))
        lines.append("")
    else:
        for idx, box in enumerate(boxes):
            content = box.lines
            if idx == selected:
                content = [highlight(line) for line in content]
            lines.extend(content)
            lines.append("")

    return lines


def _rewrite_block(lines: Sequence[str], previous_lines: int) -> None:
    if previous_lines:
        for _ in range(previous_lines):
            print("\033[F\033[K", end="")
    for line in lines:
        print(line)


def _read_key() -> str | None:
    if os.name == "nt" and msvcrt is not None:  # pragma: no cover - Windows
        key = msvcrt.getwch()
        if key in ("\r", "\n"):
            return "ENTER"
        if key in ("\x00", "\xe0"):
            arrow = msvcrt.getwch()
            return {"K": "LEFT", "M": "RIGHT", "H": "UP", "P": "DOWN"}.get(arrow)
        return key.lower()

    if termios is None or tty is None or not sys.stdin.isatty():
        return None

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        char = sys.stdin.read(1)
        if char in ("\r", "\n"):
            return "ENTER"
        if char == "\x1b":
            seq = sys.stdin.read(2)
            return {
                "[A": "UP",
                "[B": "DOWN",
                "[C": "RIGHT",
                "[D": "LEFT",
            }.get(seq)
        return char.lower()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


class CheckboxPrompt:
    """Interactive helper allowing learners to cocher plusieurs réponses."""

    def __init__(self, prompt: str, options: Sequence[str]) -> None:
        self.prompt = prompt
        self.options = list(options)
        self._selected: Set[int] = set()

    def _render(self) -> None:
        print()
        print(self.prompt)
        print("Tape le numéro pour (dé)cocher, 'v' pour valider, 'r' pour tout décocher.")
        for index, option in enumerate(self.options, start=1):
            mark = "☑" if index - 1 in self._selected else "☐"
            print(f"  {index}. {mark} {option}")

    def ask(self) -> List[int]:
        """Return the indices selected by the learner (zero-based)."""

        while True:
            self._render()
            choice = input("Choix : ").strip().lower()

            if choice in {"v", "valider"}:
                return sorted(self._selected)
            if choice in {"r", "reset", "effacer"}:
                self._selected.clear()
                continue

            try:
                numbers = _parse_numbers(choice)
            except ValueError:
                print("Entre un numéro valide, plusieurs séparés par des espaces, ou 'v'.")
                continue

            invalid = [n for n in numbers if n < 1 or n > len(self.options)]
            if invalid:
                print("Numéro en dehors de la liste. Réessaie.")
                continue

            for number in numbers:
                idx = number - 1
                if idx in self._selected:
                    self._selected.remove(idx)
                else:
                    self._selected.add(idx)


def _parse_numbers(value: str) -> List[int]:
    """Parse a whitespace-separated list of integers."""

    if not value:
        raise ValueError("empty")

    numbers: List[int] = []
    for chunk in value.split():
        number = int(chunk)
        numbers.append(number)
    return numbers

