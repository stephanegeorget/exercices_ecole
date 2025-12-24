# Refactoring Plan: Sequencer Objects in francais_cloze_dictations.py

## Executive Summary

The **francais_cloze_dictations.py** file (1,594 LOC) contains the primary "sequencer" pattern in this codebase: the **ClozeApp** class, which orchestrates workflow transitions between different screens in a Terminal UI application. This plan outlines how to refactor this complex file into smaller, more comprehensible pieces while maintaining the overall functionality and complexity.

**Target File**: `exercices/francais_cloze_dictations.py`
**Current Size**: 1,594 lines
**Classes**: 16
**Methods**: 94

---

## Complexity Analysis

### Current Sequencer Architecture

```
ClozeApp (Application Controller - Lines 539-745)
├── Navigation Methods (Workflow Sequencer)
│   ├── goto_main_menu()
│   ├── goto_teacher_home()
│   ├── goto_student_home()
│   └── set_screen() - Core sequencing method
│
├── Screen Base Class (Lines 425-441)
│   └── Abstract interface for all screens
│
└── Screen Implementations
    ├── MainMenuScreen (47 lines)
    ├── TeacherHomeScreen (62 lines)
    ├── TextSourceEditorScreen (86 lines)
    ├── SelectTextSourceScreen (36 lines)
    ├── SelectClozeScreen (38 lines)
    ├── ClozeEditorScreen (209 lines) ⚠️
    └── StudentPracticeScreen (262 lines) ⚠️ MOST COMPLEX
```

### Complexity Hotspots

| Component | Lines | Issues |
|-----------|-------|--------|
| **StudentPracticeScreen** | 262 | • 13 methods<br>• 64-line key_bindings()<br>• 45-line _load_autosave()<br>• Complex state management (answers, revealed, cursor) |
| **ClozeEditorScreen** | 209 | • 14 methods<br>• Token masking/unmasking logic<br>• Cursor navigation across words |
| **Helper functions** | ~400 | • tokenize() - State machine<br>• render_tokens() - Conditional rendering<br>• Clipboard operations |

---

## Refactoring Strategy

### Phase 1: Extract Core Data Operations (No Behavior Change)

**Goal**: Separate data layer from UI layer

#### 1.1 Create `francais_cloze_dictations/models.py`

Extract data models and persistence:

```python
# Move from main file:
- Token dataclass (lines 126-141)
- TextSource dataclass (lines 144-166)
- Cloze dataclass (lines 169-193)
- ensure_directories()
- utc_now(), isoformat(), generate_id()
- atomic_write_json()
- load_text_sources(), save_text_source()
- load_clozes(), save_cloze()
```

**Lines reduced**: ~200 lines → separate file
**Benefit**: Clear separation of data layer

#### 1.2 Create `francais_cloze_dictations/text_processing.py`

Extract text processing utilities:

```python
# Move from main file:
- tokenize() (lines 290-322)
- mask_display_for_token() (lines 323-337)
- render_tokens() (lines 340-366)
- reconstructed_text() (lines 368-385)
- token_answer_length() (lines 258-267)
- sanitize_answer_display() (lines 269-277)
- answer_display_for_token() (lines 279-287)
- _core_bounds() (lines 248-256)
```

**Lines reduced**: ~150 lines → separate file
**Benefit**: Isolated text processing logic

#### 1.3 Create `francais_cloze_dictations/clipboard.py`

Extract clipboard operations:

```python
# Move from main file:
- copy_attempt_to_clipboard() (lines 387-423)
- pyperclip import handling
```

**Lines reduced**: ~40 lines → separate file
**Benefit**: Optional dependency isolation

---

### Phase 2: Refactor StudentPracticeScreen (Reduce Complexity)

**Current**: 262 lines, 13 methods
**Target**: 4 smaller classes with single responsibilities

#### 2.1 Extract `StudentPracticeState` (State Management)

Create a dedicated state object:

```python
class StudentPracticeState:
    """Manages student answers, reveals, and cursor position."""

    def __init__(self, cloze: Cloze):
        self.cloze = cloze
        self.answers: Dict[int, str] = {}
        self.revealed: Dict[int, bool] = {}
        self.masked_indices = [i for i, t in enumerate(cloze.tokens) if t.masked]
        self.cursor_index = self.masked_indices[0] if self.masked_indices else 0

    def move_cursor(self, forward: bool) -> None:
        """Navigate to next/previous masked token."""
        # Extract from _move_cursor()

    def set_answer(self, text: str) -> None:
        """Set complete answer for current cursor position."""
        # Extract from _set_answer()

    def insert_text(self, text: str) -> None:
        """Append text to current answer."""
        # Extract from _insert_text()

    def backspace(self) -> None:
        """Remove last character from current answer."""
        # Extract from _backspace()

    def delete_answer(self) -> None:
        """Clear current answer completely."""
        # Extract from _delete()

    def toggle_reveal(self) -> None:
        """Reveal or hide the current answer."""
        # New method extracted from key_bindings()

    def answers_snapshot(self) -> Tuple[Tuple[int, str], ...]:
        """Return sorted snapshot of non-empty answers."""
        # Extract from _answers_snapshot()

    def revealed_snapshot(self) -> Tuple[int, ...]:
        """Return sorted snapshot of revealed indices."""
        # Extract from _revealed_snapshot()
```

