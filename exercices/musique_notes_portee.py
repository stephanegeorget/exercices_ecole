from __future__ import annotations

"""Exercice interactif pour relier des notes à leur nom."""

import curses
from typing import Iterable

from .logger import log_result

DISPLAY_NAME = "Musique : Relier les notes sur la portée"

# Paramètres d'affichage de la portée ASCII.
STAFF_TOP = 5
STAFF_LEFT = 22
STAFF_WIDTH = 40
NOTE_SPACING = 5
MIN_HEIGHT = 24
MIN_WIDTH = 80
BUBBLE_WIDTH = 15

# Lignes de la portée (5 lignes espacées d'un interligne vide).
STAFF_LINES = [STAFF_TOP + i * 2 for i in range(5)]

# Description des notes visibles de gauche à droite : (nom, ligne, ligne supplémentaire).
NOTES_LAYOUT = [
    ("Do du bas", STAFF_TOP + 10, True),
    ("Ré", STAFF_TOP + 9, False),
    ("Fa", STAFF_TOP + 7, False),
    ("Sol", STAFF_TOP + 6, False),
    ("La", STAFF_TOP + 5, False),
    ("Si", STAFF_TOP + 4, False),
    ("Do du haut", STAFF_TOP + 3, False),
]


TREBLE_CLEF = [
    "   __",
    "  /  )",
    " /  /",
    "(  ( ",
    " \\  \\",
    "  \\__)",
    "   /",
    "  (_",
]

OPTION_LAYOUT = [
    ["Fa", "Sol"],
    ["Do du haut", "Ré"],
    ["Si", "La", "Do du bas"],
]

TOP_OPTIONS_ROW = STAFF_TOP - 3
MIDDLE_OPTIONS_ROW = STAFF_TOP + 11
BOTTOM_OPTIONS_ROW = STAFF_TOP + 15

OPTION_POSITIONS = {
    "Fa": (TOP_OPTIONS_ROW, STAFF_LEFT + 12),
    "Sol": (TOP_OPTIONS_ROW, STAFF_LEFT + 26),
    "Do du haut": (MIDDLE_OPTIONS_ROW, 2),
    "Ré": (MIDDLE_OPTIONS_ROW, STAFF_LEFT + STAFF_WIDTH + 2),
    "Si": (BOTTOM_OPTIONS_ROW, STAFF_LEFT + 2),
    "La": (BOTTOM_OPTIONS_ROW, STAFF_LEFT + 18),
    "Do du bas": (BOTTOM_OPTIONS_ROW, STAFF_LEFT + 34),
}


def _build_notes() -> list[dict[str, int | str | bool]]:
    """Prépare les informations nécessaires pour tracer les notes."""

    notes: list[dict[str, int | str | bool]] = []
    for index, (name, row, ledger) in enumerate(NOTES_LAYOUT):
        col = STAFF_LEFT + 4 + index * NOTE_SPACING
        notes.append({"name": name, "row": row, "col": col, "ledger": ledger})
    return notes


NOTES = _build_notes()
TOTAL_NOTES = len(NOTES)


def _first_available(solved: set[str]) -> tuple[int, int] | None:
    """Retourne la première bulle encore disponible."""

    for row_index, row in enumerate(OPTION_LAYOUT):
        for col_index, name in enumerate(row):
            if name not in solved:
                return row_index, col_index
    return None


def _move_horizontal(
    solved: set[str],
    position: tuple[int, int],
    direction: int,
) -> tuple[int, int]:
    """Déplace le curseur horizontalement en ignorant les bulles déjà utilisées."""

    row_index, col_index = position
    row = OPTION_LAYOUT[row_index]
    if not row:
        return position
    next_col = col_index
    for _ in range(len(row)):
        next_col = (next_col + direction) % len(row)
        if row[next_col] not in solved:
            return row_index, next_col
    return position


