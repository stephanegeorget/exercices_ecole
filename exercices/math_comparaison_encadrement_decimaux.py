"""Leçon et quiz centrés sur la comparaison et l'encadrement des nombres décimaux."""

import textwrap

from .logger import log_result
from .utils import ask_choice_with_navigation, format_fraction, show_lesson

DISPLAY_NAME = "Maths : Comparaison et encadrement des décimaux"

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main() -> None:
    """Affiche la leçon inspirée du support et lance un quiz de 20 questions."""

    def indent_block(text: str, prefix: str = "    ") -> str:
        return textwrap.indent(text, prefix)

    tenth = format_fraction(1, 10)
    hundredth = format_fraction(1, 100)
    mixed_tenth = format_fraction(3, 10, prefix="4 + ")
    mixed_hundredth = format_fraction(7, 100, prefix="2 + ")

    lesson = f"""
{CYAN}{BOLD}Comparer et encadrer les nombres décimaux{RESET}

{BOLD}1) Définitions clés{RESET}
- Comparer deux nombres consiste à dire s'ils sont égaux, ou si l'un est plus grand ou plus petit.
- Les symboles utiles sont : « < » plus petit, « > » plus grand, « = » égal.
- Encadrer un nombre revient à trouver deux nombres entre lesquels il se situe (souvent au dixième ou au centième).

{BOLD}2) Repères de numération{RESET}
- On compare d'abord la partie entière, puis les dixièmes, centièmes, millièmes...
- Exemple : 3,408 < 3,48 car 3 = 3 mais 0,408 < 0,48.
- Tableau de numération : unités | dixièmes | centièmes | millièmes.

{BOLD}3) Encadrer à un rang donné{RESET}
- Encadrer au dixième : on cherche les deux dixièmes qui entourent le nombre.
- Encadrer au centième : on cherche les deux centièmes les plus proches.
- Exemple au dixième : 7,08 se situe entre 7,0 et 7,1.
- Exemple au centième : 5,237 se situe entre 5,23 et 5,24.

{BOLD}4) Écritures fractionnaires utiles{RESET}
- Un dixième s'écrit :
{indent_block(tenth)}
- Un centième s'écrit :
{indent_block(hundredth)}
- Nombre mixte avec dixièmes :
{indent_block(mixed_tenth)} = 4,3.
- Nombre mixte avec centièmes :
{indent_block(mixed_hundredth)} = 2,07.

{BOLD}5) Droite graduée et proportionnalité{RESET}
- Sur une droite graduée entre deux entiers, chaque intervalle peut être partagé en dixièmes puis en centièmes.
- Comparer ou encadrer revient à repérer la place exacte du nombre entre deux graduations.

Prêt ? Entraîne-toi maintenant sur la comparaison et l'encadrement !
"""

    show_lesson(lesson)

    questions = [
        {
            "question": "Quelle est la première étape pour comparer deux nombres décimaux ?",
            "choices": [
                "Comparer la partie entière",
                "Comparer directement les millièmes",
                "Additionner les deux nombres",
            ],
            "answer": 0,
        },
        {
            "question": "Que signifie le symbole > entre deux nombres ?",
            "choices": ["Le premier est plus petit", "Le premier est plus grand", "Les deux sont égaux"],
            "answer": 1,
        },
        {
            "question": "Lequel est le plus grand : 4,38 ou 4,083 ?",
            "choices": ["4,38", "4,083", "Ils sont égaux"],
            "answer": 0,
        },
        {
            "question": "Quel nombre se situe entre 2,3 et 2,4 ?",
            "choices": ["2,25", "2,35", "2,41"],
            "answer": 1,
        },
        {
            "question": "Complète : 7,08 est encadré au dixième par...",
            "choices": ["7,07 < 7,08 < 7,09", "7,0 < 7,08 < 7,1", "7 < 7,08 < 8"],
            "answer": 1,
        },
        {
            "question": "Complète : 5,237 est encadré au centième par...",
            "choices": ["5,23 et 5,24", "5,2 et 5,3", "5,30 et 5,31"],
            "answer": 0,
        },
        {
            "question": "Quel nombre est le plus petit ?",
            "choices": ["6,105", "6,15", "6,015"],
            "answer": 2,
        },
        {
            "question": "Quel ordre est croissant ?",
            "choices": ["3,402 < 3,42 < 3,5", "3,42 < 3,402 < 3,5", "3,5 < 3,42 < 3,402"],
            "answer": 0,
        },
        {
            "question": "Quel nombre complète 2,4 < ? < 2,5 avec un centième ?",
            "choices": ["2,38", "2,46", "2,51"],
            "answer": 1,
        },
        {
            "question": "Quel dixième encadre 9,502 ?",
            "choices": ["9,5 < 9,502 < 9,6", "9,4 < 9,502 < 9,5", "9 < 9,502 < 10"],
            "answer": 0,
        },
        {
            "question": "Quelle écriture montre un encadrement au centième de 3,789 ?",
            "choices": ["3,7 < 3,789 < 3,8", "3,78 < 3,789 < 3,79", "3,78 < 3,789 < 3,80"],
            "answer": 1,
        },
        {
            "question": "Lequel est le plus grand : 8,07 ou 8,7 ?",
            "choices": ["8,07", "8,7", "Ils sont égaux"],
            "answer": 1,
        },
        {
            "question": "Quel est le nombre du milieu entre 1,2 et 1,3 ?",
            "choices": ["1,21", "1,25", "1,29"],
            "answer": 1,
        },
        {
            "question": "Quelle fraction décimale correspond au dixième juste après 3 ?",
            "choices": [format_fraction(31, 10), format_fraction(3, 10), format_fraction(30, 1)],
            "answer": 0,
        },
        {
            "question": "Quel encadrement au dixième pour 12,78 est correct ?",
            "choices": ["12,7 < 12,78 < 12,8", "12,78 < 12,8 < 12,9", "12,6 < 12,78 < 12,7"],
            "answer": 0,
        },
        {
            "question": "Quel encadrement au centième pour 0,904 est correct ?",
            "choices": ["0,9 < 0,904 < 0,91", "0,90 < 0,904 < 0,91", "0,89 < 0,904 < 0,90"],
            "answer": 1,
        },
        {
            "question": "Complète : 2,07 correspond à...",
            "choices": ["2 unités et 7 dixièmes", "2 unités et 7 centièmes", "2 dixièmes et 7 centièmes"],
            "answer": 1,
        },
        {
            "question": "Quelle comparaison est vraie ?",
            "choices": ["4,5 = 4,50", "4,05 > 4,5", "4,500 < 4,5"],
            "answer": 0,
        },
        {
            "question": "Quel nombre se situe juste après 3,409 au centième près ?",
            "choices": ["3,41", "3,409", "3,40"],
            "answer": 0,
        },
        {
            "question": "Sur une droite graduée de 5 à 6, où placer 5,48 ?",
            "choices": ["Un peu avant la moitié", "Juste après la moitié", "Tout au bout"],
            "answer": 0,
        },
    ]

    print(
        "Quiz : réponds à chaque question en choisissant la lettre de la bonne réponse (a, b, c...)\n"
        "Astuce : utilise les flèches pour naviguer entre les propositions ou tape directement la lettre."
        " Tape 'q' à tout moment pour retourner au menu précédent."
    )
    score = 0
    for i, q in enumerate(questions, start=1):
        question_label = f"Question {i}: "
        question_lines = q["question"].splitlines()
        if question_lines:
            print(f"\n{question_label}{question_lines[0]}")
            continuation_indent = " " * len(question_label)
            for extra_line in question_lines[1:]:
                print(f"{continuation_indent}{extra_line}")
        else:
            print(f"\n{question_label}")

        student, option_letters, quit_requested = ask_choice_with_navigation(q["choices"])
        if quit_requested:
            print("\nRetour au menu Mathématiques demandé. Fin du quiz.\n")
            return
        correct = q["answer"]
        correct_text = q["choices"][correct]
        correct_letter = option_letters[correct]
        if student == correct:
            print(f"{GREEN}Exact ! ✅{RESET}")
            score += 1
        else:
            correct_lines = str(correct_text).splitlines()
            print(
                f"{RED}Non, la bonne réponse était {correct_letter}) {correct_lines[0]} ❌{RESET}"
            )
            for extra_line in correct_lines[1:]:
                print(f"{RED}   {extra_line}{RESET}")

    total = len(questions)
    print(f"\n{BOLD}Score final : {score}/{total}{RESET}")
    if score == total:
        print(f"{GREEN}Bravo ! Tu maîtrises les comparaisons et encadrements décimaux. 🥳{RESET}")
    elif score >= total * 0.6:
        print(f"{CYAN}Beau travail ! Quelques révisions et ce sera parfait. 👍{RESET}")
    else:
        print(f"{RED}Courage, relis la leçon et réessaie ! 💪{RESET}")
    log_result("math_comparaison_encadrement_decimaux", score / total * 100)


if __name__ == "__main__":
    main()