**Lines reduced**: ~80 lines → separate class
**Benefit**: State changes isolated, easier to test

#### 2.2 Extract `StudentPracticeAutosave` (Persistence)

Create autosave manager:

```python
class StudentPracticeAutosave:
    """Handles automatic saving and restoration of student progress."""

    def __init__(self, cloze_id: str):
        self.autosave_path = ATTEMPTS_DIR / f"{cloze_id}_autosave.json"
        self.last_saved_answers: Tuple[Tuple[int, str], ...] = ()
        self.last_saved_revealed: Tuple[int, ...] = ()
        self.notified = False

    def load(self, state: StudentPracticeState) -> bool:
        """Restore saved progress. Returns True if progress was restored."""
        # Extract from _load_autosave() (45 lines)
        # Separate JSON parsing, validation, state restoration

    def save(self, state: StudentPracticeState, auto: bool) -> None:
        """Save current progress."""
        # Extract from _save_progress() (31 lines)
        # Separate snapshot comparison, JSON creation, file writing

    def needs_save(self, state: StudentPracticeState) -> bool:
        """Check if state has changed since last save."""
        # Extracted logic from _save_progress()
```

**Lines reduced**: ~90 lines → separate class
**Benefit**: Persistence logic isolated, clearer autosave behavior

#### 2.3 Refactor `key_bindings()` (64 lines → 10 handler methods)

Current structure (all in one method):

```python
def key_bindings(self) -> KeyBindings:
    kb = KeyBindings()

    @kb.add("left")
    def _(event): self._move_cursor(False); self._save_progress(auto=True)

    @kb.add("right")
    def _(event): self._move_cursor(True); self._save_progress(auto=True)

    # ... 8 more handlers
```

**Proposed structure** (extract handlers as methods):

```python
def key_bindings(self) -> KeyBindings:
    kb = KeyBindings()
    kb.add("left")(self._handle_cursor_left)
    kb.add("right")(self._handle_cursor_right)
    kb.add("tab")(self._handle_tab)
    kb.add("s-tab")(self._handle_shift_tab)
    kb.add("backspace")(self._handle_backspace)
    kb.add("delete")(self._handle_delete)
    kb.add("c-r")(self._handle_reveal)
    kb.add("c-c")(self._handle_copy)
    kb.add("c-s")(self._handle_save)
    kb.add("escape")(self._handle_escape)
    kb.add(Keys.Any)(self._handle_text_input)
    return kb

def _handle_cursor_left(self, event) -> None:
    """Move cursor to previous gap."""
    self.state.move_cursor(forward=False)
    self.autosave.save(self.state, auto=True)
    self.app.application.invalidate()

# ... other handlers (2-5 lines each)
```

**Lines reduced**: 64 lines → 11 methods (~3 lines each) + 12-line registration
**Benefit**: Each handler is testable, readable, and has a clear purpose

#### 2.4 Simplified StudentPracticeScreen

After extraction:

```python
class StudentPracticeScreen(Screen):
    """Student practice interface for cloze exercises."""

    def __init__(self, app: ClozeApp, cloze: Cloze):
        super().__init__(app)
        self.cloze = cloze
        self.state = StudentPracticeState(cloze)
        self.autosave = StudentPracticeAutosave(cloze.id)
        self.autosave.load(self.state)  # Restore progress

        # UI setup
        self.control = FormattedTextControl(self._formatted_text, focusable=True)
        self.window = Window(self.control, wrap_lines=True, always_hide_cursor=True)
        self.container_widget = self._build_container()

    def _formatted_text(self) -> FormattedText:
        """Render tokens with current answers and cursor position."""
        # Keep current implementation (25 lines)
        # Now uses self.state.answers, self.state.revealed, self.state.cursor_index

    def _build_container(self) -> Container:
        """Build the UI container."""
        # Extracted from __init__

    def container(self) -> Container:
        return self.container_widget

    def on_show(self) -> None:
        self.app.application.layout.focus(self.window)

    def key_bindings(self) -> KeyBindings:
        # New streamlined version (see 2.3)

    # 11 handler methods (2-5 lines each)
    def _handle_cursor_left(self, event) -> None: ...
    def _handle_cursor_right(self, event) -> None: ...
    # ... etc.
```

