"""Leçon et quiz sur la notation des segments, droites et demi-droites."""

from .utils import show_lesson
from .logger import log_result

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
*-------*
A       B

Une {BOLD}droite (AB){RESET} s'étend des deux côtés :
----*-------*----
    A       B

Une {BOLD}demi-droite [AB){RESET} a une origine A et passe par B :
*-------*-------
A       B

Exemple d'intersection :
        C
        *
        |
<---*---*---*--->
    A   E   B
        |
        *
        D
        *--------->
        F
"""
    show_lesson(lesson)

    questions = [
        {
            "figure": """*-------*\nA       B""",
            "choices": ["[AB]", "[AB)", "(AB]"],
            "answer": 0,
        },
        {
            "figure": """----*-------*----\n    A       B""",
            "choices": ["(AB)", "[AB)", "[AB]"],
            "answer": 0,
        },
        {
            "figure": """*-------*-------\nA       B""",
            "choices": ["[AB)", "(AB)", "(AB]"],
            "answer": 0,
        },
        {
            "figure": """---*-------*---\n   B       A""",
            "choices": ["(BA)", "[BA)", "[BA]"],
            "answer": 0,
        },
        {
            "figure": """*-------*-------*\nA       B       C""",
            "choices": ["[AC]", "(BC)", "[AB)"],
            "answer": 0,
        },
    ]

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
