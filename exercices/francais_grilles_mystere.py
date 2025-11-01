"""Jeux de phrases mystère basés sur des grilles de lettres."""

from __future__ import annotations

import random
import string
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Sequence, Tuple

from prompt_toolkit import Application
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import HSplit, Layout, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style

DISPLAY_NAME = "Français : Grilles mystère"


class Orientation(Enum):
    """Orientation d'un mot dans la grille."""

    LEFT_TO_RIGHT = (0, 1)
    TOP_TO_BOTTOM = (1, 0)
    RIGHT_TO_LEFT = (0, -1)  # prévu pour de futurs thèmes
    BOTTOM_TO_TOP = (-1, 0)  # prévu pour de futurs thèmes

    @property
    def delta(self) -> Tuple[int, int]:
        return self.value  # type: ignore[return-value]


ACTIVE_ORIENTATIONS: Tuple[Orientation, ...] = (
    Orientation.LEFT_TO_RIGHT,
    Orientation.TOP_TO_BOTTOM,
)


@dataclass(frozen=True)
class MysteryWord:
    """Mot de la phrase mystère."""

    display: str
    grid: str

    @classmethod
    def from_text(cls, text: str) -> "MysteryWord":
        return cls(display=text, grid=text.upper())


@dataclass(frozen=True)
class MysteryTheme:
    """Paramètres nécessaires pour générer une grille."""

    name: str
    words: Tuple[MysteryWord, ...]
    grid_size: Tuple[int, int] = (12, 12)
    filler_alphabet: str = string.ascii_uppercase
    show_words_in_dictation: bool = True

    def __post_init__(self) -> None:
        if not self.words:
            raise ValueError("Un thème doit contenir au moins un mot mystère.")

    @property
    def sentence(self) -> Tuple[str, ...]:
        return tuple(word.display for word in self.words)


@dataclass(frozen=True)
class WordPlacement:
    """Représente un mot caché dans la grille."""

    word: MysteryWord
    coordinates: Tuple[Tuple[int, int], ...]
    sentence_index: int


class GridGenerationError(RuntimeError):
    """Erreur levée quand un placement de mots échoue."""


def _generate_grid(theme: MysteryTheme, *, rng: random.Random) -> Tuple[List[List[str]], Tuple[WordPlacement, ...]]:
    rows, cols = theme.grid_size
    attempts = 0
    max_attempts = 200
    while attempts < max_attempts:
        attempts += 1
        grid: List[List[Optional[str]]] = [[None for _ in range(cols)] for _ in range(rows)]
        placements: List[WordPlacement] = []
        word_specs = list(enumerate(theme.words))
        rng.shuffle(word_specs)
        success = True
        for sentence_index, word in word_specs:
            placement = _place_word(word, sentence_index, grid, rng)
            if placement is None:
                success = False
                break
            placements.append(placement)
        if success:
            _fill_grid(grid, theme.filler_alphabet, rng)
            return [[cell or "X" for cell in row] for row in grid], tuple(placements)
    raise GridGenerationError(
        f"Impossible de générer une grille pour le thème '{theme.name}' après {max_attempts} essais."
    )


def _place_word(
    word: MysteryWord,
    sentence_index: int,
    grid: List[List[Optional[str]]],
    rng: random.Random,
) -> Optional[WordPlacement]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    orientation_options = list(ACTIVE_ORIENTATIONS)
    rng.shuffle(orientation_options)
    for orientation in orientation_options:
        delta_row, delta_col = orientation.delta
        candidate_starts = _candidate_starts(word.grid, rows, cols, delta_row, delta_col)
        rng.shuffle(candidate_starts)
        for start_row, start_col in candidate_starts:
            coords: List[Tuple[int, int]] = []
            valid = True
            row, col = start_row, start_col
            for letter in word.grid:
                cell = grid[row][col]
                if cell is not None:
                    valid = False
                    break
                coords.append((row, col))
                row += delta_row
                col += delta_col
            if valid:
                for (r, c), letter in zip(coords, word.grid):
                    grid[r][c] = letter
                return WordPlacement(word=word, coordinates=tuple(coords), sentence_index=sentence_index)
    return None


def _candidate_starts(
    word: str,
    rows: int,
    cols: int,
    delta_row: int,
    delta_col: int,
) -> List[Tuple[int, int]]:
    length = len(word)
    valid_starts: List[Tuple[int, int]] = []
    for row in range(rows):
        for col in range(cols):
            end_row = row + (length - 1) * delta_row
            end_col = col + (length - 1) * delta_col
            if 0 <= end_row < rows and 0 <= end_col < cols:
                valid_starts.append((row, col))
    return valid_starts


def _fill_grid(grid: List[List[Optional[str]]], alphabet: str, rng: random.Random) -> None:
    letters = alphabet or string.ascii_uppercase
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell is None:
                grid[row_index][col_index] = rng.choice(letters)


