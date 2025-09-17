"""Quiz interactif sur l'appartenance de points à des objets géométriques."""

from __future__ import annotations

DISPLAY_NAME = "Géométrie : Appartenance ∈ / ∉"

import os
import sys
from dataclasses import dataclass
from typing import List

from .logger import log_result
from .utils import show_lesson

if os.name == "nt":
    import msvcrt  # pragma: no cover - Windows specific
else:  # pragma: no cover - attribute only used for type checking
    msvcrt = None  # type: ignore[assignment]

try:
    import termios
    import tty
except ImportError:  # pragma: no cover - Windows fallback
    termios = None  # type: ignore[assignment]
    tty = None  # type: ignore[assignment]


BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


@dataclass
class Question:
    """Structure décrivant une question du quiz."""

    label: str
    template: str
    answer: str

    def render(self) -> str:
        return f"{self.label}) {self.template.format(symbol='_____')}"


OPTIONS: List[str] = ["∈", "∉"]
LEFT_KEYS = {"\x1b[D", "\xe0K"}
RIGHT_KEYS = {"\x1b[C", "\xe0M"}
ENTER_KEYS = {"\r", "\n", "\r\n"}


def read_key() -> str:
    """Lit une touche du clavier et renvoie sa représentation."""

    if os.name == "nt" and msvcrt is not None:  # pragma: no cover - Windows only
        key = msvcrt.getwch()
        if key in ("\x00", "\xe0"):
            key += msvcrt.getwch()
        return key

    if termios is None or tty is None:  # pragma: no cover - improbable fallback
        return sys.stdin.read(1)

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        first = sys.stdin.read(1)
        if first == "\x1b":
            second = sys.stdin.read(1)
            if second == "[":
                third = sys.stdin.read(1)
                return first + second + third
            return first + second
        return first
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def choose_symbol() -> str:
    """Permet à l'élève de choisir entre ∈ et ∉ avec les flèches."""

    index = 0
    prompt_printed = False
    while True:
        options_display = "  ".join(
            f"[{symbol}]" if i == index else f" {symbol} "
            for i, symbol in enumerate(OPTIONS)
        )
        if not prompt_printed:
            print("Utilise les flèches gauche/droite puis appuie sur Entrée.")
            prompt_printed = True
        print(f"\r{options_display}    ", end="", flush=True)
        key = read_key()
        if key in LEFT_KEYS:
            index = (index - 1) % len(OPTIONS)
        elif key in RIGHT_KEYS:
            index = (index + 1) % len(OPTIONS)
        elif key in ENTER_KEYS or key == "\r":
            print()
            return OPTIONS[index]
        elif key == "\x03":  # Ctrl+C
            raise KeyboardInterrupt


def main() -> None:
    """Affiche la leçon puis lance le quiz d'appartenance."""

    lesson = f"""
{CYAN}{BOLD}📐  Appartenance : symboles ∈ et ∉  📐{RESET}

- (d1) est la droite horizontale passant par les points F, A et B.
- (d2) est la droite oblique passant par les points D, A et G.
- Le segment [FG] relie directement F à G.
- La demi-droite [FA) part de F et passe par A en continuant vers B.

Le symbole {BOLD}∈{RESET} signifie « appartient à ».
Le symbole {BOLD}∉{RESET} signifie « n'appartient pas à ».
"""
    figure = f"""
Figure :
      D •
         ╲
          ╲(d2)
           ╲
F •─────────•─────────• B
  (d1)      A╲
              ╲
               • G
"""
    show_lesson(lesson + figure)

    questions = [
        Question("a", "F {{symbol}} (AB)", "∈"),
        Question("b", "G {{symbol}} (d1)", "∉"),
        Question("c", "D {{symbol}} [FG]", "∉"),
        Question("d", "B {{symbol}} [FA)", "∈"),
        Question("e", "F {{symbol}} (d2)", "∉"),
        Question("f", "F {{symbol}} [BA)", "∈"),
        Question("g", "D {{symbol}} [DG]", "∈"),
        Question("h", "G {{symbol}} (FD)", "∉"),
        Question("i", "A {{symbol}} (d2)", "∈"),
    ]

    print("Observe la figure puis réponds aux questions :")
    print(
        "(Conseil : l'expression [BA) désigne la demi-droite qui part de B en"
        " direction de A.)"
    )

    score = 0
    for question in questions:
        print()
        print(figure)
        print(question.render())
        try:
            choice = choose_symbol()
        except KeyboardInterrupt:
            print("\nQuiz interrompu.")
            log_result("geometrie_appartenance", None)
            return
        if choice == question.answer:
            print(f"{GREEN}Bravo ! ✅{RESET}")
            score += 1
        else:
            print(
                f"{RED}Oups ! ❌  La bonne réponse était {question.answer}.{RESET}"
            )

    total = len(questions)
    print(
        f"\n{BOLD}Score final : {score}/{total}"
        f"  soit {score / total * 100:.0f}%{RESET}"
    )
    log_result("geometrie_appartenance", score / total * 100)


if __name__ == "__main__":
    main()
