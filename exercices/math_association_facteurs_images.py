"""Quiz guidé sur l'association astucieuse de facteurs (inspiré d'une fiche en photo)."""

from __future__ import annotations

from decimal import Decimal

from .logger import log_result
from .utils import ask_choice_with_navigation, show_lesson

DISPLAY_NAME = "Maths : Associer astucieusement les facteurs (quiz fléché)"

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


MULTIPLICATIONS: list[dict[str, object]] = [
    {
        "label": "A",
        "factors": ["2", "43", "5"],
        "pair": ("2", "5"),
        "pair_result": "10",
        "final": "430",
    },
    {
        "label": "B",
        "factors": ["2,5", "17", "4", "10"],
        "pair": ("2,5", "4"),
        "pair_result": "10",
        "final": "1700",
    },
    {
        "label": "C",
        "factors": ["5", "71,38", "4", "5"],
        "pair": ("5", "4"),
        "pair_result": "20",
        "final": "7138",
    },
    {
        "label": "D",
        "factors": ["10", "4", "0,8"],
        "pair": ("10", "0,8"),
        "pair_result": "8",
        "final": "32",
    },
    {
        "label": "E",
        "factors": ["2", "12,3", "50"],
        "pair": ("2", "50"),
        "pair_result": "100",
        "final": "1230",
    },
    {
        "label": "F",
        "factors": ["25", "3,7", "4"],
        "pair": ("25", "4"),
        "pair_result": "100",
        "final": "370",
    },
    {
        "label": "G",
        "factors": ["12", "2,5", "5", "4"],
        "pair": ("2,5", "4"),
        "pair_result": "10",
        "final": "600",
    },
    {
        "label": "H",
        "factors": ["7", "0,25", "9", "4"],
        "pair": ("0,25", "4"),
        "pair_result": "1",
        "final": "63",
    },
]


def _expression_text(factors: list[str]) -> str:
    return " × ".join(factors)


def _value(text: str) -> Decimal:
    return Decimal(text.replace(",", "."))


def _pair_options(factors: list[str], pair: tuple[str, str]) -> list[str]:
    a, b = pair
    distractors = []
    if len(factors) >= 3:
        distractors.append((factors[0], factors[1]))
        distractors.append((factors[-2], factors[-1]))
    options = [f"({a} × {b})"]
    for x, y in distractors:
        text = f"({x} × {y})"
        if text not in options:
            options.append(text)
    while len(options) < 3:
        options.append(f"({factors[0]} × {factors[-1]})")
    return options[:3]


def _rearrangements(factors: list[str], pair: tuple[str, str]) -> tuple[str, list[str]]:
    a, b = pair
    remaining = factors.copy()
    remaining.remove(a)
    remaining.remove(b)

    correct = f"{_expression_text(factors)}  →  ({a} × {b}) × {' × '.join(remaining)}"
    wrong_one = f"{_expression_text(factors)}  →  ({factors[0]} × {factors[1]}) × {' × '.join(factors[2:])}"
    wrong_two = f"{_expression_text(factors)}  →  ({remaining[0]} × {remaining[-1]}) × {a} × {b}"
    options = [correct, wrong_one, wrong_two]
    return correct, options


def _ask_question(prompt: str, choices: list[str], answer_index: int) -> bool:
    print(f"\n{prompt}")
    selected, _, wants_exit = ask_choice_with_navigation(choices)
    if wants_exit:
        raise KeyboardInterrupt
    if selected is None or selected < 0:
        print(f"{RED}Réponse invalide.{RESET}")
        return False
    ok = selected == answer_index
    if ok:
        print(f"{GREEN}Bravo, c'est correct !{RESET}")
    else:
        print(f"{RED}Ce n'est pas la meilleure association.{RESET}")
    return ok


def main() -> None:
    lesson = f"""
{CYAN}{BOLD}Associer astucieusement les facteurs (inspiré de la fiche en photo){RESET}

Tu vas travailler les multiplications A à H.
Pour chaque multiplication, on prend {BOLD}3 mini-questions{RESET} pour avancer lentement :
1) choisir la meilleure association de deux nombres ;
2) suivre une réécriture avec des flèches et des parenthèses ;
3) donner le résultat final.

{BOLD}Fiche de départ{RESET}
A = 2 × 43 × 5
B = 2,5 × 17 × 4 × 10
C = 5 × 71,38 × 4 × 5
D = 10 × 4 × 0,8
E = 2 × 12,3 × 50
F = 25 × 3,7 × 4
G = 12 × 2,5 × 5 × 4
H = 7 × 0,25 × 9 × 4

Astuce : on cherche souvent un produit facile comme 10, 20, 100 ou 1.
"""
    show_lesson(lesson)

    score = 0
    total = len(MULTIPLICATIONS) * 3

    try:
        for index, item in enumerate(MULTIPLICATIONS, start=1):
            label = str(item["label"])
            factors = list(item["factors"])
            pair = tuple(item["pair"])
            pair_result = str(item["pair_result"])
            final = str(item["final"])

            print(f"\n{CYAN}{BOLD}Multiplication {label} ({index}/{len(MULTIPLICATIONS)}){RESET}")
            print(f"Calcul : {BOLD}{_expression_text(factors)}{RESET}")

            # Question 1/3
            pair_choices = _pair_options(factors, pair)
            right_pair = f"({pair[0]} × {pair[1]})"
            if _ask_question(
                f"{BOLD}Question 1/3{RESET} — Quelle association est la plus astucieuse pour commencer ?",
                pair_choices,
                pair_choices.index(right_pair),
            ):
                score += 1
            print(
                f"Explication : commencer par {CYAN}{right_pair}{RESET} donne rapidement {BOLD}{pair_result}{RESET}."
            )

            # Question 2/3 (UI spéciale fléchée)
            correct, rearrangements = _rearrangements(factors, pair)
            highlighted = correct.replace(
                f"({pair[0]} × {pair[1]})",
                f"{CYAN}{BOLD}({pair[0]} × {pair[1]}){RESET}",
            )
            print(
                f"\n{BOLD}Réécriture modèle :{RESET} {highlighted}\n"
                f"Le premier produit à faire est mis en couleur."
            )
            if _ask_question(
                f"{BOLD}Question 2/3{RESET} — Quelle ligne avec flèche montre la bonne réorganisation ?",
                rearrangements,
                rearrangements.index(correct),
            ):
                score += 1

            # Question 3/3
            result_choices = [
                final,
                str(_value(final) + Decimal("10")),
                str(_value(final) / Decimal("10")),
            ]
            if _ask_question(
                f"{BOLD}Question 3/3{RESET} — Après l'association astucieuse, quel est le résultat final ?",
                result_choices,
                0,
            ):
                score += 1
            print(f"Correction : {label} = {BOLD}{final}{RESET}.")

    except KeyboardInterrupt:
        print("\nRetour au menu demandé.")

    percentage = score / total * 100
    print(f"\n{BOLD}Résultat final :{RESET} {score}/{total} ({percentage:.1f}%).")
    log_result("math_association_facteurs_images", percentage)


if __name__ == "__main__":
    main()