class MysterySentenceGame:
    """Jeu interactif basé sur prompt_toolkit pour découvrir une phrase."""

    def __init__(self, theme: MysteryTheme, *, rng: Optional[random.Random] = None) -> None:
        self.theme = theme
        self.rng = rng or random.Random()
        self.grid, self.placements = _generate_grid(theme, rng=self.rng)
        self.cursor_row = 0
        self.cursor_col = 0
        self.current_word: Optional[WordPlacement] = None
        self.word_lookup: Dict[Tuple[int, int], WordPlacement] = {
            coord: placement for placement in self.placements for coord in placement.coordinates
        }
        self.typed_words: Dict[int, List[str]] = {placement.sentence_index: [] for placement in self.placements}
        self.completed_words: set[int] = set()
        self.message = (
            "Utilise les flèches pour parcourir la grille. Tape les lettres pour copier le mot. "
            "Retour arrière efface la dernière lettre. Échap pour quitter."
        )
        self._build_ui()

    # ------------------------------------------------------------------ UI --
    def _build_ui(self) -> None:
        self.grid_control = FormattedTextControl(self._render_grid, show_cursor=False)
        grid_window = Window(content=self.grid_control, dont_extend_width=False, always_hide_cursor=True)

        self.dictation_control = FormattedTextControl(self._render_dictation, show_cursor=False)
        dictation_window = Window(content=self.dictation_control, height=len(self.theme.words) + 3)

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
                "grid.cursor": "reverse bold",
                "grid.word-active": "bg:#005f87 #ffffff bold",
                "grid.word-complete": "fg:#00d75f bold strikethrough",
                "dictation.label": "bold",
                "dictation.active": "bg:#ffd75f #000000 bold",
                "dictation.complete": "fg:#00d75f bold strikethrough",
                "dictation.partial": "fg:#ffd75f",
                "message": "fg:#afafd7",
                "message.success": "fg:#5fdf5f bold",
            }
        )

    # --------------------------------------------------------------- render --
    def _render_grid(self) -> FormattedText:
        fragments: List[Tuple[str, str]] = []
        width = len(self.grid[0])
        for row_index, row in enumerate(self.grid):
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

            if row_index != len(self.grid) - 1:
                fragments.append(("", "\n"))

        return fragments

    def _render_dictation(self) -> FormattedText:
        fragments: List[Tuple[str, str]] = []
        fragments.append(("class:dictation.label", f"\nPhrase mystère – {self.theme.name} :\n"))
        for placement in sorted(self.placements, key=lambda wp: wp.sentence_index):
            index = placement.sentence_index
            typed = "".join(self.typed_words[index])
            target = placement.word.grid
            display = typed.ljust(len(target), "_")
            if index in self.completed_words:
                style = "class:dictation.complete"
            elif placement == self.current_word:
                style = "class:dictation.active"
            elif typed:
                style = "class:dictation.partial"
            else:
                style = ""
            if self.theme.show_words_in_dictation:
                label = f"  ({placement.word.display})"
            else:
                label = ""
            fragments.append((style, f"{display}{label}\n"))
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
        new_row = max(0, min(self.cursor_row + delta_row, len(self.grid) - 1))
        new_col = max(0, min(self.cursor_col + delta_col, len(self.grid[0]) - 1))
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
        target = self.current_word.word.grid
        if len(typed) >= len(target):
            return
        typed.append(char)
        if len(typed) == len(target):
            if "".join(typed) == target:
                self.completed_words.add(index)
                self.message = "Bravo ! Le mot est correct."
                if self._is_finished():
                    self.message = "🎉🥳🌟 Félicitations ! Toute la phrase est révélée ! 🌟🥳🎉"
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
            letter = self.grid[self.cursor_row][self.cursor_col]
            self.message = f"Case libre : lettre '{letter}'. Déplace-toi jusqu'à un mot caché."
        else:
            remaining = len(self.current_word.word.grid) - len(self.typed_words[self.current_word.sentence_index])
            self.message = (
                f"Mot à copier : {self.current_word.word.grid} — encore {remaining} lettre(s) à taper."
            )

    def _is_finished(self) -> bool:
        return len(self.completed_words) == len(self.placements)

    # ----------------------------------------------------------------- main --
    def run(self) -> None:
        self._move_cursor(0, 0)
        self.application.run()


BEES_THEME = MysteryTheme(
    name="Danse des abeilles",
    words=(
        MysteryWord.from_text("Les"),
        MysteryWord.from_text("abeilles"),
        MysteryWord.from_text("dansent"),
        MysteryWord.from_text("pour"),
        MysteryWord.from_text("guider"),
        MysteryWord.from_text("la"),
        MysteryWord.from_text("ruche"),
    ),
    grid_size=(10, 10),
    filler_alphabet="ABEILPRSTUXDNOGH",
    show_words_in_dictation=True,
)

FOREST_THEME = MysteryTheme(
    name="Balade en forêt enchantée",
    words=(
        MysteryWord.from_text("Braves"),
        MysteryWord.from_text("enfants"),
        MysteryWord.from_text("suivent"),
        MysteryWord.from_text("le"),
        MysteryWord.from_text("sentier"),
        MysteryWord.from_text("lumineux"),
        MysteryWord.from_text("ce"),
        MysteryWord.from_text("soir"),
    ),
    grid_size=(12, 12),
    filler_alphabet="FORESTLUMIABCDXYZ",
    show_words_in_dictation=False,
)

THEMES: Tuple[MysteryTheme, ...] = (
    BEES_THEME,
    FOREST_THEME,
)


def _choose_theme(themes: Sequence[MysteryTheme]) -> Optional[MysteryTheme]:
    while True:
        print("Choisissez un thème :")
        for index, theme in enumerate(themes, start=1):
            print(f"{index}. {theme.name}")
        print("0. Retour")
        choice = input("Votre choix : ")
        if choice == "0":
            return None
        try:
            index = int(choice) - 1
            return themes[index]
        except (ValueError, IndexError):
            print("Choix invalide. Merci de réessayer.")


def main() -> None:
    rng = random.Random()
    theme = _choose_theme(THEMES)
    if theme is None:
        return
    game = MysterySentenceGame(theme, rng=rng)
    game.run()


if __name__ == "__main__":
    main()
