from __future__ import annotations

"""Multiplication posée d'un nombre par un chiffre avec guidage pas à pas."""

DISPLAY_NAME = "Maths : Multiplication posée (× 1 chiffre)"

CELL_WIDTH = 3
GAP = " "


def _digit_cell(char: str, highlighted: bool = False) -> list[str]:
    """Retourne une cellule 3x3 contenant ``char`` centré, avec éventuelle boîte."""

    if highlighted:
        return ["+-+", f"|{char}|", "+-+"]
    return ["   ", f" {char} ", "   "]


def _row_cells(
    chars: list[str],
    highlights: set[int],
    width: int,
    fill: str = " ",
) -> list[str]:
    """Construit une ligne de cellules de longueur ``width`` alignée à droite."""

    padded = [fill] * (width - len(chars)) + chars
    rows = ["", "", ""]
    for idx, ch in enumerate(padded):
        cell = _digit_cell(ch, idx in highlights and ch != fill)
        for line_no in range(3):
            if rows[line_no]:
                rows[line_no] += GAP
            rows[line_no] += cell[line_no]
    return rows


def _render_layout(
    first: str,
    second_digit: str,
    result_digits: list[str],
    highlight_first: int | None = None,
    highlight_second: bool = False,
    highlight_result: int | None = None,
    carry: int | None = None,
    carry_highlight: bool = False,
) -> str:
    """Génère l'affichage complet de la multiplication posée."""

    width = max(len(first), len(result_digits), 2)
    first_hl = set()
    if highlight_first is not None:
        first_hl.add(width - len(first) + highlight_first)

    second_hl = {width - 1} if highlight_second else set()
    result_hl = {highlight_result} if highlight_result is not None else set()

    carry_text = "retenue: "
    if carry is None:
        carry_text += " "
    elif carry_highlight:
        carry_text += f"[[{carry}]]"
    else:
        carry_text += str(carry)

    first_rows = _row_cells(list(first), first_hl, width)
    second_rows = _row_cells([second_digit], second_hl, width)
    result_rows = _row_cells(result_digits, result_hl, width, fill="?")

    bar = "-" * len(first_rows[1])
    lines = [
        f"   {first_rows[0]}    {carry_text}",
        f"   {first_rows[1]}    ",
        f"   {first_rows[2]}    ",
        f"x  {second_rows[0]}    ",
        f"x  {second_rows[1]}    ",
        f"x  {second_rows[2]}    ",
        f"   {bar}",
        f"   {result_rows[0]}",
        f"   {result_rows[1]}",
        f"   {result_rows[2]}",
    ]
    return "\n".join(lines)


def _ask_int(prompt: str, validator) -> int:
    while True:
        ans = input(prompt).strip()
        if ans.isdigit() and validator(int(ans)):
            return int(ans)
        print("Entrée invalide.")


def _run_multiplication_workflow(first: int, second: int) -> None:
    first_text = str(first)
    second_text = str(second)
    work = ["?"] * (len(first_text) + 1)

    print(_render_layout(first_text, second_text, work))

    carry = 0
    pos_result = len(work) - 1

    for i in range(len(first_text) - 1, -1, -1):
        d = int(first_text[i])
        while True:
            guess = _ask_int(f"Combien font {d} x {second} ? ", lambda n: n >= 0)
            if guess == d * second:
                print("Oui !")
                break
            print(f"Non ce n'est pas {guess}...")

        product = d * second
        unit = product % 10
        carry_from_product = product // 10

        if carry == 0:
            work[pos_result] = str(unit)
            print(f"Je pose {unit}" + (f" et je retiens {carry_from_product}" if carry_from_product else ""))
            carry = carry_from_product
            print(_render_layout(first_text, second_text, work, highlight_first=i, highlight_second=True, highlight_result=pos_result, carry=carry if carry else None))
        else:
            work[pos_result] = str(unit)
            print("Oui ! Je pose", unit, ", et j'ajoute la retenue.")
            print(_render_layout(first_text, second_text, work, highlight_first=i, highlight_second=True, highlight_result=pos_result, carry=carry, carry_highlight=True))
            sum_guess = _ask_int(f"{unit} + {carry} = ? ", lambda n: n >= 0)
            while sum_guess != unit + carry:
                print("Essaie encore.")
                sum_guess = _ask_int(f"{unit} + {carry} = ? ", lambda n: n >= 0)
            total = unit + carry
            work[pos_result] = str(total % 10)
            carry = carry_from_product + (total // 10)
            print("Bravo !")
            print(_render_layout(first_text, second_text, work, carry=carry if carry else None))

        pos_result -= 1

    if carry:
        work[pos_result] = str(carry)
    else:
        work = work[1:]

    final_result = "".join(work)
    answer = _ask_int(f"Quel est le résultat de {first} x {second} ? ", lambda n: True)
    if str(answer) == final_result:
        print("Bravo !")
    else:
        print(f"Ce n'est pas ça. Le résultat est {final_result}.")


def main() -> None:
    print("Multiplication posée d'un nombre par un chiffre")
    first = _ask_int("Quel est le premier nombre à multiplier ? ", lambda n: n >= 0)
    second = _ask_int("Quel est le deuxième nombre (0 à 9) ? ", lambda n: 0 <= n <= 9)
    _run_multiplication_workflow(first, second)


if __name__ == "__main__":
    main()