def _move_vertical(
    solved: set[str],
    position: tuple[int, int],
    direction: int,
) -> tuple[int, int]:
    """Déplace le curseur verticalement vers une ligne possédant une bulle libre."""

    row_index, col_index = position
    new_row = row_index
    while True:
        new_row += direction
        if new_row < 0 or new_row >= len(OPTION_LAYOUT):
            return position
        candidates = [
            idx for idx, name in enumerate(OPTION_LAYOUT[new_row]) if name not in solved
        ]
        if candidates:
            closest = min(candidates, key=lambda idx: abs(idx - col_index))
            return new_row, closest


def _draw_staff(stdscr: curses.window, highlight: int | None, solved: Iterable[str]) -> None:
    """Affiche la portée, la clé de sol et les notes."""

    for row in STAFF_LINES:
        stdscr.addstr(row, STAFF_LEFT - 1, "|" + "-" * STAFF_WIDTH + "|")

    clef_row = STAFF_TOP - 1
    clef_col = STAFF_LEFT - 5
    for line_index, line in enumerate(TREBLE_CLEF):
        for offset, char in enumerate(line):
            if char != " ":
                stdscr.addch(clef_row + line_index, clef_col + offset, char)

    solved_set = set(solved)
    for index, note in enumerate(NOTES):
        row = note["row"]
        col = note["col"]
        if note["ledger"]:
            stdscr.addstr(row, col - 2, "---")
        char = "o"
        attr = curses.A_BOLD
        if highlight is not None and index == highlight:
            char = "@"
            attr |= curses.A_REVERSE
        elif note["name"] in solved_set:
            char = "O"
        stdscr.addstr(row, col, char, attr)


def _draw_options(
    stdscr: curses.window,
    selection: tuple[int, int] | None,
    solved: Iterable[str],
) -> None:
    """Affiche les bulles contenant les noms des notes."""

    solved_set = set(solved)
    for row_index, row in enumerate(OPTION_LAYOUT):
        for col_index, name in enumerate(row):
            y, x = OPTION_POSITIONS[name]
            bubble = f"( {name} )"
            attr = curses.A_BOLD
            if name in solved_set:
                bubble = f"( {name} * )"
                attr = curses.A_DIM
            elif selection is not None and selection == (row_index, col_index):
                attr |= curses.A_REVERSE
            display = bubble.center(BUBBLE_WIDTH)
            stdscr.addstr(y, x, " " * BUBBLE_WIDTH)
            stdscr.addstr(y, x, display[:BUBBLE_WIDTH], attr)


def _draw_progress(
    stdscr: curses.window,
    solved_order: list[str],
    highlight: int | None,
) -> None:
    """Affiche la progression et la liste des bonnes réponses."""

    if highlight is None:
        text = f"Notes reliées : {TOTAL_NOTES}/{TOTAL_NOTES} (terminé)"
    else:
        text = f"Note à relier : {highlight + 1}/{TOTAL_NOTES}"
    stdscr.addstr(3, 4, text)

    stdscr.addstr(STAFF_TOP, 2, "Associations :")
    for index, name in enumerate(solved_order):
        stdscr.addstr(STAFF_TOP + 1 + index, 2, f" - {name}")


def _draw_feedback(stdscr: curses.window, message: str) -> None:
    """Affiche un message d'aide ou de correction en bas de l'écran."""

    max_y, max_x = stdscr.getmaxyx()
    row = max_y - 3
    width = max_x - 8
    if width <= 0:
        return
    truncated = message[: width]
    stdscr.addstr(row, 4, " " * width)
    stdscr.addstr(row, 4, truncated)


def _render(
    stdscr: curses.window,
    highlight: int | None,
    selection: tuple[int, int] | None,
    solved_order: list[str],
    solved: Iterable[str],
    feedback: str,
) -> None:
    """Rafraîchit l'affichage complet de l'exercice."""

    stdscr.erase()
    stdscr.addstr(0, 4, "Relie les notes à leur nom", curses.A_BOLD)
    stdscr.addstr(
        1,
        4,
        "Flèches pour naviguer • Entrée pour valider • q pour quitter",
        curses.A_DIM,
    )
    _draw_progress(stdscr, solved_order, highlight)
    _draw_options(stdscr, selection, solved)
    _draw_staff(stdscr, highlight, solved)
    _draw_feedback(stdscr, feedback)
    stdscr.refresh()


