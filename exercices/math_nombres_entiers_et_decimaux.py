"""Leçon et quiz sur les nombres entiers et décimaux."""

import textwrap

from .logger import log_result
from .utils import ask_choice_with_navigation, format_fraction, show_lesson

DISPLAY_NAME = "Maths : Nombres entiers et décimaux"

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main() -> None:
    """Affiche une leçon synthétique puis un quiz à choix multiples."""

    def indent_block(text: str, prefix: str = "    ") -> str:
        return textwrap.indent(text, prefix)

    tenth = format_fraction(1, 10)
    quarter = format_fraction(1, 4)
    decimal_quarter = format_fraction(25, 100)
    mixed_example = format_fraction(37, 100, prefix="8 + ")
    hundredth = format_fraction(7, 100)

    lesson = f"""
{CYAN}{BOLD}Relier nombres entiers et nombres décimaux{RESET}

{BOLD}1) Nombres entiers{RESET}
- Un nombre entier ne comporte pas de partie décimale : 0, 7, 153...
- Il se lit et s'écrit grâce au tableau de numération : unités, dizaines, centaines, milliers...

{BOLD}2) Nombres décimaux{RESET}
- Un nombre décimal possède une partie entière et une partie décimale séparées par une virgule.
- Les chiffres après la virgule occupent les colonnes : dixièmes, centièmes, millièmes...
- Exemple : 12,305 = 12 unités + 3 dixièmes + 5 millièmes.

{BOLD}3) Fractions décimales et écriture à virgule{RESET}
- Une {BOLD}fraction décimale{RESET} a un dénominateur 10, 100, 1000... par exemple
{indent_block(tenth)}.
- Elle se convertit facilement en écriture à virgule : on divise le numérateur par 10, 100, 1000...
- {indent_block(quarter)}
  équivaut à {indent_block(decimal_quarter)}
  donc à 0,25 en écriture décimale.

{BOLD}4) Nombre mixte et valeur numérique{RESET}
- Un {BOLD}nombre mixte{RESET} combine partie entière et fraction :
{indent_block(mixed_example)}
  qui vaut 8 + 0,37 = 8,37.
- Le {BOLD}zéro{RESET} est un repère central : les nombres entiers négatifs ou positifs s'en éloignent sur la droite graduée.

{BOLD}5) Comparer, ranger, encadrer{RESET}
- Pour comparer :
  1. On compare la partie entière.
  2. Si elles sont égales, on compare les dixièmes, centièmes, etc.
- 4,8 > 4,72 car 4 = 4 mais 0,8 > 0,72.
- Encadrer 5,073 au centième : 5,07 < 5,073 < 5,08.

{BOLD}6) Arrondir{RESET}
- On regarde le chiffre situé après le rang choisi :
  • Arrondir 7,849 au dixième : on regarde le centième (4) → 7,8.
  • Arrondir 7,849 au centième : on regarde le millième (9) → 7,85.

{BOLD}7) Lien avec les pourcentages{RESET}
- Un pourcentage est une fraction sur 100 : 7 % = {indent_block(hundredth)} = 0,07.
- Comprendre ce lien aide à passer d'un contexte de proportion à un nombre décimal.

Relis les définitions, puis essaie le quiz pour vérifier tes repères sur les écritures et les conversions !
"""

    show_lesson(lesson)

    questions = [
        {
            "question": "Qu'est-ce qu'un nombre entier ?",
            "choices": [
                "Un nombre sans partie décimale",
                "Un nombre avec au moins un dixième",
                "Un nombre qui s'écrit forcément en fraction",
            ],
            "answer": 0,
        },
        {
            "question": "Quel élément sépare la partie entière et la partie décimale ?",
            "choices": ["Le signe +", "La virgule", "Le signe ="],
            "answer": 1,
        },
        {
            "question": "Dans 53,8, quel est le chiffre des dixièmes ?",
            "choices": ["5", "3", "8"],
            "answer": 2,
        },
        {
            "question": "Laquelle est une fraction décimale ?",
            "choices": [format_fraction(5, 12), format_fraction(7, 10), format_fraction(3, 4)],
            "answer": 1,
        },
        {
            "question": "Quelle écriture décimale correspond à la fraction suivante ?\n" + indent_block(format_fraction(37, 100), "    "),
            "choices": ["0,037", "3,7", "0,37"],
            "answer": 2,
        },
        {
            "question": "Comment lire 2,405 ?",
            "choices": ["Deux unités et quatre centièmes", "Deux unités et quatre dixièmes et cinq millièmes", "Deux dixièmes et 405 centièmes"],
            "answer": 1,
        },
        {
            "question": "Quelle valeur représente ce nombre mixte ?\n" + indent_block(mixed_example, "    "),
            "choices": ["8,037", "8,37", "8,7"],
            "answer": 1,
        },
        {
            "question": "Quel nombre est le plus grand ?",
            "choices": ["12,03", "12,3", "12,030"],
            "answer": 1,
        },
        {
            "question": "Entre quels entiers se situe 5,62 ?",
            "choices": ["5 et 6", "4 et 5", "6 et 7"],
            "answer": 0,
        },
        {
            "question": "Quelle écriture fractionnaire correspond à 0,8 ?",
            "choices": [format_fraction(8, 1), format_fraction(8, 10), format_fraction(80, 10)],
            "answer": 1,
        },
        {
            "question": "Quel est l'arrondi de 9,748 au dixième ?",
            "choices": ["9,7", "9,8", "9,74"],
            "answer": 1,
        },
        {
            "question": "Quelle comparaison est vraie ?",
            "choices": ["4,09 > 4,9", "6,105 < 6,15", "7,2 = 7,20"],
            "answer": 2,
        },
        {
            "question": "Quel pourcentage correspond à 0,25 ?",
            "choices": ["2,5 %", "25 %", "0,25 %"],
            "answer": 1,
        },
        {
            "question": "Complète l'encadrement : 3,501 < ? < 3,51",
            "choices": ["3,5", "3,509", "3,49"],
            "answer": 1,
        },
        {
            "question": "Comment passer de 0,07 à une fraction décimale ?",
            "choices": ["Écrire 7/10", "Écrire 7/100", "Écrire 0,7/10"],
            "answer": 1,
        },
        {
            "question": "Quel rang observe-t-on pour arrondir 4,375 au centième ?",
            "choices": ["Le millième", "Le dixième", "Le pourcentage"],
            "answer": 0,
        },
        {
            "question": "Que signifie encadrer un nombre décimal ?",
            "choices": ["Trouver deux entiers consécutifs", "Trouver deux nombres entre lesquels il se situe", "Le transformer en fraction"],
            "answer": 1,
        },
        {
            "question": "Quel est le chiffre des millièmes dans 2,408 ?",
            "choices": ["2", "4", "8"],
            "answer": 2,
        },
        {
            "question": "Quelle fraction est équivalente à 75 % ?",
            "choices": [format_fraction(75, 10), format_fraction(3, 4), format_fraction(75, 1)],
            "answer": 1,
        },
        {
            "question": "Comment placer 1,2 sur une droite graduée entre 1 et 2 ?",
            "choices": ["Au premier centième après 1", "Au deuxième dixième après 1", "Au milieu exact"],
            "answer": 1,
        },
    ]

    print(
        "Quiz : réponds à chaque question en choisissant la lettre de la bonne réponse (a, b, c...)\n"
        "Astuce : utilise les flèches pour naviguer entre les propositions ou tape directement la lettre."
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

        student, option_letters = ask_choice_with_navigation(q["choices"])
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
        print(f"{GREEN}Bravo ! Tu maîtrises les nombres entiers et décimaux. 🥳{RESET}")
    elif score >= total * 0.6:
        print(f"{CYAN}Beau travail ! Quelques révisions et ce sera parfait. 👍{RESET}")
    else:
        print(f"{RED}Courage, relis la leçon et réessaie ! 💪{RESET}")
    log_result("math_nombres_entiers_et_decimaux", score / total * 100)
