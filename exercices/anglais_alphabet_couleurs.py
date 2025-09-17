"""Leçon et exercices sur l'alphabet, les couleurs et la présentation en anglais."""

# Nom lisible de l'exercice pour le menu principal
DISPLAY_NAME = "Anglais : Alphabet et présentation"

import random
from textwrap import dedent

from .utils import show_lesson
from .logger import log_result

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

ALPHABET_CLUES: list[tuple[str, str]] = [
    ("A", "se prononce /eɪ/ comme la fin du mot 'day'"),
    ("B", "sonne comme 'bee', une abeille"),
    ("C", "se dit /siː/ comme dans 'see'"),
    ("D", "sonne comme 'dee'"),
    ("E", "est /iː/ comme dans 'tree'"),
    ("F", "fait un son bref /ɛf/"),
    ("G", "se prononce /dʒiː/ comme 'jee'"),
    ("H", "commence par un souffle: /eɪtʃ/"),
    ("I", "ressemble à 'eye'"),
    ("J", "sonne comme 'jay'"),
    ("K", "est /keɪ/, comme dans 'okay'"),
    ("L", "est bref: /ɛl/"),
    ("M", "est bref: /ɛm/"),
    ("N", "est bref: /ɛn/"),
    ("O", "ressemble à 'oh'"),
    ("P", "est /piː/ comme 'pea'"),
    ("Q", "se prononce /kjuː/ comme 'queue'"),
    ("R", "est /ɑːr/, on entend 'ar'"),
    ("S", "fait /ɛs/"),
    ("T", "sonne comme 'tee'"),
    ("U", "est /juː/, comme 'you'"),
    ("V", "se dit /viː/, comme 'vee'"),
    ("W", "se prononce 'double you'"),
    ("X", "fait /ɛks/"),
    ("Y", "sonne comme 'why'"),
    ("Z", "en anglais britannique 'zed', en américain 'zee'"),
]

COLORS_FR_EN: dict[str, list[str]] = {
    "rouge": ["red"],
    "bleu": ["blue"],
    "vert": ["green"],
    "jaune": ["yellow"],
    "noir": ["black"],
    "blanc": ["white"],
    "orange": ["orange"],
    "rose": ["pink"],
    "violet": ["purple", "violet"],
    "marron": ["brown"],
    "gris": ["grey", "gray"],
}


PERSONAL_QUESTIONS: list[tuple[str, str]] = [
    ("What is your name?", "name"),
    ("How old are you?", "age"),
    ("Where do you live?", "city"),
    ("What is your favourite colour?", "favorite_colour"),
]

FORM_FIELDS: list[tuple[str, str]] = [
    ("First name", "first_name"),
    ("Last name", "last_name"),
    ("Age", "age"),
    ("City", "city"),
    ("Email", "email"),
]


def show_intro_lesson() -> None:
    """Display the lesson recap before the interactive activities."""

    lesson = dedent(
        f"""
        {CYAN}{BOLD}🎧 Alphabet, couleurs et présentation en anglais{RESET}

        Objectifs du jour :
        • Comprendre les lettres de l'alphabet à l'oral.
        • Écrire les couleurs en anglais sans erreur.
        • Répondre à des questions de présentation (nom, âge, ville, couleur préférée).
        • Renseigner un questionnaire simple.

        {BOLD}1. Alphabet à l'oral{RESET}
        Concentre-toi sur le son de chaque lettre :
        - A /eɪ/ → comme "day".
        - H /eɪtʃ/ → souffle initial.
        - W → "double you" (deux sons !).
        Astuce : répète les paires (A-E, I-Y, O-U) qui se ressemblent pour ne plus les confondre.

        {BOLD}2. Couleurs en anglais{RESET}
        Rouge → red • Bleu → blue • Vert → green • Jaune → yellow
        Noir → black • Blanc → white • Violet → purple • Marron → brown • Gris → grey/gray.
        Astuce : écris chaque mot deux fois à voix haute pour mémoriser l'orthographe.

        {BOLD}3. Se présenter{RESET}
        "My name is ..." • "I am ... years old." • "I live in ..." • "My favourite colour is ..."
        Pense à commencer les phrases par une majuscule et terminer par un point.

        {BOLD}4. Remplir un formulaire{RESET}
        Lis bien chaque question et réponds en anglais complet.
        Exemple : First name → "Emma", City → "Paris".

        Quand tu es prêt·e, passe au quiz !
        """
    )
    show_lesson(lesson)


