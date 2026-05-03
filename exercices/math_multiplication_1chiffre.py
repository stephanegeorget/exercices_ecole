"""Maths : Multiplication guidée d'un nombre par un seul chiffre."""

from __future__ import annotations

DISPLAY_NAME = "Maths : Multiplication par un chiffre"

import time

from .math_display_utils import (
    GREEN, YELLOW, CYAN, RED, BOLD, RESET,
    clear_screen, render_number_row, render_separator,
)


# ---------------------------------------------------------------------------
# Internal display helper
# ---------------------------------------------------------------------------

def _show(
    top: str,
    bot: str,
    result_slots: list[str],
    *,
    top_hl: int | None = None,                       # 0 = units digit of top
    bot_hl: bool = False,
    result_hl: int | frozenset[int] | None = None,   # column(s) to highlight
    carry: int = 0,
    carry_hl: bool = False,
    result_final: bool = False,                       # all result digits in green
) -> None:
    """Print the full multiplication column layout."""
    width = len(result_slots)

    # Normalise result_hl to a set
    if result_hl is None:
        hl_cols: frozenset[int] = frozenset()
    elif isinstance(result_hl, int):
        hl_cols = frozenset({result_hl})
    else:
        hl_cols = result_hl

    # Top number row
    top_cells: list[tuple[str, bool, str]] = []
    for i, d in enumerate(top):
        pos = len(top) - 1 - i   # distance from right (0 = units)
        hl = (pos == top_hl)
        top_cells.append((d, hl, GREEN if hl else ""))

    carry_text = ""
    if carry > 0:
        if carry_hl:
            carry_text = f"    retenue: {CYAN}{BOLD}[{carry}]{RESET}"
        else:
            carry_text = f"    retenue: [{carry}]"   # brackets kept so width never shifts

    print(render_number_row(width, top_cells, suffix_mid=carry_text))

    # Multiplier row
    bot_cells: list[tuple[str, bool, str]] = [(bot, bot_hl, CYAN if bot_hl else "")]
    print(render_number_row(width, bot_cells, prefix="x  "))

    # Separator
    print(render_separator(width))

    # Result row
    result_cells: list[tuple[str, bool, str]] = []
    for i, slot in enumerate(result_slots):
        if result_final:
            result_cells.append((slot, True, GREEN))
        else:
            hl = i in hl_cols
            result_cells.append((slot, hl, YELLOW if hl else ""))
    print(render_number_row(width, result_cells))
    print()


def _blink(
    top: str,
    bot: str,
    result_slots: list[str],
    *,
    result_hl: int | frozenset[int] | None = None,
    carry: int = 0,
    carry_hl: bool = False,
    duration: float = 1.0,
    n_blinks: int = 4,
) -> None:
    """Flash a highlighted element on/off for `duration` seconds, ending highlighted."""
    interval = duration / (n_blinks * 2)
    for i in range(n_blinks * 2 + 1):  # +1 so final frame is always "on"
        on = (i % 2 == 0)
        clear_screen()
        _show(
            top, bot, result_slots,
            result_hl=result_hl if on else None,
            carry=carry,
            carry_hl=carry_hl if on else False,
        )
        if i < n_blinks * 2:
            time.sleep(interval)


# ---------------------------------------------------------------------------
# Core subroutine — reusable (e.g. from euclidean division)
# ---------------------------------------------------------------------------