def _run_curses(stdscr: curses.window) -> dict[str, object]:
    """Boucle principale de l'exercice interactif."""

    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(False)

    max_y, max_x = stdscr.getmaxyx()
    if max_y < MIN_HEIGHT or max_x < MIN_WIDTH:
        stdscr.erase()
        stdscr.addstr(
            0,
            0,
            f"Fenêtre trop petite : {max_x}x{max_y} (minimum {MIN_WIDTH}x{MIN_HEIGHT}).",
        )
        stdscr.addstr(2, 0, "Agrandis le terminal puis relance l'exercice.")
        stdscr.addstr(4, 0, "Appuie sur une touche pour revenir au menu.")
        stdscr.refresh()
        stdscr.getch()
        return {"correct": 0, "total": TOTAL_NOTES, "completed": False}

    solved_names: set[str] = set()
    solved_order: list[str] = []
    selection = _first_available(solved_names)
    note_index = 0
    feedback = "Utilise les flèches pour choisir un nom, puis Entrée pour valider."
    aborted = False

    while note_index < TOTAL_NOTES:
        _render(stdscr, note_index, selection, solved_order, solved_names, feedback)
        key = stdscr.getch()
        if key in (ord("q"), 27):
            aborted = True
            break
        if selection is None:
            selection = _first_available(solved_names)
        if selection is None:
            break
        if key in (curses.KEY_LEFT, ord("h")):
            selection = _move_horizontal(solved_names, selection, -1)
        elif key in (curses.KEY_RIGHT, ord("l")):
            selection = _move_horizontal(solved_names, selection, 1)
        elif key in (curses.KEY_UP, ord("k")):
            selection = _move_vertical(solved_names, selection, -1)
        elif key in (curses.KEY_DOWN, ord("j")):
            selection = _move_vertical(solved_names, selection, 1)
        elif key in (curses.KEY_ENTER, 10, 13, ord(" ")):
            row_index, col_index = selection
            choice = OPTION_LAYOUT[row_index][col_index]
            current_note = NOTES[note_index]
            if choice == current_note["name"]:
                solved_names.add(choice)
                solved_order.append(choice)
                feedback = f"Bravo ! '{choice}' est bien la note surlignée."
                note_index += 1
                selection = _first_available(solved_names)
            else:
                feedback = f"Non, ce n'est pas '{choice}'. Essaie encore !"
        else:
            feedback = "Utilise les flèches pour te déplacer et Entrée pour valider."

    if note_index >= TOTAL_NOTES and not aborted:
        selection = None
        feedback = "Bravo ! Toutes les notes sont reliées. Appuie sur Entrée pour quitter."
        highlight: int | None = None
    else:
        highlight = note_index if note_index < TOTAL_NOTES else None
        if aborted:
            feedback = (
                "Exercice interrompu. Appuie sur Entrée ou 'q' pour revenir au menu."
            )
        else:
            feedback = "Appuie sur Entrée pour revenir au menu."

    _render(stdscr, highlight, selection, solved_order, solved_names, feedback)
    while True:
        key = stdscr.getch()
        if key in (10, 13, ord("q"), 27):
            break

    return {
        "correct": len(solved_names),
        "total": TOTAL_NOTES,
        "completed": not aborted and note_index >= TOTAL_NOTES,
    }


def main() -> None:
    """Lance l'exercice interactif de reconnaissance des notes."""

    try:
        result = curses.wrapper(_run_curses)
    except curses.error:
        print("Le terminal ne supporte pas l'affichage interactif de cet exercice.")
        log_result("musique_notes_portee", None)
        return

    correct = int(result["correct"])
    total = int(result["total"])
    completed = bool(result["completed"])
    score = (correct / total * 100) if total else 0.0

    if completed:
        print(f"Bravo ! Tu as relié {correct} note(s) sur {total}.")
    else:
        print(f"Tu as relié {correct} note(s) sur {total}. Reviens quand tu veux !")

    log_result("musique_notes_portee", score)


if __name__ == "__main__":
    main()
