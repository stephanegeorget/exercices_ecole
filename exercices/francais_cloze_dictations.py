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
import shutil
import string
import sys
import textwrap
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import pyperclip  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pyperclip = None  # type: ignore

from prompt_toolkit import Application
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
        j = i + 1
        while j < len(text) and not text[j].isspace():
            j += 1
        tokens.append(Token(text[i:j], masked=False))
        i = j
    return tokens


def mask_display_for_token(token: Token) -> str:
    if token.is_whitespace() or token.is_newline():
        return token.text
    length = len(token.text.strip()) or len(token.text)
    underscores = "_" * max(3, min(length, 12))
    trailing = ""
    leading = ""
    if token.text and token.text[0] in string.punctuation:
        leading = token.text[0]
    if token.text and token.text[-1] in string.punctuation and len(token.text) > 1:
        trailing = token.text[-1]
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
            answer = answers.get(index)
            if answer:
                parts.append(answer)
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
            parts.append(answers.get(index, mask_display_for_token(token)))
        else:
            parts.append(token.text)
    return "".join(parts)


def copy_attempt_to_clipboard(full_text: str, answers: Dict[int, str]) -> bool:
    """Copy student answers to the clipboard.

    Returns ``True`` on success, ``False`` if no clipboard backend was available.
    """

    payload = {
        "full_text": full_text,
        "answers": {str(k): v for k, v in sorted(answers.items()) if v},
    }
    combined = json.dumps(payload, indent=2, ensure_ascii=False)
    clipboard_text = combined

    try:
        app = get_app()
    except Exception:
        app = None
    success = False
    if app is not None and app.clipboard is not None:
        try:
            app.clipboard.set_data(ClipboardData(text=clipboard_text))
            success = True
        except Exception:
            success = False
    if not success and pyperclip is not None:
        try:
            pyperclip.copy(clipboard_text)
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


class ActionRadioList(RadioList):
    """RadioList that triggers a callback whenever a value is selected."""

    def __init__(
        self,
        values: Sequence[Tuple[Callable[[], None], str]],
        on_select: Optional[Callable[[Callable[[], None]], None]] = None,
    ) -> None:
        # ``select_on_focus=True`` ensures that the visual marker (``*``) moves
        # together with the focused entry when navigating with the arrow keys
        # (or any other navigation key).  This mirrors how most menu systems
        # operate: moving changes the highlighted option but does not activate
        # it until the user explicitly validates their choice.
        super().__init__(values, select_on_focus=True)
        self._on_select = on_select

        # ``RadioList`` already ships with comprehensive key bindings (arrows,
        # page up/down, vim keys, …).  We extend them so that ``Tab`` and
        # ``Shift-Tab`` can also be used to move through the menu, which is a
        # familiar pattern for users navigating interactive prompts.
        kb = self.control.key_bindings

        @kb.add("tab")
        def _tab(event) -> None:  # pragma: no cover - interactive behaviour
            if self.values:
                self._selected_index = (self._selected_index + 1) % len(self.values)
                event.app.invalidate()

        @kb.add("s-tab")
        def _shift_tab(event) -> None:  # pragma: no cover - interactive behaviour
            if self.values:
                self._selected_index = (self._selected_index - 1) % len(self.values)
                event.app.invalidate()

        @kb.add(" ")
        def _space(event) -> None:  # pragma: no cover - interactive behaviour
            self._handle_enter()

    def _handle_enter(self) -> None:
        super()._handle_enter()
        if not self.multiple_selection and self._on_select is not None:
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
                Label(text="Tab focus text • Shift+Tab focus title • Ctrl+S save • Esc back"),
            ]
        )
        return Frame(body)

    def on_show(self) -> None:
        self.app.application.layout.focus(self.title_input)

    def key_bindings(self) -> KeyBindings:
        kb = KeyBindings()

        @kb.add("tab", filter=has_focus(self.title_input))
        def _(event) -> None:
            event.app.layout.focus(self.text_input)

        @kb.add("s-tab", filter=has_focus(self.text_input))
        def _(event) -> None:
            event.app.layout.focus(self.title_input)

        @kb.add("c-s")
        def _(event) -> None:
            title = self.title_input.text.strip()
            text = self.text_input.text.rstrip()
            if not title:
                self.app.set_message("Title cannot be empty")
                return
            if not text:
                self.app.set_message("Text cannot be empty")
                return
            text_source = TextSource(
                id=generate_id("ts"),
                title=title,
                created_at=isoformat(utc_now()),
                text=text,
            )
            save_text_source(text_source)
            self.app.set_message("Text Source saved")
            self.app.set_screen(TeacherHomeScreen(self.app))

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
        self.radio = RadioList(options, select_on_focus=True)

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

    def key_bindings(self) -> KeyBindings:
        kb = KeyBindings()

        @kb.add("enter")
        def _(event) -> None:
            value = self.radio.current_value
            if value is None:
                return
            self.on_select_callback(value)

        return kb


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
        self.radio = RadioList(options, select_on_focus=True)

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

    def key_bindings(self) -> KeyBindings:
        kb = KeyBindings()

        @kb.add("enter")
        def _(event) -> None:
            value = self.radio.current_value
            if value is None:
                return
            self.on_select_callback(value)

        return kb