**Result**: 262 lines → ~120 lines (with state/autosave extracted)
**Benefit**: Clear responsibilities, easier to understand flow

---

### Phase 3: Refactor ClozeEditorScreen (Reduce Complexity)

**Current**: 209 lines, 14 methods
**Target**: Extract word navigation and masking logic

#### 3.1 Extract `WordNavigator` (Cursor Management)

```python
class WordNavigator:
    """Handles cursor navigation across word tokens."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.word_indices = [i for i, t in enumerate(tokens) if t.is_word()]
        self.cursor_index = self.word_indices[0] if self.word_indices else 0

    def move_cursor(self, forward: bool) -> None:
        """Move to next/previous word."""
        # Extract from ClozeEditorScreen._move_cursor()

    def current_token(self) -> Token:
        """Get token at cursor position."""
        return self.tokens[self.cursor_index]
```

#### 3.2 Extract `MaskingController` (Token Masking Logic)

```python
class MaskingController:
    """Manages token masking operations."""

    def toggle_mask(self, token: Token) -> None:
        """Toggle mask state of a token."""
        # Extract from ClozeEditorScreen._toggle_mask()

    def mask_all_words(self, tokens: List[Token]) -> None:
        """Mask all word tokens."""
        # Extract from ClozeEditorScreen._mask_all()

    def unmask_all_words(self, tokens: List[Token]) -> None:
        """Unmask all word tokens."""
        # Extract from ClozeEditorScreen._unmask_all()
```

#### 3.3 Simplified ClozeEditorScreen

```python
class ClozeEditorScreen(Screen):
    """Editor for creating cloze exercises."""

    def __init__(self, app: ClozeApp, text_source: TextSource, existing: Cloze = None):
        super().__init__(app)
        self.text_source = text_source

        # Use extracted components
        if existing:
            self.tokens = existing.tokens
            self.title_text = existing.title
            self.cloze_id = existing.id
        else:
            self.tokens = tokenize(text_source.text)
            self.title_text = ""
            self.cloze_id = generate_id("cloze")

        self.navigator = WordNavigator(self.tokens)
        self.masking = MaskingController()

        # UI setup (existing code)
        ...

    # Methods now delegate to navigator and masking controller
    def _toggle_mask(self) -> None:
        token = self.navigator.current_token()
        self.masking.toggle_mask(token)
        self.app.application.invalidate()
```

**Result**: 209 lines → ~130 lines (with extractors)
**Benefit**: Navigation and masking logic can be tested independently

---

### Phase 4: Split Main File into Module Structure

**Goal**: Create a package structure that's easier to navigate

```
exercices/francais_cloze_dictations/
├── __init__.py                  # Public API (run())
├── models.py                    # Data models (Token, TextSource, Cloze)
├── persistence.py               # File I/O (load/save functions)
├── text_processing.py           # Tokenization, rendering
├── clipboard.py                 # Clipboard operations
├── app.py                       # ClozeApp (main controller)
├── screens/
│   ├── __init__.py
│   ├── base.py                  # Screen base class
│   ├── menu.py                  # Menu screens
│   ├── text_source.py           # TextSource screens
│   ├── cloze_editor.py          # ClozeEditorScreen + helpers
│   └── student_practice.py      # StudentPracticeScreen + helpers
└── widgets.py                   # ActionRadioList, TextInputPlaceholder
```

**File size targets**:
- Each file: 100-300 lines
- No file over 400 lines
- Clear single responsibility per file

---

## Refactoring Principles

### 1. Maintain Overall Complexity

**Important**: We're not reducing complexity, we're organizing it better.

- **Before**: 1,594 lines in one file
- **After**: ~1,800 lines across 12 files (slightly more due to imports/docstrings)

The total complexity stays the same, but:
- Each piece is easier to understand in isolation
- Related functionality is grouped together
- Dependencies are explicit through imports

### 2. Preserve Behavior

**Critical**: All refactoring must be behavior-preserving.