def alphabet_quiz(num_questions: int = 8) -> tuple[int, int]:
    """Quiz that asks for letters based on oral-style clues."""

    print(f"{BOLD}🅰️ Exercice 1 : devine la lettre à partir de la description orale{RESET}")
    questions = random.sample(ALPHABET_CLUES, k=min(num_questions, len(ALPHABET_CLUES)))
    score = 0
    for letter, clue in questions:
        answer = input(f"Quelle lettre correspond à cette description → {clue} ? ").strip().upper()
        if answer == letter:
            print(f"{GREEN}Yes! C'était bien la lettre {letter}.{RESET}")
            score += 1
        else:
            print(f"{RED}Presque ! La bonne réponse était {letter}.{RESET}")
    total = len(questions)
    print(f"Tu as obtenu {score}/{total} pour l'alphabet.\n")
    return score, total


def colors_quiz() -> tuple[int, int]:
    """Quiz that checks the spelling of colour names."""

    print(f"{BOLD}🎨 Exercice 2 : écris la couleur en anglais{RESET}")
    items = list(COLORS_FR_EN.items())
    random.shuffle(items)
    score = 0
    for french, answers in items:
        reply = input(f"Comment écrit-on la couleur « {french} » en anglais ? ").strip().lower()
        if reply in answers:
            print(f"{GREEN}Parfait, {reply} est correct !{RESET}")
            score += 1
        else:
            solutions = ", ".join(answers)
            print(f"{RED}Attention, on écrit {solutions}.{RESET}")
    total = len(items)
    print(f"Résultat : {score}/{total} pour les couleurs.\n")
    return score, total


def personal_questions() -> dict[str, str]:
    """Ask the learner personal questions in English."""

    print(f"{BOLD}🧍‍♀️ Exercice 3 : réponds aux questions sur toi{RESET}")
    responses: dict[str, str] = {}
    for question, key in PERSONAL_QUESTIONS:
        responses[key] = input(f"{question} ").strip()
    print("Merci ! Continue avec le questionnaire.\n")
    return responses


def fill_form() -> dict[str, str]:
    """Collect information as if filling a basic form."""

    print(f"{BOLD}📄 Exercice 4 : remplis le mini-formulaire en anglais{RESET}")
    filled: dict[str, str] = {}
    for label, key in FORM_FIELDS:
        filled[key] = input(f"{label}: ").strip()
    print("\nFormulaire complété, bravo !\n")
    return filled


def main() -> None:
    """Run the lesson followed by the four activities."""

    show_intro_lesson()
    letter_score, letter_total = alphabet_quiz()
    colour_score, colour_total = colors_quiz()
    personal_answers = personal_questions()
    form_answers = fill_form()

    total_points = letter_total + colour_total
    score_points = letter_score + colour_score
    final_percentage = (score_points / total_points * 100) if total_points else 0.0

    print(f"{CYAN}{BOLD}Récapitulatif :{RESET}")
    print(f"Alphabet : {letter_score}/{letter_total}")
    print(f"Couleurs : {colour_score}/{colour_total}")
    print("Tes réponses personnelles :")
    for key, value in personal_answers.items():
        print(f"  - {key.replace('_', ' ').title()} : {value}")
    print("Formulaire :")
    for key, value in form_answers.items():
        print(f"  - {key.replace('_', ' ').title()} : {value}")

    if final_percentage == 100:
        message = "Superbe travail, tout est parfait !"
    elif final_percentage >= 70:
        message = "Très bien ! Encore un peu de pratique et tu seras au top."
    else:
        message = "Courage, relis la leçon et recommence pour progresser."
    print(f"\n{BOLD}{message}{RESET}")

    log_result("anglais_alphabet_presentation", final_percentage)


if __name__ == "__main__":
    main()