# ---------------------------------------------------------------------------
# Cloze Editor (Teacher)


class ClozeEditorScreen(Screen):
    def __init__(self, app: ClozeApp, cloze: Cloze, is_new: bool) -> None:
        super().__init__(app)
        self.cloze = cloze
        self.is_new = is_new
        self.cursor_index = 0
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
                            "Ctrl+T focus title • Ctrl+G focus gaps • Left/Right move • "
                            "Up mask • Down unmask • Tab next gap • Shift+Tab previous gap"
                        )
                    ),
                    Box(self.token_window, padding=1, style=""),
                    Label(text="Ctrl+A mask all • Ctrl+U unmask all • Ctrl+S save • Esc back"),
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
        self.app.application.layout.focus(self.token_window)

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
        self.cursor_index = max(0, min(len(self.cloze.tokens) - 1, self.cursor_index + delta))
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
            event.app.layout.focus(self.title_area)

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

        @kb.add("tab", filter=has_focus(self.token_window))
        def _(event) -> None:
            self._jump_masked(True)

        @kb.add("s-tab", filter=has_focus(self.token_window))
        def _(event) -> None:
            self._jump_masked(False)

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

        @kb.add("c-s")
        def _(event) -> None:
            title = self.title_area.text.strip()
            if not title:
                self.app.set_message("Title required before saving")
                return
            self.cloze.title = title
            if self.is_new and not self.cloze.id.startswith("cl_"):
                self.cloze.id = generate_id("cl")
            save_cloze(self.cloze)
            self.app.set_message("Cloze saved")
            self.app.set_screen(TeacherHomeScreen(self.app))

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
        self.radio = RadioList(items, select_on_focus=True)

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

    def key_bindings(self) -> KeyBindings:
        kb = KeyBindings()

        @kb.add("enter")
        def _(event) -> None:
            cloze = self.radio.current_value
            if cloze is None:
                return
            self.app.set_screen(StudentPracticeScreen(self.app, cloze))

        return kb


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
        self.control = FormattedTextControl(self._formatted_text, focusable=True)
        self.window = Window(self.control, wrap_lines=True, always_hide_cursor=True)
        self.container_widget = Frame(
            HSplit(
                [
                    Label(text="Left/Right move • Type to answer • Backspace/Delete edit"),
                    Label(text="Ctrl+R reveal • Ctrl+C copy • Ctrl+S save attempt • Esc back"),
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
                answer = self.answers.get(index, "")
                display = answer or mask_display_for_token(token)
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
        self.answers[self.cursor_index] = text
        self.app.application.invalidate()

    def _insert_text(self, text: str) -> None:
        current = self.answers.get(self.cursor_index, "")
        self.answers[self.cursor_index] = current + text
        self.app.application.invalidate()

    def _backspace(self) -> None:
        current = self.answers.get(self.cursor_index, "")
        if current:
            self.answers[self.cursor_index] = current[:-1]
            self.app.application.invalidate()

    def _delete(self) -> None:
        if self.cursor_index in self.answers:
            self.answers[self.cursor_index] = ""
            self.app.application.invalidate()

    def key_bindings(self) -> KeyBindings:
        kb = KeyBindings()

        @kb.add("left")
        def _(event) -> None:
            self._move_cursor(False)

        @kb.add("right")
        def _(event) -> None:
            self._move_cursor(True)

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

        @kb.add("c-c")
        def _(event) -> None:
            full_text = reconstructed_text(self.cloze.tokens, self.answers)
            success = copy_attempt_to_clipboard(full_text, self.answers)
            if success:
                self.app.set_message("Answers copied to clipboard")
            else:
                self.app.set_message("Clipboard unavailable. Printed answers to terminal.")

        @kb.add("c-s")
        def _(event) -> None:
            attempt = {
                "cloze_id": self.cloze.id,
                "started_at": self.cloze.created_at,
                "saved_at": isoformat(utc_now()),
                "answers": {str(k): v for k, v in self.answers.items() if v},
            }
            file_name = f"{self.cloze.id}_{datetime.utcnow():%Y%m%d_%H%M%S}.json"
            ensure_directories()
            atomic_write_json(ATTEMPTS_DIR / file_name, attempt)
            self.app.set_message("Attempt saved")

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

