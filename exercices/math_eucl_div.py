"""Maths : Division euclidienne guidée."""
from __future__ import annotations

DISPLAY_NAME = "Maths : Division euclidienne"

import re
import time
from dataclasses import dataclass

from .math_display_utils import GREEN, YELLOW, CYAN, RED, MAGENTA, BOLD, RESET, clear_screen

# Consistent colour for the divisor throughout the whole exercise
_M = MAGENTA + BOLD   # "divisor colour" — apply as f"{_M}{divisor}{RESET}"
from .math_multiplication_1chiffre import run_multiplication_interactive


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class _Step:
    end_col: int           # last dividend column consumed (0-based)
    partial_dividend: int  # e.g. 73
    quotient_digit: int    # 0–9
    product: int           # quotient_digit × divisor
    remainder: int         # partial_dividend − product


def _precompute(dividend_str: str, divisor: int) -> list[_Step]:
    steps: list[_Step] = []
    current = 0
    n = len(dividend_str)
    for i, ch in enumerate(dividend_str):
        current = current * 10 + int(ch)
        if current < divisor and not steps:
            continue
        q = current // divisor
        prod = q * divisor
        rem = current - prod
        steps.append(_Step(i, current, q, prod, rem))
        current = rem
    if not steps:
        # whole dividend smaller than divisor
        steps.append(_Step(n - 1, int(dividend_str), 0, 0, int(dividend_str)))
    return steps


# ---------------------------------------------------------------------------
# Slot helpers — each digit slot is 3 visible chars: "d  " or "   "
# ---------------------------------------------------------------------------

_B = "   "  # blank slot
DIM = "\033[2m"  # ANSI dim — used for out-of-focus digits

_ANSI_ESC = re.compile(r"\033\[[0-9;]*m")


def _dim_slot(slot: str) -> str:
    """Return slot rendered in DIM, or blank if already blank."""
    if slot == _B:
        return _B
    ch = _ANSI_ESC.sub("", slot).strip()
    return f"{DIM}{ch}{RESET}  " if ch else _B


def _s(ch: str, color: str = "") -> str:
    if color:
        return f"{color}{BOLD}{ch}{RESET}  "
    return f"{ch}  "


def _place(number: int, end_col: int, nd: int, color: str = "") -> list[str]:
    """Return nd slots with `number` right-aligned to end_col."""
    slots = [_B] * nd
    s = str(number)
    for i, d in enumerate(s):
        c = end_col - len(s) + 1 + i
        if 0 <= c < nd:
            slots[c] = _s(d, color)
    return slots


def _sep_str(end_col: int, n_wide: int, nd: int) -> str:
    """Separator line (─── per slot) spanning n_wide slots ending at end_col."""
    start = end_col - n_wide + 1
    return "  " + "".join("───" if start <= c <= end_col else "   " for c in range(nd))


# ---------------------------------------------------------------------------
# Canvas rendering
# ---------------------------------------------------------------------------

