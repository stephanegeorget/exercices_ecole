"""Leçon et quiz sur quelques propriétés de l'eau liquide."""

# Nom lisible de l'exercice pour le menu principal
DISPLAY_NAME = "Physique : Propriétés de l'eau liquide"

from .utils import show_lesson
from .logger import log_result

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main() -> None:
    """Présente la leçon puis un quiz corrigé."""

    lesson = rf"""
{CYAN}{BOLD}Activité 2 : Quelques propriétés de l'eau liquide{RESET}

Les propriétés de la matière peuvent dépendre de l'état physique dans lequel elle se trouve.
Problématique : {BOLD}Quelles sont les propriétés de l'eau à l'état liquide ?{RESET}

Hypothèse : {BOLD}L'eau prend la forme du récipient qui la contient.{RESET}

{BOLD}1) Représenter de l'eau à l'état liquide dans chaque récipient :{RESET}
a) Bécher :
       __
      /  \
     /~~~~\
    /      \
   /________\

b) Verre à pied :
       ____
      /    \
     /~~~~~~\
     \      /
      \____/
        ||
        ||

c) Éprouvette graduée :
      ____
     |    |
     |~~~~|
     |    |
     |____|

{BOLD}Observation :{RESET} la surface de l'eau est plane, quel que soit le récipient.

{BOLD}Conclusion :{RESET}
  a) La surface de l'eau est horizontale.
  b) L'eau prend la forme du récipient qui la contient.
"""

    show_lesson(lesson)

    questions = [
        {
            "question": "Quelle est la surface de l'eau dans un récipient ?",
            "choices": ["Horizontale", "Inclinée", "Courbée"],
            "answer": 0,
        },
        {
            "question": "L'eau prend-elle la forme du récipient ?",
            "choices": ["Oui", "Non"],
            "answer": 0,
        },
        {
            "question": "Quel est l'état étudié dans cette leçon ?",
            "choices": ["Solide", "Liquide", "Gazeux"],
            "answer": 1,
        },
    ]

    print("Quiz : réponds à chaque question en choisissant le numéro de la bonne réponse.")
    score = 0
    for i, q in enumerate(questions, start=1):
        print(f"\nQuestion {i}: {q['question']}")
        for j, choice in enumerate(q["choices"], start=1):
            print(f"  {j}. {choice}")
        try:
            student = int(input("Votre réponse : ")) - 1
        except ValueError:
            student = -1
        correct = q["answer"]
        correct_text = q["choices"][correct]
        if student == correct:
            print(f"{GREEN}Exact ! ✅{RESET}")
            score += 1
        else:
            print(f"{RED}Non, la bonne réponse était {correct + 1}. {correct_text} ❌{RESET}")

    total = len(questions)
    print(f"\n{BOLD}Score final : {score}/{total}{RESET}")
    if score == total:
        print(f"{GREEN}Excellent travail ! Tu maîtrises parfaitement ces propriétés. 🥳{RESET}")
    elif score >= total / 2:
        print(f"{CYAN}Bravo ! Continue à réviser pour progresser encore. 👍{RESET}")
    else:
        print(f"{RED}Courage, relis la leçon et essaie à nouveau ! 💪{RESET}")
    log_result("physique_proprietes_eau_liquide", score / total * 100)


if __name__ == "__main__":
    main()
