"""Leçon et quiz sur les fractions et nombres décimaux."""

import textwrap

DISPLAY_NAME = "Maths : Fractions et nombres décimaux"

from .utils import format_fraction, show_lesson
from .logger import log_result

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main() -> None:
    """Affiche la leçon inspirée des documents fournis puis un quiz de 40 questions."""

    def indent_block(text: str, prefix: str = "  ") -> str:
        return textwrap.indent(text, prefix)

    improper_fraction = format_fraction(5, 4)
    mixed_quarter = format_fraction(1, 4, prefix="1 + ")
    decimal_fraction = format_fraction(128, 100)
    mixed_number = format_fraction(45, 100, prefix="2 + ")
    decimal_part = format_fraction(45, 100)
    fraction_three_twenty = format_fraction(3, 20)

    lesson = f"""
{CYAN}{BOLD}Nombres décimaux : fractions, écriture et comparaison{RESET}

{BOLD}1) Les fractions{RESET}
- On partage une unité en parts égales : chaque part est une fraction de l'unité.
- Le {BOLD}numérateur{RESET} indique combien de parts on prend.
- Le {BOLD}dénominateur{RESET} indique en combien de parts égales l'unité est partagée.

{BOLD}Propriétés importantes{RESET}
• Une fraction est supérieure à 1 lorsque le numérateur est plus grand que le dénominateur.
• Une fraction décimale est une fraction dont le dénominateur est un entier et s'écrit 10, 100, 1000...
• Pour additionner ou soustraire des fractions décimales : on additionne les numérateurs et on conserve le dénominateur.
• Le pourcentage « p % » correspond à la fraction décimale p/100.

{BOLD}2) Écriture décimale{RESET}
- Un nombre décimal est un nombre qui peut s'écrire sous forme de fraction décimale.
- L'écriture d'un nombre décimal avec une virgule est appelée {BOLD}écriture décimale{RESET}.
- On repère chaque chiffre d'un nombre décimal dans le tableau de numération : unités, dixièmes, centièmes, millièmes...
- Pour passer d'un nombre décimal à un nombre mixte (partie entière + fraction), on sépare la partie entière et la partie décimale.

{BOLD}3) Comparaison et encadrement{RESET}
- Comparer deux nombres décimaux :
  1. On compare la partie entière.
  2. Si elles sont égales, on compare les chiffres décimaux dans l'ordre (dixièmes, centièmes...).
- Encadrer un nombre revient à trouver deux nombres entre lesquels il se situe, souvent au dixième ou au centième près.
- Sur une demi-droite graduée, chaque point correspond à un nombre : l'abscisse.

{BOLD}Exemples clés{RESET}
• Fraction impropre :
{indent_block(improper_fraction, "    ")}
  Ce nombre vaut aussi :
{indent_block(mixed_quarter, "    ")}
  = 1,25.

• Fraction décimale :
{indent_block(decimal_fraction, "    ")}
  correspond à 1,28 en écriture décimale.

• Nombre mixte :
{indent_block(mixed_number, "    ")}
  sépare la partie entière (2) et la partie décimale :
{indent_block(decimal_part, "    ")}
  qui vaut 0,45.

• Conversion fraction → décimal :
{indent_block(fraction_three_twenty, "    ")}
  se lit 3 ÷ 20 = 0,15.

• Comparaison :
  6,915 < 6,92 car 6 = 6 mais 0,915 < 0,92 en comparant les centièmes.
• Encadrer 3,538 au centième : 3,53 < 3,538 < 3,54.

{BOLD}Méthodes{RESET}
1. Pour passer d'une fraction décimale à une écriture à virgule : on effectue la division du numérateur par 10, 100, 1000...
2. Pour passer d'une écriture à virgule à un nombre mixte : on garde la partie entière et on transforme la partie décimale en fraction décimale simplifiée.
3. Pour comparer ou encadrer : on aligne les chiffres dans le tableau de numération et on repère la position sur la droite graduée.

Relis ces rappels, puis lance le quiz pour t'entraîner à reconnaître les définitions et à effectuer quelques calculs simples !
"""

    show_lesson(lesson)

    questions = [
        {
            "question": f"Dans la fraction suivante, quel est le numérateur ?\n{indent_block(format_fraction(3, 5), '    ')}",
            "choices": ["3", "5", "8"],
            "answer": 0,
        },
        {
            "question": f"Dans la fraction suivante, que représente le nombre 5 ?\n{indent_block(format_fraction(3, 5), '    ')}",
            "choices": ["Le dénominateur", "Le numérateur", "La somme"],
            "answer": 0,
        },
        {
            "question": "Quand une fraction est-elle supérieure à 1 ?",
            "choices": ["Quand le numérateur est plus grand que le dénominateur", "Quand les deux nombres sont égaux", "Quand le dénominateur est plus grand"],
            "answer": 0,
        },
        {
            "question": "Laquelle de ces fractions est une fraction décimale ?",
            "choices": [
                format_fraction(7, 25),
                format_fraction(18, 100),
                format_fraction(5, 3),
            ],
            "answer": 1,
        },
        {
            "question": "Quelle est la fraction décimale associée à 45 % ?",
            "choices": [
                format_fraction(45, 100),
                format_fraction(45, 10),
                format_fraction(45, 1000),
            ],
            "answer": 0,
        },
        {
            "question": f"Quel est le résultat de la fraction suivante en nombre mixte ?\n{indent_block(format_fraction(5, 4), '    ')}",
            "choices": [
                format_fraction(1, 4, prefix="1 + "),
                format_fraction(1, 5, prefix="4 + "),
                format_fraction(4, 5, prefix="1 + "),
            ],
            "answer": 0,
        },
        {
            "question": (
                "Comment additionner les fractions décimales suivantes ?\n"
                f"{indent_block(format_fraction(3, 10, suffix='  +'), '    ')}\n"
                f"{indent_block(format_fraction(4, 10), '    ')}"
            ),
            "choices": [
                "On additionne les dénominateurs",
                "On additionne les numérateurs et on garde 10",
                "On multiplie tout",
            ],
            "answer": 1,
        },
        {
            "question": f"Quel est le pourcentage équivalent à la fraction suivante ?\n{indent_block(format_fraction(3, 4), '    ')}",
            "choices": ["25 %", "50 %", "75 %"],
            "answer": 2,
        },
        {
            "question": f"Quelle est l'écriture décimale de la fraction suivante ?\n{indent_block(format_fraction(128, 100), '    ')}",
            "choices": ["1,28", "12,8", "0,128"],
            "answer": 0,
        },
        {
            "question": "Quel nom donne-t-on à l'écriture d'un nombre avec une virgule ?",
            "choices": ["Écriture fractionnaire", "Écriture décimale", "Écriture mixte"],
            "answer": 1,
        },
        {
            "question": "Quel est le chiffre des centièmes dans 3,415 ?",
            "choices": ["4", "1", "5"],
            "answer": 1,
        },
        {
            "question": "Dans le tableau de numération, quelle colonne vient juste après les dixièmes ?",
            "choices": ["Les unités", "Les centièmes", "Les millièmes"],
            "answer": 1,
        },
        {
            "question": "Comment écrire 2,45 sous forme de nombre mixte ?",
            "choices": [
                format_fraction(45, 10, prefix="2 + "),
                format_fraction(45, 100, prefix="2 + "),
                format_fraction(4, 5, prefix="2 + "),
            ],
            "answer": 2,
        },
        {
            "question": "Que signifie encadrer un nombre ?",
            "choices": ["Trouver deux nombres entre lesquels il se situe", "Arrondir au nombre entier le plus proche", "Additionner deux nombres"],
            "answer": 0,
        },
        {
            "question": "Entre quels nombres au centième se situe 3,538 ?",
            "choices": ["3,53 et 3,54", "3,5 et 3,6", "3,30 et 3,60"],
            "answer": 0,
        },
        {
            "question": "Quel est l'ordre correct de comparaison ?",
            "choices": ["Comparer les dixièmes puis les unités", "Comparer la partie entière puis les décimales", "Comparer les centièmes puis les dixièmes"],
            "answer": 1,
        },
        {
            "question": "Lequel est le plus grand : 6,915 ou 6,92 ?",
            "choices": ["6,915", "6,92", "Ils sont égaux"],
            "answer": 1,
        },
        {
            "question": "Que signifie l'abscisse d'un point sur une demi-droite graduée ?",
            "choices": ["La longueur du segment", "Le nombre associé au point", "Le nombre de graduations"],
            "answer": 1,
        },
        {
            "question": "Quelle fraction décimale correspond à 0,4 ?",
            "choices": [
                format_fraction(4, 100),
                format_fraction(4, 10),
                format_fraction(40, 1),
            ],
            "answer": 1,
        },
        {
            "question": "Quelle écriture donne 3 unités et 7 dixièmes ?",
            "choices": ["37", "3,7", "3,07"],
            "answer": 1,
        },
        {
            "question": "Quel est le résultat de 0,5 + 0,25 ?",
            "choices": ["0,75", "0,55", "0,525"],
            "answer": 0,
        },
        {
            "question": "Quel nombre est exactement au milieu entre 4,2 et 4,4 ?",
            "choices": ["4,25", "4,3", "4,35"],
            "answer": 1,
        },
        {
            "question": "Quelle comparaison est vraie ?",
            "choices": ["2,305 > 2,35", "7,08 < 7,8", "5,4 = 5,40"],
            "answer": 2,
        },
        {
            "question": "Quelle fraction décimale représente 6,07 ?",
            "choices": [
                format_fraction(607, 10),
                format_fraction(607, 100),
                format_fraction(607, 1000),
            ],
            "answer": 2,
        },
        {
            "question": f"Quelle écriture est égale à ce nombre mixte ?\n{indent_block(format_fraction(3, 10, prefix='9 + '), '    ')}",
            "choices": ["9,3", "9,03", "9,30"],
            "answer": 0,
        },
        {
            "question": "Comment écrire 0,125 sous forme de fraction décimale simplifiée ?",
            "choices": [
                format_fraction(125, 1000),
                format_fraction(1, 8),
                format_fraction(125, 100),
            ],
            "answer": 1,
        },
        {
            "question": "Quel nombre est plus petit que 5,08 ?",
            "choices": ["5,8", "5,18", "5,071"],
            "answer": 2,
        },
        {
            "question": "Entre quels entiers se situe 17,6 ?",
            "choices": ["17 et 18", "16 et 17", "18 et 19"],
            "answer": 0,
        },
        {
            "question": f"Quelle est l'écriture décimale de la fraction suivante ?\n{indent_block(format_fraction(3, 20), '    ')}",
            "choices": ["0,15", "0,3", "0,25"],
            "answer": 0,
        },
        {
            "question": "Quel pourcentage correspond à 0,62 ?",
            "choices": ["6,2 %", "62 %", "0,62 %"],
            "answer": 1,
        },
        {
            "question": "Laquelle de ces écritures représente 1 unité et 35 centièmes ?",
            "choices": ["1,035", "1,35", "135"],
            "answer": 1,
        },
        {
            "question": "Quel centième se trouve exactement au milieu de 5,4 et 5,5 ?",
            "choices": ["5,45", "5,49", "5,5"],
            "answer": 0,
        },
        {
            "question": "Quelle addition de fractions décimales est correcte ?",
            "choices": [
                (
                    f"{format_fraction(3, 100, suffix='  +')}\n"
                    f"{format_fraction(5, 100, suffix='  =')}\n"
                    f"{format_fraction(8, 10)}"
                ),
                (
                    f"{format_fraction(7, 10, suffix='  +')}\n"
                    f"{format_fraction(2, 10, suffix='  =')}\n"
                    f"{format_fraction(9, 10)}"
                ),
                (
                    f"{format_fraction(4, 10, suffix='  +')}\n"
                    f"{format_fraction(1, 10, suffix='  =')}\n"
                    f"{format_fraction(5, 100)}"
                ),
            ],
            "answer": 1,
        },
        {
            "question": "Quelle est l'écriture fractionnaire de 2,08 ?",
            "choices": [
                format_fraction(208, 10),
                format_fraction(208, 100),
                format_fraction(208, 1000),
            ],
            "answer": 2,
        },
        {
            "question": f"Quel nombre décimal correspond à ce nombre mixte ?\n{indent_block(format_fraction(56, 100, prefix='4 + '), '    ')}",
            "choices": ["4,056", "4,56", "4,65"],
            "answer": 1,
        },
        {
            "question": "Quel est le dixième le plus proche de 7,86 ?",
            "choices": ["7,8", "7,9", "8"],
            "answer": 1,
        },
        {
            "question": "Laquelle de ces inégalités est vraie ?",
            "choices": ["8,07 > 8,7", "3,402 < 3,42", "1,5 = 1,50"],
            "answer": 2,
        },
        {
            "question": "Quelle fraction décimale représente 0,03 ?",
            "choices": [
                format_fraction(3, 10),
                format_fraction(3, 100),
                format_fraction(3, 1000),
            ],
            "answer": 1,
        },
        {
            "question": "Quel est le pourcentage équivalent à 0,005 ?",
            "choices": ["0,5 %", "5 %", "0,05 %"],
            "answer": 0,
        },
        {
            "question": "Quel nombre complète 2,4 < ? < 2,5 avec un centième ?",
            "choices": ["2,44", "2,46", "2,51"],
            "answer": 1,
        },
    ]

    print("Quiz : réponds à chaque question en choisissant la lettre de la bonne réponse (a, b, c...).")
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

        option_letters = [chr(ord("a") + idx) for idx in range(len(q["choices"]))]
        for letter, choice in zip(option_letters, q["choices"]):
            choice_lines = str(choice).splitlines()
            prefix = f"  {letter}) "
            print(prefix + choice_lines[0])
            continuation = " " * len(prefix)
            for extra_line in choice_lines[1:]:
                print(f"{continuation}{extra_line}")

        student_input = input("Votre réponse (lettre) : ").strip().lower()
        student = option_letters.index(student_input) if student_input in option_letters else -1
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
        print(f"{GREEN}Bravo ! Tu maîtrises parfaitement les nombres décimaux. 🥳{RESET}")
    elif score >= total * 0.6:
        print(f"{CYAN}Bon travail ! Continue à t'entraîner pour progresser encore. 👍{RESET}")
    else:
        print(f"{RED}Courage, relis la leçon et réessaie ! 💪{RESET}")
    log_result("math_nombres_decimaux", score / total * 100)


if __name__ == "__main__":
    main()
