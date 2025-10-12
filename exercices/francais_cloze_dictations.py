"""Terminal application for creating and practising cloze dictations.

This module implements a fairly feature-complete TUI using prompt_toolkit
covering both the teacher and student workflows described in the
specification.  The file intentionally contains most of the application logic
so that it can be launched both from ``python -m exercices`` and directly via
``python main.py``.

The implementation is intentionally self-contained and avoids external
frameworks so the file is longer than typical modules.  The overall structure
is:

* Data models and persistence helpers
* Utility helpers (tokenisation, rendering, clipboard support)
* The ``ClozeApp`` class that orchestrates the prompt_toolkit Application
* Screen objects for each major workflow (menus, editors, practice view)

The UI uses prompt_toolkit widgets because they are portable across terminals
and operating systems.  Each screen exposes a container and a set of
key-bindings that ``ClozeApp`` merges into the global application bindings.

The application stores JSON files under ``data/`` and ensures atomic writes so
the files remain valid even if the program crashes mid-save.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import shutil
import string
import sys
import textwrap
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple, TypeVar

try:
    import pyperclip  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pyperclip = None  # type: ignore

from prompt_toolkit import Application
from prompt_toolkit.buffer import SelectionType
from prompt_toolkit.application.current import get_app
from prompt_toolkit.application.run_in_terminal import run_in_terminal
from prompt_toolkit.clipboard import ClipboardData
from prompt_toolkit.filters import has_focus
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import HSplit, Layout, VSplit
from prompt_toolkit.layout.containers import Container, DynamicContainer, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Frame, Label, RadioList, TextArea


DISPLAY_NAME = "Français : Dictées à trous (Cloze)"


# ---------------------------------------------------------------------------
# Data model definitions


DATA_DIR = Path("data")
TEXT_SOURCE_DIR = DATA_DIR / "text_sources"
CLOZE_DIR = DATA_DIR / "clozes"
ATTEMPTS_DIR = DATA_DIR / "attempts"


def ensure_directories() -> None:
    """Ensure the data folders exist."""

    for path in (DATA_DIR, TEXT_SOURCE_DIR, CLOZE_DIR, ATTEMPTS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def utc_now() -> datetime:
    return datetime.utcnow().replace(microsecond=0)


def isoformat(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_id(prefix: str) -> str:
    return f"{prefix}_{datetime.utcnow():%Y%m%d_%H%M%S_%f}"


def atomic_write_json(path: Path, data: dict) -> None:
    """Atomically write JSON data to ``path``."""

    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.flush()
        os.fsync(fh.fileno())
    tmp_path.replace(path)


def prompt_confirmation(message: str) -> bool:
    """Prompt the user for confirmation, returning ``True`` if accepted."""

    confirmed = False

    def _ask() -> None:
        nonlocal confirmed
        try:
            answer = input(f"{message} [y/N]: ").strip().lower()
        except EOFError:
            confirmed = False
        else:
            confirmed = answer in {"y", "yes"}

    run_in_terminal(_ask)
    return confirmed


@dataclass
class Token:
    text: str
    masked: bool = False

    def is_newline(self) -> bool:
        return self.text == "\n"

    def is_whitespace(self) -> bool:
        return self.text.strip("\n\r ") == "" and not self.is_newline()

    def is_word(self) -> bool:
        if self.is_newline() or self.is_whitespace():
            return False
        stripped = self.text.strip(string.punctuation)
        return bool(stripped)


@dataclass
class TextSource:
    id: str
    title: str
    created_at: str
    text: str

    @classmethod
    def from_json(cls, data: dict) -> "TextSource":
        return cls(
            id=data["id"],
            title=data["title"],
            created_at=data["created_at"],
            text=data["text"],
        )

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at,
            "text": self.text,
        }


@dataclass
class Cloze:
    id: str
    title: str
    created_at: str
    source_id: str
    tokens: List[Token] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict) -> "Cloze":
        return cls(
            id=data["id"],
            title=data["title"],
            created_at=data["created_at"],
            source_id=data["source_id"],
            tokens=[Token(**token) for token in data.get("tokens", [])],
        )

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at,
            "source_id": self.source_id,
            "tokens": [token.__dict__ for token in self.tokens],
        }


# ---------------------------------------------------------------------------
# Data layer helpers


def load_text_sources() -> List[TextSource]:
    ensure_directories()
    text_sources: List[TextSource] = []
    for path in sorted(TEXT_SOURCE_DIR.glob("*.json")):
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            text_sources.append(TextSource.from_json(data))
        except Exception as exc:  # pragma: no cover - user facing feedback
            print(f"Failed to load text source {path.name}: {exc}", file=sys.stderr)
    text_sources.sort(key=lambda ts: ts.created_at, reverse=True)
    return text_sources


def save_text_source(text_source: TextSource) -> None:
    ensure_directories()
    path = TEXT_SOURCE_DIR / f"{text_source.id}.json"
    atomic_write_json(path, text_source.to_json())


def load_clozes() -> List[Cloze]:
    ensure_directories()
    clozes: List[Cloze] = []
    for path in sorted(CLOZE_DIR.glob("*.json")):
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            clozes.append(Cloze.from_json(data))
        except Exception as exc:  # pragma: no cover - user facing feedback
            print(f"Failed to load cloze {path.name}: {exc}", file=sys.stderr)
    clozes.sort(key=lambda cl: cl.created_at, reverse=True)
    return clozes


def save_cloze(cloze: Cloze) -> None:
    ensure_directories()
    path = CLOZE_DIR / f"{cloze.id}.json"
    atomic_write_json(path, cloze.to_json())


# ---------------------------------------------------------------------------
# Token helpers


APOSTROPHE_CHARS = {"'", "’"}
WORD_SEPARATOR_PUNCTUATION = {ch for ch in string.punctuation if ch not in APOSTROPHE_CHARS}


def _core_bounds(text: str) -> Tuple[int, int]:
    start = 0
    end = len(text)
    while start < end and text[start] in WORD_SEPARATOR_PUNCTUATION:
        start += 1
    while end > start and text[end - 1] in WORD_SEPARATOR_PUNCTUATION:
        end -= 1
    return start, end


def token_answer_length(token: Token) -> int:
    if token.is_whitespace() or token.is_newline():
        return 0
    start, end = _core_bounds(token.text)
    core_length = end - start
    if core_length <= 0:
        stripped = token.text.strip()
        return len(stripped)
    return core_length


def sanitize_answer_display(answer: str, expected_length: int) -> str:
    display = re.sub(r"\s", "_", answer)
    if expected_length > 0:
        if len(display) < expected_length:
            display = display + "_" * (expected_length - len(display))
        else:
            display = display[:expected_length]
    return display


def answer_display_for_token(token: Token, answer: str) -> str:
    """Return the formatted answer keeping surrounding punctuation intact."""

    expected_length = token_answer_length(token)
    core = sanitize_answer_display(answer, expected_length)
    start, end = _core_bounds(token.text)
    leading = token.text[:start]
    trailing = token.text[end:]
    return f"{leading}{core}{trailing}"


def tokenize(text: str) -> List[Token]:
    """Split text into tokens while keeping whitespace tokens."""

    tokens: List[Token] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\n":
            tokens.append(Token("\n", masked=False))
            i += 1
            continue
        if ch.isspace():
            j = i + 1
            while j < len(text) and text[j].isspace() and text[j] != "\n":
                j += 1
            tokens.append(Token(text[i:j], masked=False))
            i = j
            continue
        if ch in WORD_SEPARATOR_PUNCTUATION:
            j = i + 1
            while j < len(text) and text[j] in WORD_SEPARATOR_PUNCTUATION:
                j += 1
            tokens.append(Token(text[i:j], masked=False))
            i = j
            continue
        j = i + 1
        while j < len(text) and not text[j].isspace() and text[j] not in WORD_SEPARATOR_PUNCTUATION:
            j += 1
        tokens.append(Token(text[i:j], masked=False))
        i = j
    return tokens


def mask_display_for_token(token: Token) -> str:
    if token.is_whitespace() or token.is_newline():
        return token.text

    text = token.text
    start, end = _core_bounds(text)

    core_length = end - start
    if core_length <= 0:
        core_length = len(text.strip()) or len(text)

    underscores = "_" * core_length
    leading = text[:start]
    trailing = text[end:]
    return f"{leading}{underscores}{trailing}"


def render_tokens(tokens: Sequence[Token], answers: Optional[Dict[int, str]] = None,
                  reveal_map: Optional[Dict[int, bool]] = None) -> str:
    """Return a text representation of ``tokens`` with answers applied."""

    answers = answers or {}
    reveal_map = reveal_map or {}
    parts: List[str] = []
    for index, token in enumerate(tokens):
        if token.is_newline():
            parts.append("\n")
            continue
        if token.is_whitespace():
            parts.append(token.text)
            continue
        if token.masked:
            expected_length = token_answer_length(token)
            answer = answers.get(index, "")
            if answer:
                parts.append(answer_display_for_token(token, answer))
            elif reveal_map.get(index):
                parts.append(token.text)
            else:
                parts.append(mask_display_for_token(token))
        else:
            parts.append(token.text)
    return "".join(parts)


def reconstructed_text(tokens: Sequence[Token], answers: Dict[int, str]) -> str:
    parts: List[str] = []
    for index, token in enumerate(tokens):
        if token.is_newline():
            parts.append("\n")
        elif token.is_whitespace():
            parts.append(token.text)
        elif token.masked:
            expected_length = token_answer_length(token)
            answer = answers.get(index, "")
            if answer:
                parts.append(answer_display_for_token(token, answer))
            else:
                parts.append(mask_display_for_token(token))
        else:
            parts.append(token.text)
    return "".join(parts)


def copy_attempt_to_clipboard(text_representation: str, answers: Dict[int, str]) -> bool:
    """Copy the current practise text and answers to the clipboard.

    Returns ``True`` on success, ``False`` if no clipboard backend was available.
    """

    payload = text_representation
    if answers:
        answers_json = json.dumps({str(k): v for k, v in sorted(answers.items()) if v}, indent=2, ensure_ascii=False)
        payload = f"{text_representation}\n\nAnswers:\n{answers_json}"
    clipboard_text = payload

    try:
        app = get_app()
    except Exception:
        app = None
    success = False
    if pyperclip is not None:
        try:
            pyperclip.copy(clipboard_text)
            success = True
        except Exception:
            success = False
    if not success and app is not None and app.clipboard is not None:
        try:
            app.clipboard.set_data(ClipboardData(text=clipboard_text))
            success = True
        except Exception:
            success = False
    if not success:
        run_in_terminal(lambda: print("Copy failed. Data:\n" + clipboard_text))
    return success


# ---------------------------------------------------------------------------
# UI scaffolding


class Screen:
    """Base class for UI screens."""

    title: str = ""

    def __init__(self, app: "ClozeApp") -> None:
        self.app = app

    def container(self) -> Container:
        raise NotImplementedError

    def key_bindings(self) -> KeyBindings:
        return KeyBindings()

    def on_show(self) -> None:
        """Hook when the screen becomes active."""


class ClozeApp:
    """Application controller managing prompt_toolkit Application."""

    style = Style.from_dict(
        {
            "status": "reverse",
            "message": "reverse",
            "menu-title": "bold underline",
            "token.current": "reverse",
            "token.masked": "underline",
        }
    )

    def __init__(self, demo: bool = False, reset_demo: bool = False) -> None:
        ensure_directories()
        if reset_demo:
            self._reset_demo()
        if demo:
            self._seed_demo()

        self.message: str = ""
        self.mode: str = "Home"
        self.current_screen: Optional[Screen] = None

        self.global_bindings = KeyBindings()
        self.global_bindings.add("escape")(self._handle_escape)

        self._container = DynamicContainer(self._current_container)
        self.layout = Layout(
            HSplit(
                [
                    Window(
                        height=1,
                        content=FormattedTextControl(self._statusbar_text),
                        style="class:status",
                    ),
                    self._container,
                    Window(
                        height=1,
                        content=FormattedTextControl(self._message_text),
                        style="class:message",
                    ),
                ]
            )
        )

        self.application = Application(
            layout=self.layout,
            key_bindings=self.global_bindings,
            style=self.style,
            full_screen=True,
        )

    # ------------------------------------------------------------------
    # Demo helpers

    def _reset_demo(self) -> None:
        for directory in (TEXT_SOURCE_DIR, CLOZE_DIR):
            for path in directory.glob("demo_*.json"):
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass

    def _seed_demo(self) -> None:
        sample_text = textwrap.dedent(
            """
            The quick brown fox jumps over the lazy dog.
            This classic pangram contains every letter of the alphabet.
            """
        ).strip()
        text_id = "demo_text_source"
        text_source = TextSource(
            id=f"demo_{text_id}",
            title="Demo Pangram",
            created_at=isoformat(utc_now()),
            text=sample_text,
        )
        save_text_source(text_source)

        cloze_id = "demo_cloze"
        tokens = tokenize(sample_text)
        masked_indices = {i for i, token in enumerate(tokens) if token.is_word() and token.text.lower() in {"quick", "lazy"}}
        for i in masked_indices:
            tokens[i].masked = True
        cloze = Cloze(
            id=f"demo_{cloze_id}",
            title="Demo Cloze",
            created_at=isoformat(utc_now()),
            source_id=text_source.id,
            tokens=tokens,
        )
        save_cloze(cloze)

    # ------------------------------------------------------------------
    # General helpers

    def _statusbar_text(self) -> FormattedText:
        parts = [
            ("", f" Mode: {self.mode} "),
            ("", "• Ctrl+S Save  "),
            ("", "• Ctrl+C Copy (Student)  "),
            ("", "• Esc Back"),
        ]
        if isinstance(self.current_screen, StudentPracticeScreen):
            parts.insert(1, ("", f" Cloze: {self.current_screen.cloze.title} "))
        elif isinstance(self.current_screen, ClozeEditorScreen):
            parts.insert(1, ("", f" Editing: {self.current_screen.title_text} "))
        return FormattedText(parts)

    def _message_text(self) -> str:
        return self.message

    def set_message(self, message: str, duration: float = 3.0) -> None:
        self.message = message
        self.application.invalidate()

        async def clear() -> None:
            await asyncio.sleep(duration)
            self.message = ""
            self.application.invalidate()

        try:
            self.application.create_background_task(clear())
        except RuntimeError:
            # Application not running yet; ignore.
            pass

    def _current_container(self) -> Container:
        """Return the container for the active screen.

        ``prompt_toolkit`` initialises the layout while the application is
        constructed, before any screen has been selected.  On the very first
        run ``self.current_screen`` is still ``None`` which previously caused
        an ``AttributeError`` when the dynamic container tried to access
        ``.container()``.  Returning a minimal placeholder window avoids the
        crash until ``set_screen`` is invoked.
        """

        if self.current_screen is not None:
            return self.current_screen.container()
        return Window(content=FormattedTextControl(""))

    def set_screen(self, screen: Screen) -> None:
        self.current_screen = screen
        screen.on_show()
        bindings = merge_key_bindings([self.global_bindings, screen.key_bindings()])
        self.application.key_bindings = bindings
        self.application.invalidate()

    def run(self) -> None:
        self.goto_main_menu()
        self.application.run()

    # Navigation -------------------------------------------------------

    def goto_main_menu(self) -> None:
        self.mode = "Home"
        self.set_screen(MainMenuScreen(self))

    def goto_teacher_home(self) -> None:
        self.mode = "Teacher"
        self.set_screen(TeacherHomeScreen(self))

    def goto_student_home(self) -> None:
        self.mode = "Student"
        self.set_screen(StudentSelectClozeScreen(self))

    def _handle_escape(self, event) -> None:
        if isinstance(self.current_screen, MainMenuScreen):
            event.app.exit()
        else:
            self.goto_main_menu()


# ---------------------------------------------------------------------------
# Menu utilities


T = TypeVar("T")


class ActionRadioList(RadioList):
    """``RadioList`` variant that notifies a callback on explicit selection."""

    def __init__(
        self,
        values: Sequence[Tuple[T, str]],
        on_select: Optional[Callable[[T], None]] = None,
    ) -> None:
        # ``select_on_focus=True`` keeps the visual marker (``*``) in sync with
        # the currently highlighted option.  We suppress the activation callback
        # for navigation keys so that moving through the menu never triggers the
        # associated action until ``Enter`` or ``Space`` is pressed.
        super().__init__(values, select_on_focus=True)
        self._on_select: Optional[Callable[[T], None]] = on_select

        kb = self.control.key_bindings

        @kb.add("tab")
        def _tab(event) -> None:  # pragma: no cover - interactive behaviour
            if self.values:
                self._selected_index = (self._selected_index + 1) % len(self.values)
                self._handle_enter()
                event.app.invalidate()

        @kb.add("s-tab")
        def _shift_tab(event) -> None:  # pragma: no cover - interactive behaviour
            if self.values:
                self._selected_index = (self._selected_index - 1) % len(self.values)
                self._handle_enter()
                event.app.invalidate()

        @kb.add("enter", eager=True)
        @kb.add(" ", eager=True)
        def _activate(event) -> None:  # pragma: no cover - interactive behaviour
            self._activate_current()

    def _handle_enter(self) -> None:  # type: ignore[override]
        # Update the selected value without triggering callbacks.  This method
        # is called by the base navigation handlers (arrow keys, page up/down,
        # ...).  By keeping it side-effect free we ensure that moving the focus
        # never validates the choice.
        RadioList._handle_enter(self)

    def _activate_current(self) -> None:
        RadioList._handle_enter(self)
        if self._on_select is not None:
            self._on_select(self.current_value)


class MenuScreen(Screen):
    """Simple vertical menu screen based on a RadioList."""

    menu_title: str = ""
    options: Sequence[Tuple[str, Callable[[], None]]]
    help_text: str = (
        "Up/Down or Tab navigate • Shift-Tab go up • Enter/Space select • Esc back"
    )

    def __init__(self, app: ClozeApp) -> None:
        super().__init__(app)
        values = [(callback, label) for label, callback in self.options]
        self.radio = ActionRadioList(values, on_select=self._handle_selection)

    def _handle_selection(self, callback: Callable[[], None]) -> None:
        if callback:
            callback()

    def container(self):
        body = HSplit(
            [
                Label(text=self.menu_title, style="class:menu-title"),
                Box(self.radio, padding=1, padding_left=2, padding_right=2),
                Label(text=self.help_text),
            ]
        )
        return Frame(body)

    def on_show(self) -> None:
        self.app.application.layout.focus(self.radio)


class MainMenuScreen(MenuScreen):
    menu_title = "Cloze Dictation"

    def __init__(self, app: ClozeApp) -> None:
        self.options = [
            ("Teacher: Create/Edit", app.goto_teacher_home),
            ("Student: Practice", app.goto_student_home),
            ("Quit", lambda: app.application.exit()),
        ]
        super().__init__(app)


class TeacherHomeScreen(MenuScreen):
    menu_title = "Teacher Mode"

    def __init__(self, app: ClozeApp) -> None:
        self.options = [
            ("Create new Text Source", lambda: app.set_screen(TextSourceEditorScreen(app))),
            (
                "Create Cloze from existing Text Source",
                lambda: app.set_screen(SelectTextSourceScreen(app, on_select=self._create_cloze)),
            ),
            (
                "Edit existing Cloze",
                lambda: app.set_screen(SelectClozeScreen(app, on_select=self._edit_cloze)),
            ),
            ("Back", app.goto_main_menu),
        ]
        super().__init__(app)

    def _open_cloze_editor(self, text_source: TextSource) -> None:
        tokens = tokenize(text_source.text)
        cloze = Cloze(
            id=generate_id("cl"),
            title="",
            created_at=isoformat(utc_now()),
            source_id=text_source.id,
            tokens=tokens,
        )
        editor = ClozeEditorScreen(self.app, cloze=cloze, is_new=True)
        self.app.set_screen(editor)

    def _edit_cloze(self, cloze: Cloze) -> None:
        editor = ClozeEditorScreen(self.app, cloze=cloze, is_new=False)
        self.app.set_screen(editor)

    def _create_cloze(self, text_source: TextSource) -> None:
        self._open_cloze_editor(text_source)


# ---------------------------------------------------------------------------
# Text Source creation


class TextSourceEditorScreen(Screen):
    title = "Create Text Source"

    def __init__(self, app: ClozeApp) -> None:
        super().__init__(app)
        self.title_input = TextArea(multiline=False, prompt="Title: ")
        self.text_input = TextArea(
            multiline=True,
            scrollbar=True,
            wrap_lines=True,
        )

    def container(self):
        body = HSplit(
            [
                Label(text="Create new Text Source"),
                self.title_input,
                Frame(self.text_input, title="Text"),
                Label(text="Tab focus text • Shift+Tab focus title • Esc save & return"),
            ]
        )
        return Frame(body)

    def on_show(self) -> None:
        self.app.application.layout.focus(self.title_input)

    def _has_unsaved_changes(self) -> bool:
        current_title = self.title_input.text.strip()
        current_text = self.text_input.text.rstrip()
        return bool(current_title or current_text)

    def _save_text_source(self) -> bool:
        title = self.title_input.text.strip()
        text = self.text_input.text.rstrip()
        if not title:
            self.app.set_message("Title cannot be empty")
            self.app.application.layout.focus(self.title_input)
            return False
        if not text:
            self.app.set_message("Text cannot be empty")
            self.app.application.layout.focus(self.text_input)
            return False
        text_source = TextSource(
            id=generate_id("ts"),
            title=title,
            created_at=isoformat(utc_now()),
            text=text,
        )
        save_text_source(text_source)
        self.app.set_message("Text Source saved")
        return True

    def key_bindings(self) -> KeyBindings:
        kb = KeyBindings()

        @kb.add("tab", filter=has_focus(self.title_input))
        def _(event) -> None:
            event.app.layout.focus(self.text_input)

        @kb.add("s-tab", filter=has_focus(self.text_input))
        def _(event) -> None:
            event.app.layout.focus(self.title_input)

        @kb.add("escape", eager=True)
        def _(event) -> None:
            if not self._has_unsaved_changes():
                self.app.goto_teacher_home()
                return
            if self._save_text_source():
                self.app.goto_teacher_home()

        return kb


# ---------------------------------------------------------------------------
# Selection helpers


class SelectTextSourceScreen(Screen):
    def __init__(self, app: ClozeApp, on_select: Callable[[TextSource], None]) -> None:
        super().__init__(app)
        self.on_select_callback = on_select
        self.sources = load_text_sources()
        if self.sources:
            options = [
                (
                    ts,
                    f"{ts.title} — {ts.created_at}",
                )
                for ts in self.sources
            ]
        else:
            options = [(None, "No text sources available")]
        self.radio = ActionRadioList(options, on_select=self._handle_selection)

    def container(self):
        body = HSplit(
            [
                Label(text="Select Text Source", style="class:menu-title"),
                Box(self.radio, padding=1),
                Label(text="Up/Down navigate • Enter select • Esc back"),
            ]
        )
        return Frame(body)

    def on_show(self) -> None:
        self.app.application.layout.focus(self.radio)

    def _handle_selection(self, value: Optional[TextSource]) -> None:
        if value is None:
            return
        self.on_select_callback(value)


class SelectClozeScreen(Screen):
    def __init__(self, app: ClozeApp, on_select: Callable[[Cloze], None]) -> None:
        super().__init__(app)
        self.on_select_callback = on_select
        self.clozes = load_clozes()
        if self.clozes:
            options = []
            sources = {ts.id: ts for ts in load_text_sources()}
            for cloze in self.clozes:
                source_title = sources.get(cloze.source_id, TextSource(cloze.source_id, "Unknown", "", "")).title
                options.append((cloze, f"{cloze.title} — {cloze.created_at} — {source_title}"))
        else:
            options = [(None, "No clozes available")]
        self.radio = ActionRadioList(options, on_select=self._handle_selection)

    def container(self):
        body = HSplit(
            [
                Label(text="Select Cloze", style="class:menu-title"),
                Box(self.radio, padding=1),
                Label(text="Up/Down navigate • Enter select • Esc back"),
            ]
        )
        return Frame(body)

    def on_show(self) -> None:
        self.app.application.layout.focus(self.radio)

    def _handle_selection(self, value: Optional[Cloze]) -> None:
        if value is None:
            return
        self.on_select_callback(value)


# ---------------------------------------------------------------------------
# Cloze Editor (Teacher)


class ClozeEditorScreen(Screen):
    def __init__(self, app: ClozeApp, cloze: Cloze, is_new: bool) -> None:
        super().__init__(app)
        self.cloze = cloze
        self.is_new = is_new
        self.cursor_index = 0
        self._original_title = cloze.title.strip()
        self._original_masks = [token.masked for token in cloze.tokens]
        self.title_area = TextArea(
            text=cloze.title,
            multiline=False,
            prompt="Cloze title: ",
        )
        self.token_control = FormattedTextControl(self._formatted_tokens, focusable=True)
        self.token_window = Window(content=self.token_control, wrap_lines=True, always_hide_cursor=True)
        self.container_widget = Frame(
            HSplit(
                [
                    self.title_area,
                    Label(
                        text=(
                            "Tab focus gaps • Shift+Tab previous gap • Ctrl+I next gap • "
                            "Ctrl+T focus title • Ctrl+G focus gaps • "
                            "Left/Right move • Up mask • Down unmask"
                        )
                    ),
                    Box(self.token_window, padding=1, style=""),
                    Label(text="Ctrl+A mask all • Ctrl+U unmask all • Esc save & return"),
                ]
            ),
            title="Cloze Editor",
        )

    @property
    def title_text(self) -> str:
        return self.title_area.text.strip() or "(untitled)"

    def container(self):
        return self.container_widget

    def on_show(self) -> None:
        self._focus_title(select_all=True)

    def _focus_title(self, select_all: bool = False) -> None:
        """Move focus to the title field, optionally selecting the contents."""

        layout = self.app.application.layout
        layout.focus(self.title_area)
        buffer = self.title_area.buffer
        if select_all:
            # Select from the start to the end so typing replaces the whole
            # title.  ``start_selection`` records the *current* cursor
            # position, so move to the beginning first and then extend the
            # selection to the end of the text.
            buffer.cursor_position = 0
            buffer.start_selection(selection_type=SelectionType.CHARACTERS)
            buffer.cursor_position = len(buffer.text)
        else:
            buffer.selection_state = None
            buffer.cursor_position = len(buffer.text)

    def _has_unsaved_changes(self) -> bool:
        current_title = self.title_area.text.strip()
        if current_title != self._original_title:
            return True
        current_masks = [token.masked for token in self.cloze.tokens]
        return current_masks != self._original_masks

    def _save_cloze(self) -> bool:
        title = self.title_area.text.strip()
        if not title:
            self.app.set_message("Title required before saving")
            self._focus_title(select_all=True)
            return False
        self.cloze.title = title
        if self.is_new and not self.cloze.id.startswith("cl_"):
            self.cloze.id = generate_id("cl")
        save_cloze(self.cloze)
        self.app.set_message("Cloze saved")
        return True

    def _formatted_tokens(self) -> FormattedText:
        fragments: List[Tuple[str, str]] = []
        for index, token in enumerate(self.cloze.tokens):
            display: str
            style = ""
            if token.is_newline():
                fragments.append((style, "\n"))
                continue
            if token.is_whitespace():
                fragments.append((style, token.text))
                continue
            if token.masked:
                display = mask_display_for_token(token)
                style += " class:token.masked"
            else:
                display = token.text
            if index == self.cursor_index:
                style += " class:token.current"
            fragments.append((style, display + ""))
        return FormattedText(fragments)

    def _move_cursor(self, delta: int) -> None:
        if not self.cloze.tokens:
            return
        index = self.cursor_index
        limit = len(self.cloze.tokens)
        while True:
            index += delta
            if index < 0 or index >= limit:
                break
            if self.cloze.tokens[index].is_word():
                self.cursor_index = index
                break
        self.app.application.invalidate()

    def _mask_current(self, value: bool) -> None:
        token = self.cloze.tokens[self.cursor_index]
        if not token.is_word():
            return
        token.masked = value
        self.app.application.invalidate()

    def _jump_masked(self, forward: bool) -> None:
        masked_indices = [i for i, token in enumerate(self.cloze.tokens) if token.masked]
        if not masked_indices:
            return
        current = self.cursor_index
        if forward:
            for index in masked_indices:
                if index > current:
                    self.cursor_index = index
                    break
            else:
                self.cursor_index = masked_indices[0]
        else:
            for index in reversed(masked_indices):
                if index < current:
                    self.cursor_index = index
                    break
            else:
                self.cursor_index = masked_indices[-1]
        self.app.application.invalidate()

    def key_bindings(self) -> KeyBindings:
        kb = KeyBindings()

        @kb.add("c-t")
        def _(event) -> None:
            self._focus_title(select_all=True)

        @kb.add("c-g")
        def _(event) -> None:
            event.app.layout.focus(self.token_window)

        @kb.add("left")
        def _(event) -> None:
            self._move_cursor(-1)

        @kb.add("right")
        def _(event) -> None:
            self._move_cursor(1)

        @kb.add("up")
        def _(event) -> None:
            self._mask_current(True)

        @kb.add("down")
        def _(event) -> None:
            self._mask_current(False)

        @kb.add("tab", filter=has_focus(self.title_area))
        def _(event) -> None:
            event.app.layout.focus(self.token_window)

        @kb.add(Keys.BackTab, filter=has_focus(self.token_window))
        def _(event) -> None:
            self._jump_masked(False)

        @kb.add(Keys.ControlI, filter=has_focus(self.token_window))
        def _(event) -> None:
            self._jump_masked(True)

        @kb.add("tab", filter=has_focus(self.token_window))
        def _(event) -> None:
            self._focus_title(select_all=False)

        @kb.add("c-a")
        def _(event) -> None:
            for token in self.cloze.tokens:
                if token.is_word():
                    token.masked = True
            self.app.application.invalidate()

        @kb.add("c-u")
        def _(event) -> None:
            for token in self.cloze.tokens:
                token.masked = False
            self.app.application.invalidate()

        @kb.add("escape", eager=True)
        def _(event) -> None:
            if not self._has_unsaved_changes():
                self.app.goto_teacher_home()
                return
            if self._save_cloze():
                self.app.goto_teacher_home()

        return kb


# ---------------------------------------------------------------------------
# Student mode screens


class StudentSelectClozeScreen(Screen):
    def __init__(self, app: ClozeApp) -> None:
        super().__init__(app)
        clozes = load_clozes()
        sources = {ts.id: ts for ts in load_text_sources()}
        if clozes:
            items = []
            for cloze in clozes:
                source_title = sources.get(cloze.source_id, TextSource(cloze.source_id, "Unknown", "", "")).title
                items.append((cloze, f"{cloze.title} — {cloze.created_at} — {source_title}"))
        else:
            items = [(None, "No cloze dictations available")]
        self.radio = ActionRadioList(items, on_select=self._handle_selection)

    def container(self):
        body = HSplit(
            [
                Label(text="Select a Cloze to practise", style="class:menu-title"),
                Box(self.radio, padding=1),
                Label(text="Up/Down navigate • Enter select • Esc back"),
            ]
        )
        return Frame(body)

    def on_show(self) -> None:
        self.app.application.layout.focus(self.radio)

    def _handle_selection(self, cloze: Optional[Cloze]) -> None:
        if cloze is None:
            return
        self.app.set_screen(StudentPracticeScreen(self.app, cloze))


class StudentPracticeScreen(Screen):
    def __init__(self, app: ClozeApp, cloze: Cloze) -> None:
        super().__init__(app)
        self.cloze = cloze
        self.answers: Dict[int, str] = {}
        self.revealed: Dict[int, bool] = {}
        self.masked_indices = [i for i, token in enumerate(cloze.tokens) if token.masked]
        self.cursor_index = self.masked_indices[0] if self.masked_indices else 0
        self.no_gaps = not self.masked_indices
        if self.no_gaps:
            self.app.set_message("This cloze has no gaps. Press Esc to return.")
        self._autosave_path = ATTEMPTS_DIR / f"{self.cloze.id}_autosave.json"
        self._last_saved_snapshot: Tuple[Tuple[int, str], ...] = ()
        self._last_saved_revealed: Tuple[int, ...] = ()
        self._autosave_notified = False
        self._load_autosave()
        self.control = FormattedTextControl(self._formatted_text, focusable=True)
        self.window = Window(self.control, wrap_lines=True, always_hide_cursor=True)
        self.container_widget = Frame(
            HSplit(
                [
                    Label(text="Left/Right or Tab/Shift+Tab move • Type to answer • Backspace/Delete edit"),
                    Label(text="Ctrl+R reveal • Ctrl+C copy • Progress auto-saved • Esc back"),
                    Box(self.window, padding=1),
                ]
            ),
            title=f"Practice: {cloze.title}",
        )

    def container(self):
        return self.container_widget

    def on_show(self) -> None:
        self.app.application.layout.focus(self.window)

    def _formatted_text(self) -> FormattedText:
        fragments: List[Tuple[str, str]] = []
        for index, token in enumerate(self.cloze.tokens):
            style = ""
            if token.is_newline():
                fragments.append((style, "\n"))
                continue
            if token.is_whitespace():
                fragments.append((style, token.text))
                continue
            if token.masked:
                expected_length = token_answer_length(token)
                answer = self.answers.get(index, "")
                if answer:
                    display = answer_display_for_token(token, answer)
                else:
                    display = mask_display_for_token(token)
                if self.revealed.get(index) and not answer:
                    display = token.text
                if index == self.cursor_index:
                    style += " class:token.current"
                fragments.append((style, display))
            else:
                fragments.append((style, token.text))
        return FormattedText(fragments)

    # Navigation ------------------------------------------------------

    def _move_cursor(self, forward: bool) -> None:
        if not self.masked_indices:
            return
        current_pos = self.masked_indices.index(self.cursor_index)
        if forward:
            current_pos = (current_pos + 1) % len(self.masked_indices)
        else:
            current_pos = (current_pos - 1) % len(self.masked_indices)
        self.cursor_index = self.masked_indices[current_pos]
        self.app.application.invalidate()

    def _set_answer(self, text: str) -> None:
        token = self.cloze.tokens[self.cursor_index]
        limit = token_answer_length(token)
        if limit > 0:
            text = text[:limit]
        self.answers[self.cursor_index] = text
        self.app.application.invalidate()
        self._save_progress(auto=True)

    def _insert_text(self, text: str) -> None:
        token = self.cloze.tokens[self.cursor_index]
        limit = token_answer_length(token)
        current = self.answers.get(self.cursor_index, "")
        new_text = current + text
        if limit > 0:
            new_text = new_text[:limit]
        self.answers[self.cursor_index] = new_text
        self.app.application.invalidate()
        self._save_progress(auto=True)

    def _backspace(self) -> None:
        current = self.answers.get(self.cursor_index, "")
        if current:
            self.answers[self.cursor_index] = current[:-1]
            if not self.answers[self.cursor_index]:
                self.answers.pop(self.cursor_index)
            self.app.application.invalidate()
            self._save_progress(auto=True)

    def _delete(self) -> None:
        if self.cursor_index in self.answers:
            self.answers.pop(self.cursor_index, None)
            self.app.application.invalidate()
            self._save_progress(auto=True)

    def _answers_snapshot(self) -> Tuple[Tuple[int, str], ...]:
        return tuple(sorted((index, text) for index, text in self.answers.items() if text))

    def _revealed_snapshot(self) -> Tuple[int, ...]:
        return tuple(sorted(index for index, value in self.revealed.items() if value))

    def _load_autosave(self) -> None:
        """Restore saved progress for the current cloze if available."""

        if not self._autosave_path.exists():
            return
        try:
            with self._autosave_path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            self.app.set_message("Previous progress could not be restored.")
            return
        if data.get("cloze_id") != self.cloze.id:
            return
        answers = data.get("answers", {}) or {}
        restored_answers: Dict[int, str] = {}
        for key, value in answers.items():
            try:
                index = int(key)
            except (TypeError, ValueError):
                continue
            if index in self.masked_indices and isinstance(value, str) and value:
                restored_answers[index] = value
        if restored_answers:
            self.answers.update(restored_answers)
        revealed = data.get("revealed", {}) or {}
        restored_revealed: Dict[int, bool] = {}
        for key, value in revealed.items():
            if not value:
                continue
            try:
                index = int(key)
            except (TypeError, ValueError):
                continue
            if index in self.masked_indices:
                restored_revealed[index] = True
        if restored_revealed:
            self.revealed.update(restored_revealed)
        if restored_answers or restored_revealed:
            for index in self.masked_indices:
                if not self.answers.get(index):
                    self.cursor_index = index
                    break
            self._last_saved_snapshot = self._answers_snapshot()
            self._last_saved_revealed = self._revealed_snapshot()
            self.app.set_message("Previous progress restored")

    def _save_progress(self, auto: bool) -> None:
        if self.no_gaps:
            return
        answers_snapshot = self._answers_snapshot()
        revealed_snapshot = self._revealed_snapshot()
        if auto and answers_snapshot == self._last_saved_snapshot and revealed_snapshot == self._last_saved_revealed:
            return
        ensure_directories()
        payload = {
            "cloze_id": self.cloze.id,
            "started_at": self.cloze.created_at,
            "saved_at": isoformat(utc_now()),
            "answers": {str(k): v for k, v in answers_snapshot},
        }
        if revealed_snapshot:
            payload["revealed"] = {str(index): True for index in revealed_snapshot}
        payload["auto_saved"] = auto
        if auto:
            path = self._autosave_path
        else:
            file_name = f"{self.cloze.id}_{datetime.utcnow():%Y%m%d_%H%M%S}.json"
            path = ATTEMPTS_DIR / file_name
        atomic_write_json(path, payload)
        self._last_saved_snapshot = answers_snapshot
        self._last_saved_revealed = revealed_snapshot
        if auto:
            if not self._autosave_notified:
                self.app.set_message("Progress saved automatically")
                self._autosave_notified = True
        else:
            self.app.set_message("Attempt saved")

    def key_bindings(self) -> KeyBindings:
        kb = KeyBindings()

        @kb.add("left")
        def _(event) -> None:
            self._move_cursor(False)
            self._save_progress(auto=True)

        @kb.add("right")
        def _(event) -> None:
            self._move_cursor(True)
            self._save_progress(auto=True)

        @kb.add("tab")
        def _(event) -> None:
            self._move_cursor(True)
            self._save_progress(auto=True)

        @kb.add("s-tab")
        def _(event) -> None:
            self._move_cursor(False)
            self._save_progress(auto=True)

        @kb.add("backspace")
        def _(event) -> None:
            self._backspace()

        @kb.add("delete")
        def _(event) -> None:
            self._delete()

        @kb.add("c-r")
        def _(event) -> None:
            current = self.revealed.get(self.cursor_index, False)
            self.revealed[self.cursor_index] = not current
            self.app.application.invalidate()
            self._save_progress(auto=True)

        @kb.add("c-c")
        def _(event) -> None:
            snapshot = reconstructed_text(self.cloze.tokens, self.answers)
            success = copy_attempt_to_clipboard(snapshot, self.answers)
            if success:
                self.app.set_message("Answers copied to clipboard")
            else:
                self.app.set_message("Clipboard unavailable. Printed answers to terminal.")

        @kb.add("c-s")
        def _(event) -> None:
            self._save_progress(auto=False)

        @kb.add("escape")
        def _(event) -> None:
            self.app.goto_student_home()

        @kb.add(Keys.Any)
        def _(event) -> None:
            if not self.masked_indices:
                return
            if len(event.data) == 1 and event.data.isprintable():
                self._insert_text(event.data)

        return kb


# ---------------------------------------------------------------------------
# Entry point


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cloze Dictation TUI")
    parser.add_argument("--demo", action="store_true", help="Seed the application with demo data")
    parser.add_argument(
        "--reset-demo", action="store_true", help="Remove demo data before starting"
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    app = ClozeApp(demo=args.demo, reset_demo=args.reset_demo)
    try:
        app.run()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

