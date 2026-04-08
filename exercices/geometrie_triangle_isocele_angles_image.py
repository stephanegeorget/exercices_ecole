"""Quiz très guidé : calcul d'angles dans un triangle isocèle (inspiré d'une fiche en photo)."""

from __future__ import annotations

import random

from .logger import log_result
from .utils import ask_choice_with_navigation, show_lesson

DISPLAY_NAME = "Géométrie : Triangles isocèles (baby steps)"

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


EXERCISES: list[dict[str, object]] = [
    {
        "title": "Exercice 1",
        "statement": "ABC est un triangle isocèle en A et l'angle ABC vaut 37°.",
        "equal_angles": "Dans un triangle isocèle en A, les angles en B et en C sont égaux.",
        "known_angle": "37°",
        "sum_step": "Somme des 3 angles : 180°. Donc angle A = 180° - (37° + 37°) = 106°.",
        "target": "L'angle BAC",
        "answer": "106°",
        "distractors": ["74°", "143°", "53°"],
    },
    {
        "title": "Exercice 1 bis",
        "statement": "MNP est un triangle isocèle en M et l'angle MPN vaut 58°.",
        "equal_angles": "Dans un triangle isocèle en M, les angles en P et en N sont égaux.",
        "known_angle": "58°",
        "sum_step": "Somme des 3 angles : 180°. Donc angle M = 180° - (58° + 58°) = 64°.",
        "target": "L'angle PMN",
        "answer": "64°",
        "distractors": ["116°", "58°", "122°"],
    },
    {
        "title": "Exercice 2",
        "statement": "LAC est un triangle isocèle en L et l'angle ALC vaut 82°.",
        "equal_angles": "Dans un triangle isocèle en L, les angles en A et en C sont égaux.",
        "known_angle": "82°",
        "sum_step": "180° - 82° = 98°, puis 98° ÷ 2 = 49°.",
        "target": "Les angles LAC et LCA",
        "answer": "49° et 49°",
        "distractors": ["41° et 41°", "82° et 82°", "98° et 98°"],
    },
    {
        "title": "Exercice 2 bis",
        "statement": "ARE est un triangle isocèle en A et l'angle RAE vaut 124°.",
        "equal_angles": "Dans un triangle isocèle en A, les angles en R et en E sont égaux.",
        "known_angle": "124°",
        "sum_step": "180° - 124° = 56°, puis 56° ÷ 2 = 28°.",
        "target": "Les angles ARE et REA",
        "answer": "28° et 28°",
        "distractors": ["62° et 62°", "56° et 56°", "124° et 124°"],
    },
]


def _ask_baby_step(prompt: str, choices: list[str], answer: str, rng: random.Random) -> bool:
    candidates = [answer] + [choice for choice in choices if choice != answer]
    rng.shuffle(candidates)
    answer_index = candidates.index(answer)

    print(f"\n{prompt}")
    selected, _, wants_exit = ask_choice_with_navigation(candidates)
    if wants_exit:
        raise KeyboardInterrupt
    if selected is None or selected < 0:
        print(f"{RED}Réponse invalide.{RESET}")
        return False

    if selected == answer_index:
        print(f"{GREEN}Oui, c'est bien ça.{RESET}")
        return True

    print(f"{RED}Pas encore. La bonne réponse était : {answer}.{RESET}")
    return False


def main() -> None:
    lesson = f"""
{CYAN}{BOLD}Calculer un angle dans un triangle isocèle (version lente, pas à pas){RESET}

Ce quiz est inspiré de la fiche en photo.
Ici, on avance en {BOLD}baby steps{RESET}.

{BOLD}Rappel 1{RESET}
Dans un triangle isocèle, les {BOLD}2 angles à la base{RESET} sont égaux.

{BOLD}Rappel 2{RESET}
Dans n'importe quel triangle, la somme des 3 angles vaut toujours {BOLD}180°{RESET}.

{BOLD}Méthode ultra-lente{RESET}
1) Je repère les angles égaux.
2) Je remplace les angles égaux par la même valeur.
3) J'utilise la somme 180°.
4) Je calcule l'angle demandé.

Tu vas refaire 4 exercices de la fiche, en 3 mini-questions chacun.
"""
    show_lesson(lesson)

    score = 0
    total = len(EXERCISES) * 3
    rng = random.Random()

    try:
        for index, exercise in enumerate(EXERCISES, start=1):
            title = str(exercise["title"])
            statement = str(exercise["statement"])
            equal_angles = str(exercise["equal_angles"])
            known_angle = str(exercise["known_angle"])
            sum_step = str(exercise["sum_step"])
            target = str(exercise["target"])
            answer = str(exercise["answer"])
            distractors = list(exercise["distractors"])

            print(f"\n{CYAN}{BOLD}{title} ({index}/{len(EXERCISES)}){RESET}")
            print(statement)

            if _ask_baby_step(
                f"{BOLD}Mini-question 1/3{RESET} — Quelle phrase est vraie ?",
                [
                    equal_angles,
                    "Les 3 angles sont toujours égaux.",
                    "La somme des angles est 360°.",
                    "Un triangle isocèle a toujours un angle droit.",
                ],
                equal_angles,
                rng,
            ):
                score += 1

            if _ask_baby_step(
                f"{BOLD}Mini-question 2/3{RESET} — Quelle opération correspond au calcul ?",
                [
                    sum_step,
                    f"180° + {known_angle}",
                    f"{known_angle} ÷ 2 puis + 180°",
                    "On ne peut rien calculer.",
                ],
                sum_step,
                rng,
            ):
                score += 1

            if _ask_baby_step(
                f"{BOLD}Mini-question 3/3{RESET} — Quelle est la mesure de {target} ?",
                [answer] + distractors,
                answer,
                rng,
            ):
                score += 1

            print(f"Correction douce : {BOLD}{answer}{RESET}.")

    except KeyboardInterrupt:
        print("\nRetour au menu demandé.")

    percentage = score / total * 100
    print(f"\n{BOLD}Résultat final :{RESET} {score}/{total} ({percentage:.1f}%).")
    log_result("geometrie_triangle_isocele_angles_image", percentage)


if __name__ == "__main__":
    main()