def _render_canvas(
    dividend_str: str,
    divisor_str: str,
    steps: list[_Step],
    *,
    q_digits: list[str | None],           # per step: char or None (hidden)
    products: list[list[str] | None],      # per step: slots or None (hidden)
    seps_shown: list[bool],
    remainders: list[list[str] | None],    # per step: slots or None (hidden)
    active_step: int = -1,
    active_rem: list[str] | None = None,   # partial subtraction result being built
    highlight_dividend_col: int | None = None,  # highlight this dividend digit (descent)
    borrow_cols: list[int] | None = None,  # columns where carry "1" markers are shown
    active_sub_col: int | None = None,     # column being actively subtracted (dividend=CYAN, product=RED)
    focus_col_range: tuple[int, int] | None = None,  # dim dividend digits outside this range
    subtraction_mode: bool = False,        # dim everything except the active subtraction
) -> None:
    nd = len(dividend_str)
    ns = len(divisor_str)
    nsteps = len(steps)
    rw = max(ns, nsteps)  # right-section width in slots

    sm = subtraction_mode  # shorthand
    BAR = f" {DIM}│{RESET} " if sm else f" {BOLD}│{RESET} "

    def left(prefix: str, slots: list[str]) -> str:
        return prefix + "".join(slots)

    def right_slots(s: str, color: str = "") -> str:
        sl = [_B] * rw
        for i, d in enumerate(s):
            col = rw - len(s) + i
            sl[col] = _s(d, color)
        return "".join(sl)

    clear_screen()

    # ── Label row ──────────────────────────────────────────────────────────
    lc = DIM if sm else CYAN
    left_w = 2 + nd * 3
    print(
        f"  {lc}dividende{RESET}"
        + " " * max(0, left_w - 11)
        + "    "
        + f"{lc}diviseur{RESET}"
    )

    # ── Dividend │ Divisor ─────────────────────────────────────────────────
    div_slots = []
    for j, d in enumerate(dividend_str):
        if sm:
            color = CYAN if j == active_sub_col else DIM
        elif highlight_dividend_col == j:
            color = CYAN
        elif active_sub_col == j:
            color = CYAN
        elif focus_col_range is not None and not (focus_col_range[0] <= j <= focus_col_range[1]):
            color = DIM
        else:
            color = BOLD
        div_slots.append(_s(d, color))
    divisor_color = DIM if sm else MAGENTA
    print(left("  ", div_slots) + BAR + right_slots(divisor_str, divisor_color))

    # ── Blank │ separator under divisor ───────────────────────────────────
    corner = f" {DIM}├{RESET} " if sm else f" {BOLD}├{RESET} "
    horiz = f"{DIM}{'─' * (rw * 3)}{RESET}" if sm else "─" * (rw * 3)
    print(left("  ", [_B] * nd) + corner + horiz)

    # ── Blank │ quotient ──────────────────────────────────────────────────
    q_sl = [_B] * rw
    any_q = False
    for i, qd in enumerate(q_digits):
        if qd is not None:
            col = rw - nsteps + i
            q_sl[col] = _s(qd, DIM if sm else GREEN)
            any_q = True
    if any_q:
        q_label = f"  {DIM}quotient{RESET}" if sm else f"  {CYAN}quotient{RESET}"
    else:
        q_label = ""
    print(left("  ", [_B] * nd) + BAR + "".join(q_sl) + q_label)

    # ── Steps ──────────────────────────────────────────────────────────────
    for i, step in enumerate(steps):
        if step.quotient_digit == 0:
            # Dividend < divisor: no subtraction row, just show remainder/reste
            if i == nsteps - 1:
                r_slots = remainders[i] if remainders[i] is not None else [_B] * nd
                if sm:
                    r_slots = [_dim_slot(s) for s in r_slots]
                reste_label = f"  {CYAN}reste{RESET}" if remainders[i] is not None else ""
                print(left("  ", r_slots) + reste_label)
            continue

        # Non-active steps: dim everything during subtraction
        if sm and i != active_step:
            if products[i] is not None:
                print(f"{DIM}─ {RESET}" + "".join(_dim_slot(s) for s in products[i]))
            else:
                print(left("  ", [_B] * nd))
            if seps_shown[i]:
                n_wide = max(len(str(step.product)), len(str(step.partial_dividend)))
                print(f"{DIM}{_sep_str(step.end_col, n_wide, nd)}{RESET}")
            else:
                print(left("  ", [_B] * nd))
            r_src = remainders[i] if remainders[i] is not None else [_B] * nd
            print(left("  ", [_dim_slot(s) for s in r_src]))
            continue

        # Product row: "─ " prefix
        if products[i] is not None:
            if i == active_step and active_sub_col is not None:
                # Color active product digit RED, dim the others
                prod_s = str(step.product)
                prod_start = step.end_col - len(prod_s) + 1
                p_slots = [_B] * nd
                for c in range(prod_start, step.end_col + 1):
                    pd = prod_s[c - prod_start]
                    p_slots[c] = _s(pd, RED if c == active_sub_col else DIM)
                print(left("─ ", p_slots))
            else:
                print(left("─ ", products[i]))
        else:
            print(left("  ", [_B] * nd))

        # Carry row: CYAN "1" at each column where a carry has been placed
        if i == active_step and borrow_cols:
            carry_slots = [_B] * nd
            for bc in borrow_cols:
                if 0 <= bc < nd:
                    carry_slots[bc] = _s("1", CYAN)
            print(left("  ", carry_slots))

        # Separator row
        if seps_shown[i]:
            n_wide = max(len(str(step.product)), len(str(step.partial_dividend)))
            print(_sep_str(step.end_col, n_wide, nd))
        else:
            print(left("  ", [_B] * nd))

        # Remainder/result row
        if i == active_step and active_rem is not None:
            r_slots = active_rem
        elif remainders[i] is not None:
            r_slots = remainders[i]
        else:
            r_slots = [_B] * nd

        if i == nsteps - 1:
            reste_label = f"  {CYAN}reste{RESET}" if remainders[i] is not None else ""
            print(left("  ", r_slots) + reste_label)
        else:
            print(left("  ", r_slots))


