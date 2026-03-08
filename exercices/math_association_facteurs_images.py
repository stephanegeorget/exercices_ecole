"""Quiz guidé sur l'association astucieuse de facteurs (inspiré d'une fiche en photo)."""

from __future__ import annotations

import random
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
        "group": ["2", "5"],
        "group_result": "10",
        "final": "430",
    },
    {
        "label": "B",
        "factors": ["2,5", "17", "4", "10"],
        "group": ["2,5", "4"],
        "group_result": "10",
        "final": "1700",
    },
    {
        "label": "C",
        "factors": ["5", "71,38", "4", "5"],
        "group": ["5", "4", "5"],
        "group_result": "100",
        "final": "7138",
    },
    {
        "label": "D",
        "factors": ["10", "4", "0,8"],
        "group": ["10", "0,8"],
        "group_result": "8",
        "final": "32",
    },
    {
        "label": "E",
        "factors": ["2", "12,3", "50"],
        "group": ["2", "50"],
        "group_result": "100",
        "final": "1230",
    },
    {
        "label": "F",
        "factors": ["25", "3,7", "4"],
        "group": ["25", "4"],
        "group_result": "100",
        "final": "370",
    },
    {
        "label": "G",
        "factors": ["12", "2,5", "5", "4"],
        "group": ["2,5", "4"],
        "group_result": "10",
        "final": "600",
    },
    {
        "label": "H",
        "factors": ["7", "0,25", "9", "4"],
        "group": ["0,25", "4"],
        "group_result": "1",
        "final": "63",
    },
]


def _expression_text(factors: list[str]) -> str:
    return " × ".join(factors)


def _group_text(group: list[str]) -> str:
    return f"({' × '.join(group)})"


def _value(text: str) -> Decimal:
    return Decimal(text.replace(",", "."))


def _remove_group_once(factors: list[str], group: list[str]) -> list[str]:
    remaining = factors.copy()
    for element in group:
        remaining.remove(element)
    return remaining


def _group_options(factors: list[str], group: list[str]) -> list[str]:
    options = [_group_text(group)]

    pair_a = factors[:2]
    pair_b = factors[-2:]
    for proposal in (pair_a, pair_b):
        proposal_text = _group_text(proposal)
        if proposal_text not in options:
            options.append(proposal_text)

    if len(factors) >= 4:
        first_three = factors[:3]
        first_three_text = _group_text(first_three)
        if first_three_text not in options:
            options.append(first_three_text)

    while len(options) < 4:
        fallback = _group_text([factors[0], factors[-1]])
        if fallback not in options:
            options.append(fallback)
        else:
            options.append(_group_text([factors[1], factors[-1]]))

    return options[:4]


def _rearrangements(factors: list[str], group: list[str]) -> tuple[str, list[str]]:
    remaining = _remove_group_once(factors, group)
    group_text = _group_text(group)

    if remaining:
        tail = " × ".join(remaining)
        correct = f"{_expression_text(factors)}  →  {group_text} × {tail}"
    else:
        correct = f"{_expression_text(factors)}  →  {group_text}"

    wrong_one = f"{_expression_text(factors)}  →  {_group_text(factors[:2])} × {' × '.join(factors[2:])}"
    wrong_two_group = _group_text([remaining[0], group[0]]) if remaining else _group_text(factors[:2])
    wrong_two_tail = " × ".join(group[1:] + ([remaining[-1]] if remaining else []))
    wrong_two = f"{_expression_text(factors)}  →  {wrong_two_group} × {wrong_two_tail}"

    options = [correct, wrong_one, wrong_two]
    return correct, options


def _shuffle_choices(correct_choice: str, distractors: list[str], rng: random.Random) -> tuple[list[str], int]:
    choices = [correct_choice] + [choice for choice in distractors if choice != correct_choice]
    rng.shuffle(choices)
    return choices, choices.index(correct_choice)


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
Pour chaque multiplication, on avance avec {BOLD}3 mini-questions{RESET} :
1) choisir l'association la plus efficace (parfois 2 facteurs, parfois 3) ;
2) repérer la bonne réécriture avec parenthèses et flèches ;
3) donner le résultat final.

