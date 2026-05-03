# CLAUDE.md — exercices_ecole

## Running the program

```bash
python -m exercices
```

Two-level menu: category → exercise. Each exercise module exposes `main()` and `DISPLAY_NAME`.

## Adding a new exercise

1. Create `exercices/my_module.py` with `DISPLAY_NAME = "..."` and `def main() -> None`.
2. Import it in `exercices/__main__.py` and add it to the relevant category in `CATEGORIES`.

---

## Architecture

### Module layout

```
exercices/
  __main__.py          — two-level menu, CATEGORIES list
  math_display_utils.py — ANSI color constants + digit-cell rendering (shared)
  math_eucl_div.py     — euclidean division (most complex module)
  math_multiplication_1chiffre.py — column multiplication, called by eucl_div
  utils.py, logger.py  — generic helpers
  anglais_*.py, francais_*.py, geometrie_*.py, ... — lesson + quiz modules
```

### Typical exercise structure

Most modules: present a lesson, then a quiz loop. Simple `input()` / `print()` — no curses except `musique_notes_portee.py`.

---

## math_display_utils — color constants

```python
GREEN, YELLOW, CYAN, RED, MAGENTA, BOLD, RESET   # ANSI codes
DIM = "\033[2m"                                    # defined locally in math_eucl_div
```

`clear_screen()` — `os.system("clear")` on Linux.

---

## math_multiplication_1chiffre — column multiplication

### Public API used by eucl_div

```python
run_multiplication_interactive(a: int, b: int) -> bool
```

Returns `True` on completion, `False` if the student cancels (types `x`, `annuler`, or `stop`).

### Cancellation pattern

```python
class _Cancelled(Exception): ...
_CANCEL_WORDS = frozenset(("x", "annuler", "stop"))

def _inp(prompt: str) -> str:
    raw = input(prompt).strip()
    if raw.lower() in _CANCEL_WORDS:
        raise _Cancelled
    return raw
```

All `input()` calls inside the exercise use `_inp()`. The whole `run_multiplication_interactive` body is wrapped in `try / except _Cancelled → return False`.

### Three tiers

1. `b == 0` → trivial message, return True  
2. `len(str(a)) == 1` → simple single-digit ask, no layout  
3. Multi-digit `a` → full column layout with retenue

---

## math_eucl_div — euclidean division

### Slot system (3 visible chars per digit)

```python
_B = "   "                      # blank slot

def _s(ch: str, color: str = "") -> str:
    if color:
        return f"{color}{BOLD}{ch}{RESET}  "
    return f"{ch}  "

_M = MAGENTA + BOLD             # divisor color — use as f"{_M}{divisor}{RESET}"
```

`_place(number, end_col, nd, color)` — right-aligns `number` into `nd` slots ending at column `end_col`.  
`_sep_str(end_col, n_wide, nd)` — horizontal separator line.  
`_dim_slot(slot)` — strips ANSI codes from a slot and re-wraps in `DIM`.

### Data model

```python
@dataclass
class _Step:
    end_col: int           # last dividend column consumed (0-based)
    partial_dividend: int  # e.g. 73
    quotient_digit: int    # 0–9
    product: int           # quotient_digit × divisor
    remainder: int         # partial_dividend − product
```

`_precompute(dividend_str, divisor) -> list[_Step]` — builds all steps upfront.

### Canvas state (lives in `run_division_interactive`)

```python
q_digits:   list[str | None]        # revealed quotient digits (per step)
products:   list[list[str] | None]  # product slot-lists (per step)
seps_shown: list[bool]              # whether separator is drawn (per step)
remainders: list[list[str] | None]  # remainder/descent slot-lists (per step)
```

### `rc(**kw)` closure pattern

Defined inside the `for i, step in enumerate(steps)` loop:

```python
def rc(**kw):
    _render_canvas(
        dividend_str, divisor_str, steps,
        **{"q_digits": q_digits, "products": products,
           "seps_shown": seps_shown, "remainders": remainders,
           **kw},   # caller kwargs override defaults
    )
```

Pass only what differs: `rc(focus_col_range=focus)`, `rc(q_digits=q_tmp, focus_col_range=focus)`, etc.

### `_render_canvas` key parameters

| Parameter | Purpose |
|---|---|
| `focus_col_range` | Dim dividend digits outside `(start, end)` |
| `highlight_dividend_col` | CYAN — used for descent animation |
| `active_sub_col` | CYAN dividend digit, RED product digit during subtraction |
| `borrow_cols` | List of columns where CYAN carry "1" markers are shown |
| `active_step` | Which step's product/carry/result rows are "live" |
| `active_rem` | Partial result being built during subtraction |
| `subtraction_mode` | Dims everything except active subtraction rows |

### Interactive flow per step

**Phase 0** (step 0 only): scan dividend left-to-right, explaining why each digit alone is too small.  
**Phase A**: `_find_quotient_digit(partial, divisor)` — trial-and-error with multiplication.  
**Phase C**: blink quotient digit into canvas; reveal product row.  
**Phase D**: `_do_subtraction(...)` — digit-by-digit subtraction (Austrian method, see below).  
**Phase E**: descent animation — highlight next dividend digit, land it in the remainder row.

### Subtraction: Austrian (compensation) method

**Rule**: borrows add +1 to the *subtrahend* of the next column — the minuend digit never changes.

```
  1 2 3        units:  3 − 9  → can't → 13 − 9  = 4  (carry +1 to tens' subtrahend)
−   9 9        tens:   2 − 10 → can't → 12 − 10 = 2  (carry +1 to hundreds' subtrahend)
-------        hundreds: 1 − 1 = 0
    0 2 4
```

`borrow_cols` accumulates permanently — once a carry "1" is placed, it stays visible in the carry row throughout the subtraction (below the product row, above the separator).

### Presentation flow inside `_do_subtraction`

Per column, separated into two phases so retries skip re-explanation:

1. **Presentation** (once):
   - Draw canvas
   - If incoming carry: print "Retenue: j'ajoute 1 au X, donc je dois soustraire Y"
   - If borrow needed: print "A − B : on ne peut pas ! J'emprunte pour transformer le A en A+10" → Enter → update `borrow_cols`, redraw → Enter
   - If carry but no borrow: Enter (pause after retenue explanation)

2. **Answer loop** (retries here):
   - Draw canvas → print question → get answer
   - Wrong: "Non — X − Y = Z" → Enter → back to top of loop

### `_find_quotient_digit` — quotient digit helper

Trial-and-error screen. Student guesses a digit 0–9:
- Already-tried wrong digits are blocked
- `n == 0` or `n == 1`: trivial inline message (no multiplication launched)
- `n >= 2`: calls `run_multiplication_interactive(divisor, n)` — cancellable with `x`
- Verdict: **trop grand** (RED), **pas assez** (YELLOW, shows `n+1` in CYAN without parens), or correct (GREEN with full explanation)

---

## Colour conventions (eucl_div)

| Color | Meaning |
|---|---|
| `MAGENTA + BOLD` (`_M`) | Divisor — every occurrence |
| `CYAN` | Current focus digit, carry "1" markers, partial dividend label |
| `RED` | Active subtrahend digit (product at `active_sub_col`), wrong answers |
| `GREEN` | Correct answers, revealed quotient/result digits |
| `YELLOW` | Product slots (revealed, not yet being subtracted) |
| `DIM` | Out-of-focus digits, all non-active rows in `subtraction_mode` |
