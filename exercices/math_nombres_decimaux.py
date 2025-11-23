"""Leçon et quiz sur les fractions et nombres décimaux."""

import textwrap

DISPLAY_NAME = "Maths : Fractions et nombres décimaux"

from .utils import ask_choice_with_navigation, format_fraction, show_lesson
from .logger import log_result

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main() -> None:
    """Affiche la leçon inspirée des documents fournis puis un quiz de 35 questions."""

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
            "question": "Quand une fraction est-elle supérieure à 1 ?",
            "choices": [
                "Quand les deux sont égaux",
                "Quand le numérateur est supérieur au dénominateur",
                "Quand le dénominateur est supérieur",
            ],
            "answer": 1,
        },
        {
            "question": "Quelle condition rend une fraction décimale ?",
            "choices": [
                "Un numérateur pair obligatoire",
                "Un dénominateur égal à 1, 10, 100, 1000...",
                "Un dénominateur toujours impair",
            ],
            "answer": 1,
        },
        {
            "question": "Comment additionner des fractions décimales de même dénominateur ?",
            "choices": [
                "On additionne les dénominateurs",
                "On multiplie numérateurs et dénominateurs",
                "On additionne les numérateurs et on garde le dénominateur",
            ],
            "answer": 2,
        },
        {
            "question": "Comment écrire le pourcentage a % en fraction ?",
            "choices": [
                "100/a",
                "a/10",
                "a/100",
            ],
            "answer": 2,
        },
        {
            "question": "Quelle affirmation décrit un nombre décimal ?",
            "choices": [
                "Il est toujours entier",
                "Il peut s'écrire comme une fraction décimale",
                "Il ne peut jamais s'écrire en fraction",
            ],
            "answer": 1,
        },
        {
            "question": "Comment appelle-t-on l'écriture d'un nombre décimal avec une virgule ?",
            "choices": [
                "Écriture fractionnaire",
                "Écriture scientifique",
                "Écriture décimale",
            ],
            "answer": 2,
        },
        {
            "question": "Qu'est-ce qu'un nombre mixte ?",
            "choices": [
                "Une fraction dont le dénominateur est 1",
                "Somme d'un entier et d'une fraction inférieure à 1",
                "Un entier négatif",
            ],
            "answer": 1,
        },
        {
            "question": "Que signifie comparer deux nombres ?",
            "choices": [
                "Les multiplier",
                "Dire s'ils sont égaux ou lequel est plus grand",
                "Les additionner",
            ],
            "answer": 1,
        },
        {
            "question": "Quelles étapes suivent-on pour comparer deux décimaux ?",
            "choices": [
                "Comparer uniquement le dernier chiffre",
                "Comparer seulement les parties entières",
                "Comparer la partie entière puis les dixièmes, centièmes...",
            ],
            "answer": 2,
        },
        {
            "question": "Que signifie encadrer ou intercaler un nombre ?",
            "choices": [
                "Arrondir au plus proche entier",
                "Diviser par 10",
                "Trouver deux nombres de part et d'autre ou un nombre entre deux",
            ],
            "answer": 2,
        },
        {
            "question": "Qu'est-ce qu'une valeur arrondie d'un décimal ?",
            "choices": [
                "La valeur exacte de la fraction",
                "Toujours la partie entière",
                "Le nombre (entier, ou avec 1 ou 2 décimales) le plus proche",
            ],
            "answer": 2,
        },
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
            "question": "Que sépare la virgule dans une écriture décimale ?",
            "choices": [
                "Le numérateur et le dénominateur",
                "La partie entière et la partie décimale",
                "Deux nombres sans lien",
            ],
            "answer": 1,
        },
        {
            "question": "À quoi sert le tableau de numération décimale ?",
            "choices": [
                "Ajouter deux fractions",
                "Repérer unités, dixièmes, centièmes, etc.",
                "Ranger uniquement les entiers pairs",
            ],
            "answer": 1,
        },
        {
            "question": "Quelle partie d'un nombre décimal se trouve avant la virgule ?",
            "choices": ["La partie entière", "La partie décimale", "La partie négative"],
            "answer": 0,
        },
        {
            "question": "Laquelle de ces fractions est décimale ?",
            "choices": [
                format_fraction(7, 25),
                format_fraction(18, 100),
                format_fraction(5, 3),
            ],
            "answer": 1,
        },
        {
            "question": "Quelle fraction décimale représente 45 % ?",
            "choices": [
                format_fraction(45, 100),
                format_fraction(45, 10),
                format_fraction(45, 1000),
            ],
            "answer": 0,
        },
        {
            "question": f"Quel est le résultat de cette fraction en nombre mixte ?\n{indent_block(format_fraction(5, 4), '    ')}",
            "choices": [
                format_fraction(1, 4, prefix="1 + "),
                format_fraction(1, 5, prefix="4 + "),
                format_fraction(4, 5, prefix="1 + "),
            ],
            "answer": 0,
        },
        {
            "question": (
                "Comment additionner ces fractions décimales ?\n"
                f"{indent_block(format_fraction(3, 10, suffix='  +'), '    ')}\n"
                f"{indent_block(format_fraction(4, 10), '    ')}"
            ),
            "choices": [
                "On additionne les numérateurs et on garde 10",
                "On additionne les dénominateurs",
                "On multiplie tout",
            ],
            "answer": 0,
        },
        {
            "question": f"Quel pourcentage équivaut à cette fraction ?\n{indent_block(format_fraction(3, 4), '    ')}",
            "choices": ["25 %", "50 %", "75 %"],
            "answer": 2,
        },
        {
            "question": f"Quelle est l'écriture décimale de la fraction suivante ?\n{indent_block(format_fraction(128, 100), '    ')}",
            "choices": ["1,28", "12,8", "0,128"],
            "answer": 0,
        },
        {
            "question": "Quel est le chiffre des centièmes dans 3,415 ?",
            "choices": ["4", "1", "5"],
            "answer": 1,
        },
        {
            "question": "Dans le tableau de numération, quelle colonne vient après les dixièmes ?",
            "choices": ["Les centièmes", "Les unités", "Les millièmes"],
            "answer": 0,
        },
        {
            "question": "Comment écrire 2,45 sous forme de nombre mixte ?",
            "choices": [
                format_fraction(45, 10, prefix="2 + "),
                format_fraction(45, 100, prefix="2 + "),
                format_fraction(4, 5, prefix="2 + "),
            ],
            "answer": 1,
        },
        {
            "question": "Entre quels nombres au centième se situe 3,538 ?",
            "choices": ["3,53 et 3,54", "3,5 et 3,6", "3,30 et 3,60"],
            "answer": 0,
        },
        {
            "question": "Lequel est le plus grand : 6,915 ou 6,92 ?",
            "choices": ["6,915", "6,92", "Ils sont égaux"],
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
            "choices": ["3,7", "37", "3,07"],
            "answer": 0,
        },
        {
            "question": "Laquelle de ces comparaisons est vraie ?",
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
            "answer": 1,
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
            "question": f"Quelle est l'écriture décimale de la fraction suivante ?\n{indent_block(format_fraction(3, 20), '    ')}",
            "choices": ["0,15", "0,3", "0,25"],
            "answer": 0,
        },
        {
            "question": f"Quel nombre décimal correspond à ce nombre mixte ?\n{indent_block(format_fraction(56, 100, prefix='4 + '), '    ')}",
            "choices": ["4,56", "4,056", "4,65"],
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
        print(f"{GREEN}Bravo ! Tu maîtrises parfaitement les nombres décimaux. 🥳{RESET}")
    elif score >= total * 0.6:
        print(f"{CYAN}Bon travail ! Continue à t'entraîner pour progresser encore. 👍{RESET}")
    else:
        print(f"{RED}Courage, relis la leçon et réessaie ! 💪{RESET}")
    log_result("math_nombres_decimaux", score / total * 100)


if __name__ == "__main__":
    main()
