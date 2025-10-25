"""Jeu de découverte d'une phrase mystère à partir d'une grille de lettres."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from prompt_toolkit import Application
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import HSplit, Layout, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style

DISPLAY_NAME = "Français : Danse des abeilles"


@dataclass(frozen=True)
class WordPlacement:
    """Represents a hidden word inside the letter matrix."""

    word: str
    coordinates: Tuple[Tuple[int, int], ...]
    sentence_index: int


GRID: List[List[str]] = [
    list("LESPLAGESX"),
    list("RABEILLESO"),
    list("MONTAGNESR"),
    list("DANSENTLUX"),
    list("ECOLETENTS"),
    list("QUPOURSITE"),
    list("HIVESFLOWN"),
    list("TENGUIDERS"),
    list("PLANELAXES"),
    list("TRUCHENEST"),
]

WORD_PLACEMENTS: Tuple[WordPlacement, ...] = (
    WordPlacement("LES", ((0, 0), (0, 1), (0, 2)), 0),
    WordPlacement("ABEILLES", tuple((1, col) for col in range(1, 9)), 1),
    WordPlacement("DANSENT", tuple((3, col) for col in range(0, 7)), 2),
    WordPlacement("POUR", tuple((5, col) for col in range(2, 6)), 3),
    WordPlacement("GUIDER", tuple((7, col) for col in range(3, 9)), 4),
    WordPlacement("LA", ((8, 5), (8, 6)), 5),
    WordPlacement("RUCHE", tuple((9, col) for col in range(1, 6)), 6),
)

MYSTERY_SENTENCE = [
    "Les",
    "abeilles",
    "dansent",
    "pour",
    "guider",
    "la",
    "ruche",
]


class MysterySentenceGame:
    """Interactive prompt_toolkit game for discovering a hidden sentence."""

    def __init__(self) -> None:
        self.cursor_row = 0
        self.cursor_col = 0
        self.current_word: Optional[WordPlacement] = None
        self.word_lookup: Dict[Tuple[int, int], WordPlacement] = {
            coord: placement for placement in WORD_PLACEMENTS for coord in placement.coordinates
        }
        self.typed_words: Dict[int, List[str]] = {placement.sentence_index: [] for placement in WORD_PLACEMENTS}
        self.completed_words: set[int] = set()
        self.message = "Utilise les flèches pour parcourir la grille. Tape les lettres pour copier le mot."\
            " Retour arrière efface la dernière lettre. Échap pour quitter."
        self._build_ui()

    # ------------------------------------------------------------------ UI --
    def _build_ui(self) -> None:
        """Create prompt_toolkit UI components."""

        self.grid_control = FormattedTextControl(self._render_grid, show_cursor=False)
        grid_window = Window(content=self.grid_control, dont_extend_width=False, always_hide_cursor=True)

        self.dictation_control = FormattedTextControl(self._render_dictation, show_cursor=False)
        dictation_window = Window(content=self.dictation_control, height=len(MYSTERY_SENTENCE) + 2)

        self.message_control = FormattedTextControl(self._render_message, show_cursor=False)
        message_window = Window(content=self.message_control, height=2)

        container = HSplit([grid_window, dictation_window, message_window])

        self.key_bindings = self._create_key_bindings()

        self.application = Application(
            layout=Layout(container),
            full_screen=True,
            key_bindings=self.key_bindings,
            mouse_support=False,
            style=self._build_style(),
        )

    def _build_style(self) -> Style:
        return Style.from_dict(
            {
                "grid": "",
                "grid.cursor": "underline",
                "grid.word-active": "bg:#005f87 #ffffff bold",
                "grid.word-complete": "fg:#00d75f bold",
                "dictation.label": "bold",
                "dictation.active": "bg:#ffd75f #000000 bold",
                "dictation.complete": "fg:#00d75f bold",
                "dictation.partial": "fg:#ffd75f",
                "message": "fg:#afafd7",
                "message.success": "fg:#5fdf5f bold",
            }
        )

    # --------------------------------------------------------------- render --
    def _render_grid(self) -> FormattedText:
        fragments: List[Tuple[str, str]] = []
        width = len(GRID[0])
        for row_index, row in enumerate(GRID):
            for col_index, letter in enumerate(row):
                style = "class:grid"
                word = self.word_lookup.get((row_index, col_index))
                if word:
                    if word.sentence_index in self.completed_words:
                        style = "class:grid.word-complete"
                    elif word == self.current_word:
                        style = "class:grid.word-active"
                elif row_index == self.cursor_row and col_index == self.cursor_col:
                    style = "class:grid.cursor"

                fragments.append((style, letter))
                if col_index != width - 1:
                    fragments.append(("", " "))

            if row_index != len(GRID) - 1:
                fragments.append(("", "\n"))

        return fragments

    def _render_dictation(self) -> FormattedText:
        fragments: List[Tuple[str, str]] = []
        fragments.append(("class:dictation.label", "\nPhrase mystère :\n"))
        for placement in sorted(WORD_PLACEMENTS, key=lambda wp: wp.sentence_index):
            index = placement.sentence_index
            typed = "".join(self.typed_words[index])
            target = placement.word
            display = typed.ljust(len(target), "_")
            if index in self.completed_words:
                style = "class:dictation.complete"
            elif placement == self.current_word:
                style = "class:dictation.active"
            elif typed:
                style = "class:dictation.partial"
            else:
                style = ""
            fragments.append((style, f"{display}  ({MYSTERY_SENTENCE[index]})\n"))
        return fragments

    def _render_message(self) -> FormattedText:
        style = "class:message.success" if self._is_finished() else "class:message"
        return [(style, self.message)]

    # --------------------------------------------------------------- helpers --
    def _create_key_bindings(self) -> KeyBindings:
        bindings = KeyBindings()

        @bindings.add("up")
        def _up(event) -> None:
            self._move_cursor(-1, 0)
            event.app.invalidate()

        @bindings.add("down")
        def _down(event) -> None:
            self._move_cursor(1, 0)
            event.app.invalidate()

        @bindings.add("left")
        def _left(event) -> None:
            self._move_cursor(0, -1)
            event.app.invalidate()

        @bindings.add("right")
        def _right(event) -> None:
            self._move_cursor(0, 1)
            event.app.invalidate()

        @bindings.add("backspace")
        def _backspace(event) -> None:
            self._handle_backspace()
            event.app.invalidate()

        @bindings.add("escape")
        def _escape(event) -> None:
            event.app.exit()

        @bindings.add(Keys.Any)
        def _any(event) -> None:
            data = event.data
            if data and data.isalpha():
                self._handle_character(data.upper())
                event.app.invalidate()

        return bindings

    def _move_cursor(self, delta_row: int, delta_col: int) -> None:
        new_row = max(0, min(self.cursor_row + delta_row, len(GRID) - 1))
        new_col = max(0, min(self.cursor_col + delta_col, len(GRID[0]) - 1))
        self.cursor_row = new_row
        self.cursor_col = new_col
        self.current_word = self.word_lookup.get((self.cursor_row, self.cursor_col))
        self._update_message()

    def _handle_character(self, char: str) -> None:
        if self.current_word is None:
            return
        index = self.current_word.sentence_index
        if index in self.completed_words:
            return
        typed = self.typed_words[index]
        target = self.current_word.word
        if len(typed) >= len(target):
            return
        typed.append(char)
        if len(typed) == len(target):
            if "".join(typed) == target:
                self.completed_words.add(index)
                self.message = "Bravo ! Le mot est correct."
                if self._is_finished():
                    self.message = "🎉🥳🌟 Félicitations ! Toutes les abeilles ont trouvé la ruche ! 🌟🥳🎉"
            else:
                self.message = "Oups, compare bien les lettres de la grille."
        else:
            self._update_message()

    def _handle_backspace(self) -> None:
        if self.current_word is None:
            return
        index = self.current_word.sentence_index
        if index in self.completed_words:
            return
        typed = self.typed_words[index]
        if typed:
            typed.pop()
        self._update_message()

    def _update_message(self) -> None:
        if self.current_word is None:
            letter = GRID[self.cursor_row][self.cursor_col]
            self.message = f"Case libre : lettre '{letter}'. Déplace-toi jusqu'à un mot caché."
        else:
            remaining = len(self.current_word.word) - len(self.typed_words[self.current_word.sentence_index])
            self.message = (
                f"Mot à copier : {self.current_word.word} — encore {remaining} lettre(s) à taper."
            )

    def _is_finished(self) -> bool:
        return len(self.completed_words) == len(WORD_PLACEMENTS)

    # ----------------------------------------------------------------- main --
    def run(self) -> None:
        self._move_cursor(0, 0)  # initialise selection
        self.application.run()


def main() -> None:
    game = MysterySentenceGame()
    game.run()


if __name__ == "__main__":
    main()