# ---------------------------------------------------------------------------
# Phase A: find the quotient digit (trial-and-error with multiplication)
# ---------------------------------------------------------------------------

def _find_quotient_digit(partial: int, divisor: int) -> int:
    """Guide student to the quotient digit through guessing + multiplication.

    Returns the confirmed quotient digit. The product (digit × divisor) has
    already been computed interactively, so Phase B multiplication is skipped.
    """
    partial_s = str(partial)
    divisor_s = str(divisor)

    # Persistent hint: compare leading digits to estimate
    d0 = int(divisor_s[0])
    p0 = int(partial_s[0])
    hint_partial = int(partial_s[:2]) if (p0 < d0 and len(partial_s) > 1) else p0
    # Only show the hint when it offers a simpler sub-problem than the full question
    if hint_partial != partial or d0 != divisor:
        hint_line = (
            f"  {CYAN}Astuce :{RESET} commence par combien de fois "
            f"{_M}{d0}{RESET} entre dans {BOLD}{hint_partial}{RESET} "
            f"— ça donne une bonne estimation."
        )
    else:
        hint_line = ""

    history: list[tuple[int, int, str]] = []  # (n, product, verdict)
    tried: set[int] = set()

    while True:
        clear_screen()
        # ── Goal — always visible ────────────────────────────────────────
        print(f"\n  {BOLD}Combien de fois {_M}{divisor}{RESET} entre dans {partial} ?{RESET}")
        print(f"  (On cherche le plus grand chiffre N tel que N × {_M}{divisor}{RESET} ≤ {partial})\n")
        print(hint_line + "\n")

        # ── History of previous attempts ─────────────────────────────────
        if history:
            print(f"  Tes essais jusqu'ici :")
            for hn, hprod, verdict in history:
                if verdict == "trop_grand":
                    print(f"    {RED}{hn} × {_M}{divisor}{RESET}{RED} = {hprod} > {partial}  → trop grand{RESET}")
                else:
                    hprod1 = (hn + 1) * divisor
                    print(f"    {YELLOW}{hn} × {_M}{divisor}{RESET}{YELLOW} = {hprod} ≤ {partial},  "
                          f"mais {CYAN}{BOLD}{hn+1}{RESET}{YELLOW} × {_M}{divisor}{RESET}{YELLOW}"
                          f" = {hprod1} ≤ {partial}  → pas assez{RESET}")
            print()

        raw = input(f"  Essaie : {_M}{divisor}{RESET} × ___ ?   Chiffre (0-9) : ").strip()
        if not raw.isdigit() or len(raw) != 1:
            continue

        n = int(raw)

        # Block already-tried wrong answers
        if n in tried:
            print(f"\n  {RED}Tu as déjà essayé {n} — ça ne marche pas, choisis un autre chiffre.{RESET}")
            input("  Entrée pour continuer...")
            continue

        prod = n * divisor

        # Compute n × divisor interactively (trivial cases shown inline)
        if n == 0:
            clear_screen()
            print(f"\n  {_M}{divisor}{RESET} × 0 = 0  (tout nombre multiplié par 0 vaut 0)\n")
            input("  Entrée pour continuer...")
            completed = True
        elif n == 1:
            clear_screen()
            print(f"\n  {_M}{divisor}{RESET} × 1 = {_M}{divisor}{RESET}  (tout nombre multiplié par 1 vaut lui-même)\n")
            input("  Entrée pour continuer...")
            completed = True
        else:
            clear_screen()
            print(f"\n  Calculons {n} × {_M}{divisor}{RESET}...\n")
            input("  Entrée pour lancer la multiplication...")
            completed = run_multiplication_interactive(divisor, n)

        # If multiplication was cancelled, go back to the prompt without recording
        if not completed:
            continue

        # Verdict
        prod1 = (n + 1) * divisor
        clear_screen()
        print(f"\n  {BOLD}Résultat : {n} × {_M}{divisor}{RESET} = {prod}{RESET}")
        if prod > partial:
            print(f"  {RED}{prod} > {partial}  → trop grand, essaie quelque chose de plus petit !{RESET}")
            tried.add(n)
            history.append((n, prod, "trop_grand"))
            input("  Entrée pour réessayer...")
        elif prod1 <= partial:
            print(f"  {YELLOW}{prod} ≤ {partial}, mais {CYAN}{BOLD}{n+1}{RESET}{YELLOW} × {_M}{divisor}{RESET}{YELLOW} = {prod1} ≤ {partial} aussi.{RESET}")
            print(f"  {YELLOW}Tu peux faire mieux !{RESET}")
            tried.add(n)
            history.append((n, prod, "pas_assez"))
            input("  Entrée pour réessayer...")
        else:
            print(f"\n  {GREEN}✓  {n} × {_M}{divisor}{RESET}{GREEN} = {prod},  et {prod} ≤ {partial}{RESET}")
            print(f"     → {_M}{divisor}{RESET} rentre bien {n} fois dans {partial}.\n")
            print(f"  {GREEN}✓  {CYAN}{BOLD}{n+1}{RESET}{GREEN} × {_M}{divisor}{RESET}{GREEN} = {prod1},  et {prod1} > {partial}{RESET}")
            print(f"     → {_M}{divisor}{RESET} ne rentre PAS {CYAN}{BOLD}{n+1}{RESET} fois dans {partial}.\n")
            print(f"  {GREEN}{BOLD}Donc le chiffre du quotient est {n} :{RESET}")
            print(f"  {GREEN}c'est le plus grand chiffre pour lequel {_M}{divisor}{RESET}{GREEN} × {n} tient encore dans {partial}.{RESET}\n")
            input("  Entrée pour continuer...")
            return n


