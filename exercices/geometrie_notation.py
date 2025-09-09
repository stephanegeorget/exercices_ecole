"""Leçon et quiz sur la notation des segments, droites et demi-droites."""

# Nom lisible de l'exercice pour le menu principal
DISPLAY_NAME = "Géométrie : Notations des segments et droites"

from .utils import show_lesson
from .logger import log_result
import random

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main() -> None:
    """Affiche la leçon puis un quiz sur les notations géométriques."""

    lesson = f"""
{CYAN}{BOLD}📏  Notation des segments, droites et demi-droites  📏{RESET}

Un {BOLD}segment [AB]{RESET} relie deux points :
x───────x
A       B

Une {BOLD}droite (AB){RESET} s'étend des deux côtés :
───x───────x───
    A       B

Une {BOLD}demi-droite [AB){RESET} a une origine A et passe par B :
x───────x───────
A       B

Exemple d'intersection :
        C
        x
        │
<───x───x───x───>
    A   E   B
        │
        x
        D
        x────────>
        F
"""
    show_lesson(lesson)

    questions = [
        {
            "figure": """x───────x\nA       B""",
            "choices": ["[AB]", "[AB)", "(AB]"],
            "answer": 0,
        },
        {
            "figure": """───x───────x───\n    A       B""",
            "choices": ["(AB)", "[AB)", "[AB]"],
            "answer": 0,
        },
        {
            "figure": """x───────x───────\nA       B""",
            "choices": ["[AB)", "(AB)", "(AB]"],
            "answer": 0,
        },
        {
            "figure": """───x───────x───\n   B       A""",
            "choices": ["(BA)", "[BA)", "[BA]"],
            "answer": 0,
        },
        {
            "figure": """x───────x───────x\nA       B       C""",
            "choices": ["[AC]", "(BC)", "[AB)"],
            "answer": 0,
        },
        {
            "figure": """x───────x───────\nB       A""",
            "choices": ["[BA)", "(BA)", "(BA]"],
            "answer": 0,
        },
        {
            "figure": """───x───────x───\n   C       D""",
            "choices": ["(CD)", "[CD]", "[CD)"],
            "answer": 0,
        },
        {
            "figure": """x───────x\nB       D""",
            "choices": ["[BD]", "[BD)", "(BD)"],
            "answer": 0,
        },
        {
            "figure": """x A\n│\n│\nx────────────x────────\nB            C""",
            "choices": ["[AB] et [BC)", "(AB) et (BC)", "(AB) et [BC)"],
            "answer": 0,
        },
        {
            "figure": """      x C\n      │\n◄─────x─────x─────►\n      B     D\n      │\n      x E""",
            "choices": ["(BD) et [CE]", "[BD] et [CE)", "(BD) et (CE]"],
            "answer": 0,
        },
    ]

    # Shuffle answer order for each question
    for q in questions:
        correct_choice = q["choices"][q["answer"]]
        random.shuffle(q["choices"])
        q["answer"] = q["choices"].index(correct_choice)

    print("Quiz : quelle est la bonne notation ?")
    score = 0
    for i, q in enumerate(questions, start=1):
        print(f"\nQuestion {i} :")
        print(q["figure"])
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
    log_result("geometrie_notation", score / total * 100)


if __name__ == "__main__":
    main()