{BOLD}Méthode conseillée (surtout quand il y a 4 facteurs){RESET}
• Étape 1 : repérer le groupe facile (qui donne souvent 10, 20, 50, 100 ou 1).
• Étape 2 : remplacer ce groupe par son résultat.
• Étape 3 : terminer le calcul avec les facteurs restants.

{BOLD}Fiche de départ{RESET}
A = 2 × 43 × 5
B = 2,5 × 17 × 4 × 10
C = 5 × 71,38 × 4 × 5
D = 10 × 4 × 0,8
E = 2 × 12,3 × 50
F = 25 × 3,7 × 4
G = 12 × 2,5 × 5 × 4
H = 7 × 0,25 × 9 × 4
"""
    show_lesson(lesson)

    score = 0
    total = len(MULTIPLICATIONS) * 3
    rng = random.Random()

    try:
        for index, item in enumerate(MULTIPLICATIONS, start=1):
            label = str(item["label"])
            factors = list(item["factors"])
            group = list(item["group"])
            group_result = str(item["group_result"])
            final = str(item["final"])

            print(f"\n{CYAN}{BOLD}Multiplication {label} ({index}/{len(MULTIPLICATIONS)}){RESET}")
            print(f"Calcul : {BOLD}{_expression_text(factors)}{RESET}")

            # Question 1/3
            group_choices = _group_options(factors, group)
            right_group = _group_text(group)
            shuffled_group_choices, group_answer_index = _shuffle_choices(
                right_group,
                group_choices,
                rng,
            )
            if _ask_question(
                f"{BOLD}Question 1/3{RESET} — Quelle association est la plus astucieuse pour commencer ?",
                shuffled_group_choices,
                group_answer_index,
            ):
                score += 1
            print(
                f"Explication : commencer par {CYAN}{right_group}{RESET} donne rapidement {BOLD}{group_result}{RESET}."
            )

            # Question 2/3 (UI spéciale fléchée)
            correct, rearrangements = _rearrangements(factors, group)
            highlighted = correct.replace(
                right_group,
                f"{CYAN}{BOLD}{right_group}{RESET}",
            )
            print(
                f"\n{BOLD}Réécriture modèle :{RESET} {highlighted}\n"
                f"On calcule d'abord le groupe en couleur, puis on continue avec les autres facteurs."
            )
            shuffled_rearrangements, rearrangement_answer_index = _shuffle_choices(
                correct,
                rearrangements,
                rng,
            )
            if _ask_question(
                f"{BOLD}Question 2/3{RESET} — Quelle ligne avec flèche montre la bonne réorganisation ?",
                shuffled_rearrangements,
                rearrangement_answer_index,
            ):
                score += 1

            # Question 3/3
            result_distractors = [
                str(_value(final) + Decimal("10")),
                str(_value(final) / Decimal("10")),
                str(_value(final) - Decimal("10")),
            ]
            result_choices, result_answer_index = _shuffle_choices(final, result_distractors, rng)
            if _ask_question(
                f"{BOLD}Question 3/3{RESET} — Après l'association astucieuse, quel est le résultat final ?",
                result_choices,
                result_answer_index,
            ):
                score += 1

            remaining = _remove_group_once(factors, group)
            if remaining:
                print(
                    f"Correction détaillée : {_group_text(group)} = {group_result}, puis "
                    f"{group_result} × {' × '.join(remaining)} = {BOLD}{final}{RESET}."
                )
            else:
                print(f"Correction détaillée : {_group_text(group)} = {BOLD}{final}{RESET}.")

    except KeyboardInterrupt:
        print("\nRetour au menu demandé.")

    percentage = score / total * 100
    print(f"\n{BOLD}Résultat final :{RESET} {score}/{total} ({percentage:.1f}%).")
    log_result("math_association_facteurs_images", percentage)


if __name__ == "__main__":
    main()