# ---------------------------------------------------------------------------
# Phase D: subtraction with borrow, inline in canvas
# ---------------------------------------------------------------------------

def _do_subtraction(
    dividend_str: str,
    divisor_str: str,
    steps: list[_Step],
    step_idx: int,
    *,
    q_digits: list[str | None],
    products: list[list[str] | None],
    seps_shown: list[bool],
    remainders: list[list[str] | None],
    focus_col_range: tuple[int, int] | None = None,
) -> list[str]:
    """Guide the student through partial_dividend − product digit by digit.
    Returns the fully-revealed result slots list (nd entries)."""
    step = steps[step_idx]
    nd = len(dividend_str)
    partial = step.partial_dividend
    product = step.product
    end_col = step.end_col

    partial_s = str(partial)
    product_s = str(product)
    # Pad product to same length as partial
    n_digits = max(len(partial_s), len(product_s))
    partial_s = partial_s.zfill(n_digits)
    product_s = product_s.zfill(n_digits)

    result_slots: list[str] = [_B] * nd
    carry = 0           # Austrian method: carry adds +1 to subtrahend of next column
    borrow_cols: list[int] = []   # columns where carry "1" markers persist in display

    for pos in range(n_digits - 1, -1, -1):
        col = end_col - (n_digits - 1 - pos)
        top_d = int(partial_s[pos])    # minuend digit (never modified in Austrian method)
        bot_d = int(product_s[pos])    # subtrahend digit before carry
        effective_bot = bot_d + carry  # actual value to subtract

        seps_shown[step_idx] = True

        def _draw(_col=col):
            _render_canvas(
                dividend_str, divisor_str, steps,
                q_digits=q_digits,
                products=products,
                seps_shown=seps_shown,
                remainders=remainders,
                active_step=step_idx,
                active_rem=result_slots,
                borrow_cols=borrow_cols,
                active_sub_col=_col,
                focus_col_range=focus_col_range,
                subtraction_mode=True,
            )

        # Pre-compute this column's arithmetic
        if top_d < effective_bot:
            borrowed_top = top_d + 10
            next_carry = 1
            expected = borrowed_top - effective_bot
            needs_borrow = True
        else:
            borrowed_top = 0  # unused
            next_carry = 0
            expected = top_d - effective_bot
            needs_borrow = False

        # --- Presentation phase (runs once per column) ---
        _draw()

        if carry > 0:
            print(f"\n  {CYAN}Retenue :{RESET} j'ajoute 1 au {RED}{BOLD}{bot_d}{RESET}"
                  f", donc je dois soustraire {RED}{BOLD}{effective_bot}{RESET}")

        if needs_borrow:
            print(f"  {BOLD}{top_d} − {RED}{BOLD}{effective_bot}{RESET}"
                  f" : on ne peut pas ! J'emprunte pour transformer le"
                  f" {CYAN}{BOLD}{top_d}{RESET} en {CYAN}{BOLD}{borrowed_top}{RESET}")
            input("  Entrée pour continuer...")
            if col > 0:
                borrow_cols.append(col - 1)
            _draw()
            input("  Entrée pour continuer...")
        elif carry > 0:
            input("  Entrée pour continuer...")

        # --- Answer phase (retries loop here) ---
        while True:
            _draw()
            if needs_borrow:
                print(f"  {CYAN}{BOLD}{borrowed_top}{RESET} − {RED}{BOLD}{effective_bot}{RESET} = ?")
            else:
                print(f"  {BOLD}{top_d} − {RED}{BOLD}{effective_bot}{RESET} = ?")

            raw = input("  > ").strip()
            if raw.lstrip("-").isdigit() and int(raw) == expected:
                result_slots[col] = _s(str(expected), GREEN)
                carry = next_carry
                break
            else:
                prompt_top = borrowed_top if needs_borrow else top_d
                print(f"  {RED}Non — {prompt_top} − {effective_bot} = {expected}{RESET}")
                input("  Entrée pour réessayer...")

        _draw()
        print(f"  {GREEN}Correct !{RESET}")
        input("  Entrée pour continuer...")

    return result_slots


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