def run_multiplication_interactive(a: int, b: int) -> None:
    """Guide the student step-by-step through the column multiplication a × b.

    ``a`` may have any number of digits; ``b`` must be a single digit 0–9.
    All display and interaction happen here; the caller only provides operands.
    """
    top = str(a)
    bot = str(b)

    # --- Special case: multiplying by 0 ---
    if b == 0:
        width = len(top)
        result_slots = [" "] * (width - 1) + ["0"]
        clear_screen()
        _show(top, bot, result_slots)
        print(f"Tout nombre multiplié par 0 est égal à {BOLD}0{RESET}.")
        input("\nAppuie sur Entrée pour continuer...")
        return

    result = a * b
    result_str = str(result)
    # width ≥ len(top) always when b ≥ 1
    width = len(result_str)
    result_slots: list[str] = ["?"] * width
    carry = 0

    # Initial layout
    clear_screen()
    _show(top, bot, result_slots)
    input("Appuie sur Entrée pour commencer...")

    for step in range(len(top)):
        pos_from_right = step
        top_idx = len(top) - 1 - step
        digit_a = int(top[top_idx])
        result_col = width - 1 - step
        is_last_step = (step == len(top) - 1)

        # Show display with current digit pair highlighted
        clear_screen()
        _show(top, bot, result_slots,
              top_hl=pos_from_right, bot_hl=True,
              carry=carry)

        # Step 1 — ask the basic multiplication fact
        product_raw = digit_a * b
        while True:
            raw = input(f"Combien font {digit_a} × {b} ? ").strip()
            if raw.lstrip("-").isdigit() and int(raw) == product_raw:
                print(f"{GREEN}Oui !{RESET}")
                break
            print(f"{RED}Non, ce n'est pas {raw}... Combien font {digit_a} × {b} ?{RESET}")

        # Step 2 — add previous carry if any
        total = product_raw + carry
        if carry > 0:
            # For single-digit products, show the value temporarily in the result slot
            if product_raw < 10:
                result_slots[result_col] = str(product_raw)
                clear_screen()
                _show(top, bot, result_slots,
                      result_hl=result_col,
                      carry=carry, carry_hl=True)
            else:
                clear_screen()
                _show(top, bot, result_slots, carry=carry, carry_hl=True)

            print(f"  {digit_a} × {b} = {BOLD}{product_raw}{RESET}")
            print(f"J'avais une retenue de {carry}, donc {product_raw} + {carry} = ?")
            while True:
                raw = input("> ").strip()
                if raw.lstrip("-").isdigit() and int(raw) == total:
                    print(f"{GREEN}Bravo !{RESET}")
                    break
                print(f"{RED}Non, ce n'est pas {raw}... {product_raw} + {carry} = ?{RESET}")

        # Step 3 — pose and carry
        pose = total % 10
        new_carry = total // 10

        if is_last_step and new_carry > 0:
            # Last digit and total is two digits: place both directly, no retenue left
            result_slots[result_col] = str(pose)
            result_slots[result_col - 1] = str(new_carry)
            both_cols = frozenset({result_col - 1, result_col})

            print(f"Je pose {YELLOW}{BOLD}{total}{RESET}.")
            input("Appuie sur Entrée pour continuer...")

            _blink(top, bot, result_slots, result_hl=both_cols, carry=0)

            carry = 0

            # Land with both digits highlighted
            clear_screen()
            _show(top, bot, result_slots, result_hl=both_cols)

        else:
            result_slots[result_col] = str(pose)

            if new_carry > 0:
                print(f"Je pose {YELLOW}{BOLD}{pose}{RESET} et je retiens {CYAN}{BOLD}{new_carry}{RESET}.")
            else:
                print(f"Je pose {YELLOW}{BOLD}{pose}{RESET}.")
            input("Appuie sur Entrée pour continuer...")

            # Blink posed digit (1 s), old carry cleared, new carry not yet shown
            _blink(top, bot, result_slots, result_hl=result_col, carry=0)

            if new_carry > 0:
                # Blink new carry (1 s), posed digit steady
                _blink(top, bot, result_slots, carry=new_carry, carry_hl=True)

            carry = new_carry

            # Land with posed digit AND retenue both highlighted
            clear_screen()
            _show(top, bot, result_slots,
                  result_hl=result_col,
                  carry=carry,
                  carry_hl=(carry > 0))

        input("Appuie sur Entrée pour continuer...")

    # Place any remaining carry (normal path: last step had no overflow)
    if carry > 0:
        result_slots[0] = str(carry)
        clear_screen()
        _show(top, bot, result_slots)

    # Final verification
    clear_screen()
    _show(top, bot, result_slots)
    print(f"Quel est le résultat de {a} × {b} ?")
    while True:
        raw = input("> ").strip()
        if raw == result_str:
            print(f"{GREEN}Bravo !{RESET}")
            break
        print(f"{RED}Non, ce n'est pas {raw}... Quel est le résultat de {a} × {b} ?{RESET}")

    # Show final result in green
    clear_screen()
    _show(top, bot, result_slots, result_final=True)
    print(f"  {GREEN}{BOLD}{a} × {b} = {result}{RESET}\n")
    input("Appuie sur Entrée pour continuer...")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Ask for two numbers and launch the guided multiplication."""
    print(f"\n{BOLD}=== Multiplication par un chiffre ==={RESET}\n")

    while True:
        raw = input("Quel est le premier nombre (peut avoir plusieurs chiffres) ? ").strip()
        if raw.isdigit() and int(raw) > 0:
            a = int(raw)
            break
        print(f"{RED}Merci d'entrer un nombre entier positif.{RESET}")

    while True:
        raw = input("Quel est le deuxième nombre (un seul chiffre, de 0 à 9) ? ").strip()
        if raw.isdigit() and len(raw) == 1:
            b = int(raw)
            break
        print(f"{RED}Merci d'entrer un seul chiffre (0 à 9).{RESET}")

    run_multiplication_interactive(a, b)


if __name__ == "__main__":
    main()
