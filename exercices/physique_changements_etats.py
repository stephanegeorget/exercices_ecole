"""Leçon et quiz sur les changements d'état de la matière."""

from .utils import scroll_text, wait_for_letter


GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main() -> None:
    """Présente la leçon puis un quiz corrigé."""

    lesson = f"""
{CYAN}{BOLD}🌡️  Changements d'état de la matière  🌡️{RESET}

1. ❄️  {BOLD}Fusion{RESET}            →  solide  →  liquide
   Exemple : la glace qui devient de l'eau.

2. 🧊  {BOLD}Solidification{RESET}    →  liquide  →  solide
   Exemple : l'eau qui gèle dans le congélateur.

3. 💧  {BOLD}Vaporisation{RESET}      →  liquide  →  gaz
   Exemple : l'eau qui bout devient de la vapeur.

4. ☁️  {BOLD}Condensation{RESET}      →  gaz     →  liquide
   Exemple : la vapeur d'eau qui forme des gouttes sur une vitre froide.

5. 🎈  {BOLD}Sublimation{RESET}       →  solide  →  gaz
   Exemple : la glace sèche qui disparaît en fumée.

6. ✨  {BOLD}Condensation solide{RESET} →  gaz     →  solide
   Exemple : le givre qui se forme sur une fenêtre en hiver.
"""

    scroll_text(lesson)
    wait_for_letter("q", "Tape 'q' pour passer au quiz : ")

    # Définition des questions du quiz
    questions = [
        {
            "question": "Le passage de l'état solide à l'état liquide s'appelle...",
            "choices": ["la fusion", "la solidification", "la vaporisation"],
            "answer": 0,
        },
        {
            "question": "Le passage de l'état liquide à l'état solide s'appelle...",
            "choices": ["la fusion", "la condensation", "la solidification"],
            "answer": 2,
        },
        {
            "question": "Le passage de l'état liquide à l'état gazeux s'appelle...",
            "choices": ["la sublimation", "la vaporisation", "la condensation"],
            "answer": 1,
        },
        {
            "question": "Le passage de l'état gazeux à l'état liquide s'appelle...",
            "choices": ["la condensation", "la solidification", "la fusion"],
            "answer": 0,
        },
        {
            "question": "Le passage direct du solide au gaz s'appelle...",
            "choices": ["la condensation", "la vaporisation", "la sublimation"],
            "answer": 2,
        },
        {
            "question": "Le passage direct du gaz au solide s'appelle...",
            "choices": ["la fusion", "la condensation solide", "la sublimation"],
            "answer": 1,
        },
        {
            "question": "La glace qui fond dans un verre d'eau est un exemple de...",
            "choices": ["fusion", "condensation solide", "vaporisation"],
            "answer": 0,
        },
        {
            "question": "La buée qui se forme sur un miroir après une douche est due à...",
            "choices": ["la condensation", "la sublimation", "la fusion"],
            "answer": 0,
        },
        {
            "question": "Quand on met de l'eau au congélateur, l'eau subit...",
            "choices": ["la vaporisation", "la solidification", "la sublimation"],
            "answer": 1,
        },
        {
            "question": "La formation de givre sur un pare-brise par temps froid est un exemple de...",
            "choices": ["condensation solide", "vaporisation", "fusion", "condensation"],
            "answer": 0,
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
        print(f"{GREEN}Excellent travail ! Tu maîtrises parfaitement les changements d'état. 🥳{RESET}")
    elif score >= total / 2:
        print(f"{CYAN}Bravo ! Continue à réviser pour progresser encore. 👍{RESET}")
    else:
        print(f"{RED}Courage, relis la leçon et essaie à nouveau ! 💪{RESET}")


if __name__ == "__main__":
    main()