def run_division_interactive(dividend: int, divisor: int) -> None:
    dividend_str = str(dividend)
    divisor_str = str(divisor)
    nd = len(dividend_str)
    steps = _precompute(dividend_str, divisor)
    nsteps = len(steps)

    # Canvas state (all hidden initially)
    q_digits: list[str | None] = [None] * nsteps
    products: list[list[str] | None] = [None] * nsteps
    seps_shown: list[bool] = [False] * nsteps
    remainders: list[list[str] | None] = [None] * nsteps

    # Initial display
    _render_canvas(
        dividend_str, divisor_str, steps,
        q_digits=q_digits, products=products,
        seps_shown=seps_shown, remainders=remainders,
    )
    print(f"\n  {BOLD}Division euclidienne : {dividend} ÷ {_M}{divisor}{RESET}")
    input("  Entrée pour commencer...")

    for i, step in enumerate(steps):
        partial = step.partial_dividend
        q = step.quotient_digit
        partial_len = len(str(partial))
        focus_start = max(0, step.end_col - partial_len + 1)
        focus = (focus_start, step.end_col)

        def rc(**kw):
            """Redraw with current canvas state; caller kwargs override defaults."""
            _render_canvas(
                dividend_str, divisor_str, steps,
                **{
                    "q_digits": q_digits,
                    "products": products,
                    "seps_shown": seps_shown,
                    "remainders": remainders,
                    **kw,
                },
            )

        # ── Phase 0: build up the partial dividend, digit by digit ────────
        if i == 0:
            # Scan from left until the partial dividend is large enough
            current = 0
            for j in range(step.end_col + 1):
                current = current * 10 + int(dividend_str[j])
                rc(focus_col_range=(0, j))
                if current < divisor:
                    print(f"\n  {_M}{divisor}{RESET} dans {BOLD}{current}{RESET} ?"
                          f"  Non — {current} est plus petit que {_M}{divisor}{RESET}.")
                    if j < step.end_col:
                        print(f"  On prend le chiffre suivant...")
                        input("  Entrée pour continuer...")
                else:
                    print(f"\n  {_M}{divisor}{RESET} dans {BOLD}{current}{RESET} ?"
                          f"  Oui — {current} est assez grand.")
                    print(f"  {CYAN}C'est notre dividende partiel.{RESET}"
                          f"  Les autres chiffres du dividende attendent leur tour.")
                    input("  Entrée pour continuer...")
        else:
            # Subsequent steps: partial already shown via descent
            rc(focus_col_range=focus)
            print(f"\n  On travaille maintenant avec {BOLD}{partial}{RESET}"
                  f" — les autres chiffres sont mis de côté pour l'instant.")
            input("  Entrée pour continuer...")

        # ── Phase A: find quotient digit ──────────────────────────────────
        if q == 0:
            rc(focus_col_range=focus)
            print(f"\n  {_M}{divisor}{RESET} ne rentre pas dans {partial}.")
            print(f"  Le quotient est {BOLD}0{RESET} et le reste est {BOLD}{partial}{RESET}.")
            q_digits[i] = "0"
            remainders[i] = _place(step.remainder, step.end_col, nd, YELLOW)
            rc()
            input("  Entrée pour continuer...")
            continue

        found_q = _find_quotient_digit(partial, divisor)

        # ── Phase C: pose quotient digit with blink, then show product ────
        # Blink the quotient digit into place
        q_tmp = list(q_digits)
        for frame in [False, True, False, True, True]:
            q_tmp[i] = str(found_q) if frame else None
            rc(q_digits=q_tmp, focus_col_range=focus)
            time.sleep(0.35)
        q_digits[i] = str(found_q)

        # Show where the product lands, with focus highlighting
        products[i] = _place(step.product, step.end_col, nd, YELLOW)
        rc(focus_col_range=focus)
        print(f"\n  On pose {BOLD}{found_q}{RESET} au quotient.")
        print(f"  Le résultat {BOLD}{found_q} × {_M}{divisor}{RESET} = {step.product}"
              f" se place sous les chiffres {BOLD}{partial}{RESET} qu'on regardait.")
        print(f"  {CYAN}(Les autres chiffres du dividende sont grisés — on les ignore pour l'instant.){RESET}")
        input("  Entrée pour continuer...")

        # ── Phase D: subtraction with focus ───────────────────────────────
        seps_shown[i] = True
        result_slots = _do_subtraction(
            dividend_str, divisor_str, steps, i,
            q_digits=q_digits,
            products=products,
            seps_shown=seps_shown,
            remainders=remainders,
            focus_col_range=focus,
        )

        # ── Phase E: descent with highlight ───────────────────────────────
        if i < nsteps - 1:
            next_col = step.end_col + 1
            next_digit = dividend_str[next_col]

            # Highlight the digit about to descend in the dividend
            rc(highlight_dividend_col=next_col, focus_col_range=focus)
            print(f"\n  Ce chiffre {CYAN}{BOLD}{next_digit}{RESET} va descendre ↓")
            time.sleep(1.5)

            # Land it in the remainder row, shift focus to the new range
            remainder_slots = list(result_slots)
            remainder_slots[next_col] = _s(next_digit, CYAN)
            remainders[i] = remainder_slots
            new_focus = (focus_start if step.remainder == 0 else focus[0],
                         next_col)
            rc(focus_col_range=new_focus)
            print(f"\n  {CYAN}{BOLD}On descend le {next_digit} !{RESET}")
            print(f"  On travaille maintenant avec : {BOLD}{step.remainder}{next_digit}{RESET}")
            input("  Entrée pour continuer...")
        else:
            remainders[i] = result_slots
            rc()
            print(f"\n  Reste : {BOLD}{step.remainder}{RESET}")
            input("  Entrée pour continuer...")

    # ── Final verification ────────────────────────────────────────────────
    quotient, remainder = divmod(dividend, divisor)
    rc()
    print()

    while True:
        raw = input(f"  Quel est le quotient de {dividend} ÷ {_M}{divisor}{RESET} ? ").strip()
        if raw.lstrip("-").isdigit() and int(raw) == quotient:
            print(f"  {GREEN}Exact !{RESET}")
            break
        print(f"  {RED}Non, réessaie.{RESET}")

    while True:
        raw = input(f"  Quel est le reste ? ").strip()
        if raw.lstrip("-").isdigit() and int(raw) == remainder:
            print(f"  {GREEN}Bravo !{RESET}")
            break
        print(f"  {RED}Non, réessaie.{RESET}")

    print(f"\n  {GREEN}{BOLD}{dividend} = {_M}{divisor}{RESET}{GREEN}{BOLD} × {quotient} + {remainder}{RESET}\n")
    input("  Entrée pour terminer...")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"\n{BOLD}=== Division euclidienne ==={RESET}\n")
    while True:
        raw = input("Dividende (entier positif) : ").strip()
        if raw.isdigit() and int(raw) > 0:
            dividend = int(raw)
            break
        print(f"{RED}Entre un entier positif.{RESET}")
    while True:
        raw = input("Diviseur (entier ≥ 2) : ").strip()
        if raw.isdigit() and int(raw) >= 2:
            divisor = int(raw)
            break
        print(f"{RED}Entre un entier supérieur ou égal à 2.{RESET}")
    run_division_interactive(dividend, divisor)


if __name__ == "__main__":
    main()