- Tests should pass unchanged (we don't touch tests)
- UI behavior stays identical
- File formats remain compatible
- No feature additions or removals

### 3. Incremental Refactoring

**Strategy**: Small, safe steps with validation

1. Extract a single class/function
2. Update imports in main file
3. Run tests (if any)
4. Verify app still works
5. Commit
6. Repeat

### 4. Keep Public API Stable

**Main file should still work as entry point**:

```python
# exercices/francais_cloze_dictations/__init__.py
from .app import run

DISPLAY_NAME = "Français : Dictées à trous (Cloze)"

# Maintain backward compatibility
def main(argv=None):
    return run(argv)
```

---

## Implementation Order

### Step 1: Create Package Structure (Low Risk)

1. Create `exercices/francais_cloze_dictations/` directory
2. Move current file to `francais_cloze_dictations_backup.py`
3. Create empty `__init__.py` with imports from backup
4. Verify app still launches

### Step 2: Extract Pure Data (No Dependencies)

1. Create `models.py` with dataclasses
2. Create `persistence.py` with load/save functions
3. Update imports in main file
4. Test

### Step 3: Extract Pure Functions (No State)

1. Create `text_processing.py`
2. Create `clipboard.py`
3. Update imports
4. Test

### Step 4: Extract Helper Classes (Stateless)

1. Create `widgets.py` (ActionRadioList, TextInputPlaceholder)
2. Update imports
3. Test

### Step 5: Refactor StudentPracticeScreen (Complex)

1. Create `StudentPracticeState` in new file
2. Create `StudentPracticeAutosave` in same file
3. Refactor `StudentPracticeScreen` to use them
4. Extract handler methods
5. Test thoroughly

### Step 6: Refactor ClozeEditorScreen (Complex)

1. Create `WordNavigator`
2. Create `MaskingController`
3. Refactor `ClozeEditorScreen` to use them
4. Test

### Step 7: Organize Screens (Structural)

1. Create `screens/` directory
2. Move screen classes to appropriate files
3. Update imports
4. Test

### Step 8: Final Cleanup

1. Remove `francais_cloze_dictations_backup.py`
2. Update documentation
3. Final testing

---

## Success Criteria

### Quantitative Metrics

- ✓ No file over 400 lines
- ✓ Average file size: 150-250 lines
- ✓ Each class has single clear responsibility
- ✓ No method over 50 lines
- ✓ Cyclomatic complexity < 10 per function

### Qualitative Metrics

- ✓ A new developer can understand each file in 5 minutes
- ✓ Each file can be explained in one sentence
- ✓ Dependencies are clear and one-directional
- ✓ Testing individual components is straightforward
- ✓ Adding new screen types requires minimal changes

### Functional Requirements

- ✓ All existing features work identically
- ✓ Performance is unchanged
- ✓ File formats remain compatible
- ✓ Entry point works the same way
- ✓ Import paths maintain backward compatibility

---

## Risk Assessment

### Low Risk
- Extracting dataclasses
- Extracting pure functions
- Creating new files without changing old code

### Medium Risk
- Refactoring class methods
- Changing initialization order
- Splitting interdependent classes

### High Risk
- Changing autosave format or behavior
- Modifying prompt_toolkit integration
- Altering key binding registration

### Mitigation Strategies

1. **Version control**: Commit after each successful extraction
2. **Testing**: Manual testing after each step
3. **Backup**: Keep original file until all tests pass
4. **Rollback plan**: Each commit is a safe rollback point

---

## Timeline Estimate

Not providing time estimates per requirements, but the implementation order above represents:

- 8 major steps
- Each step is independently testable
- Each step can be completed in isolation
- Steps 1-4 are straightforward extractions
- Steps 5-6 require careful refactoring
- Steps 7-8 are organizational

---

## Additional Opportunities (Future Consideration)

### Quiz Sequencer Pattern (Separate Effort)

As noted in the analysis, **20 quiz files** share a common pattern:

```python
show_lesson()
for question in QUESTIONS:
    display_question()
    answer = get_answer()
    if correct: score += 1
print_score()
```

This could be extracted into a `QuizSequencer` base class, but it's **independent from this refactoring** and should be a separate effort.

### Unit Testing

After refactoring, the extracted classes become much easier to test:

- `StudentPracticeState`: Test state transitions
- `StudentPracticeAutosave`: Test save/load with mock files
- `WordNavigator`: Test cursor movement
- `MaskingController`: Test masking logic

These tests would provide confidence for future changes.

---

## Conclusion

This refactoring plan focuses on the **ClozeApp "sequencer" architecture** in `francais_cloze_dictations.py`. By extracting cohesive components into separate files and classes, we can make the codebase significantly more comprehensible without changing its behavior.

The key insight is that **sequencing logic** (ClozeApp navigation, StudentPracticeScreen workflow) should be clearly separated from **state management** (answers, cursor position), **persistence** (autosave), and **rendering** (formatted text).

This separation makes each piece understandable in isolation while maintaining the same overall complexity and functionality.
