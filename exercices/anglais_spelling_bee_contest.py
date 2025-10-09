"""Quiz inspiré de l'affiche "Spelling Bee Contest"."""

from __future__ import annotations

# Nom lisible de l'exercice pour le menu principal
DISPLAY_NAME = "Anglais : Spelling Bee Contest"

import random

from .utils import show_lesson
from .logger import log_result

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main() -> None:
    """Affiche la leçon bilingue et un quiz de conversation."""

    lesson = f"""{CYAN}{BOLD}📜  Spelling Bee Contest - Preparing an Interview  📜{RESET}

{BOLD}Goal — Objectif :{RESET}
Understand how to introduce yourself during a spelling bee registration interview. — Comprendre comment te présenter lors d'un entretien d'inscription au concours d'orthographe.

{BOLD}Key ideas — Idées clés :{RESET}
• The examiner asks questions in English; prepare short answers. — L'examinateur pose des questions en anglais ; prépare des réponses courtes.
• Give clear information: name, age, hometown, family, pets and favourites. — Donne des informations claires : nom, âge, ville, famille, animaux et préférences.
• Practise both roles: answering and asking the questions back. — Entraîne-toi dans les deux rôles : répondre et poser les questions à ton tour.

{BOLD}Useful phrases — Expressions utiles :{RESET}
• "My name is…" — « Je m'appelle… »
• "I am … years old." — « J'ai … ans. »
• "I live in…" — « J'habite à… »
• "I have … brothers / sisters." — « J'ai … frères / sœurs. »
• "I have … pets." — « J'ai … animaux de compagnie. »
• "My favourite colour is…" — « Ma couleur préférée est… »
• "My favourite animal is…" — « Mon animal préféré est… »
• "I don't have a phone." — « Je n'ai pas de téléphone. »

Take a deep breath and speak slowly for clear pronunciation. — Respire profondément et parle lentement pour une prononciation claire.
"""
    show_lesson(lesson)

    examiner_questions = [
        {
            "prompt": "I'm the examiner – what's your name?",
            "options": [
                "Diane",
                "Bookcase",
                "Greenland",
            ],
            "answer": 0,
        },
        {
            "prompt": "Do you have pets?",
            "options": [
                "Yes, a dragon",
                "Possibly on Sundays",
                "Two cats",
            ],
            "answer": 2,
        },
        {
            "prompt": "What's your favourite colour?",
            "options": [
                "Chair",
                "The television",
                "Blue",
            ],
            "answer": 2,
        },
        {
            "prompt": "How old are you?",
            "options": [
                "Eleven",
                "Tomorrow morning",
                "October",
            ],
            "answer": 0,
        },
        {
            "prompt": "Where do you live?",
            "options": [
                "In Bellancourt",
                "In the calculator",
                "In Monday",
            ],
            "answer": 0,
        },
    ]

    candidate_prompts = [
        {
            "prompt": "Answer: Diane. Which question matches this answer?",
            "options": [
                "What's your favourite animal?",
                "What's your name?",
                "Do you have a phone?",
            ],
            "answer": 1,
        },
        {
            "prompt": "Answer: Eleven. Which question matches this answer?",
            "options": [
                "How old are you?",
                "Where do you live?",
                "How many pets do you have?",
            ],
            "answer": 0,
        },
        {
            "prompt": "Answer: In Bellancourt. Which question matches this answer?",
            "options": [
                "Where do you live?",
                "What's your favourite colour?",
                "Do you have a phone?",
            ],
            "answer": 0,
        },
        {
            "prompt": "Answer: I have one sister. Which question matches this answer?",
            "options": [
                "How many sisters do you have?",
                "What's your favourite animal?",
                "Do you have pets?",
            ],
            "answer": 0,
        },
        {
            "prompt": "Answer: Two cats. Which question matches this answer?",
            "options": [
                "Do you have any pets?",
                "What's your favourite colour?",
                "Do you have a phone?",
            ],
            "answer": 0,
        },
        {
            "prompt": "Answer: Blue. Which question matches this answer?",
            "options": [
                "What's your favourite colour?",
                "What's your favourite animal?",
                "Where do you live?",
            ],
            "answer": 0,
        },
        {
            "prompt": "Answer: Lions. Which question matches this answer?",
            "options": [
                "What's your favourite animal?",
                "What's your name?",
                "Do you have a phone?",
            ],
            "answer": 0,
        },
        {
            "prompt": "Answer: I don't have a phone. Which question matches this answer?",
            "options": [
                "Do you have a phone?",
                "How old are you?",
                "Do you have any pets?",
            ],
            "answer": 0,
        },
    ]

    print(f"\n{BOLD}Part 1 – Answer the examiner{RESET}")
    score = run_quiz(examiner_questions)

    print(f"\n{BOLD}Part 2 – Become the examiner{RESET}")
    score += run_quiz(candidate_prompts)

    total = len(examiner_questions) + len(candidate_prompts)
    print(f"\n{BOLD}Final score: {score}/{total}{RESET}")
    percentage = score / total * 100
    if score == total:
        print(f"{GREEN}Excellent! You handled both roles perfectly. 🥳{RESET}")
    elif score >= total / 2:
        print(f"{CYAN}Great effort! Keep practising the dialogue. 👍{RESET}")
    else:
        print(f"{RED}Review the phrases and try again. 💪{RESET}")

    log_result("anglais_spelling_bee_contest", percentage)


def run_quiz(questions: list[dict[str, object]]) -> int:
    """Run a multiple-choice quiz section and return the number of correct answers."""

    random.shuffle(questions)
    score = 0

    for idx, question in enumerate(questions, start=1):
        prompt = question["prompt"]
        options = list(question["options"])
        answer_index = question["answer"]

        print(f"\n{BOLD}Question {idx}:{RESET} {prompt}")

        labelled: list[tuple[str, str]] = []
        random.shuffle(options)
        for option_idx, option in enumerate(options):
            label = chr(ord("A") + option_idx)
            labelled.append((label, option))
            print(f"  {label}. {option}")

        correct_option = question["options"][answer_index]
        correct_letter = next(label for label, option in labelled if option == correct_option)

        while True:
            reply = input("Your answer (A, B, C…): ").strip().upper()
            if any(reply == label for label, _ in labelled):
                break
            print("Choose one of the letters shown.")

        if reply == correct_letter:
            print(f"{GREEN}Correct! ✅{RESET}")
            score += 1
        else:
            print(f"{RED}Not quite. The right answer was {correct_letter}.{RESET}")

    return score


if __name__ == "__main__":
    main()
