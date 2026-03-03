"""Exercices guidés (2, 3 et 4) autour des multiplications par 10, 100 et 1 000."""

from .logger import log_result
from .utils import ask_choice_with_navigation, show_lesson

DISPLAY_NAME = "Maths : Exercices 2-3-4 guidés (raisonnement pas à pas)"

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main() -> None:
    """Affiche un rappel puis un quiz guidé sur les exercices 2, 3 et 4."""

    lesson = f"""
{CYAN}{BOLD}Exercices 2, 3 et 4 : méthode de raisonnement pas à pas{RESET}

Tu vas refaire les exercices de la fiche (2, 3 et 4), mais sous forme de quiz.
Chaque petite étape du raisonnement devient une question.

{BOLD}Méthode générale utilisée{RESET}
1. Identifier les données importantes (quantité, prix unitaire).
2. Repérer les multiplications par 10, 100 ou 1 000.
3. Déplacer la virgule correctement :
   - ×10 : 1 rang vers la droite
   - ×100 : 2 rangs vers la droite
   - ×1 000 : 3 rangs vers la droite
4. Calculer chaque recette partielle.
5. Additionner les recettes partielles pour obtenir la recette totale.

{BOLD}Exercice 2 (concert){RESET}
- Catégorie A : 100 places à 63,50 €
- Catégorie B : 1 000 places à 42,30 €

{BOLD}Exercice 3 (produits en ligne){RESET}
- a) 12,753 × 100
- b) 0,435 × 1 000
- c) 2,714 × 10 × 100
- d) 14,203 × 100 × 100

{BOLD}Exercice 4 (boutique de football){RESET}
- 1 000 maillots à 87,99 €
- 100 équipements à 143,40 €

Prêt ? On déroule le raisonnement étape par étape.
"""

    show_lesson(lesson)

    questions = [
        # Exercice 2 (5 questions)
        {
            "question": "[Exercice 2] Pour calculer une recette, quelle opération relie le nombre de places et le prix d'une place ?",
            "choices": [
                "Une addition (quantité + prix)",
                "Une multiplication (quantité × prix)",
                "Une soustraction (quantité - prix)",
            ],
            "answer": 1,
        },
        {
            "question": "[Exercice 2] Pourquoi, pour la catégorie A (100 places à 63,50 €), choisit-on 100 × 63,50 ?",
            "choices": [
                "Parce qu'on additionne 63,50 € cent fois, donc c'est une multiplication",
                "Parce que 100 est plus grand que 63,50",
                "Parce qu'on doit d'abord diviser par 100",
            ],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] Quel est le résultat de 100 × 63,50 ?",
            "choices": ["635 €", "6 350 €", "63 500 €"],
            "answer": 1,
        },
        {
            "question": "[Exercice 2] Quel est le résultat de 1 000 × 42,30 pour la catégorie B ?",
            "choices": ["4 230 €", "42 300 €", "423 000 €"],
            "answer": 1,
        },
        {
            "question": "[Exercice 2] Recette totale du concert : 6 350 + 42 300 = ?",
            "choices": ["48 650 €", "49 650 €", "50 650 €"],
            "answer": 0,
        },

        # Exercice 3 (5 questions)
        {
            "question": "[Exercice 3] Rappel : multiplier par 100 revient à déplacer la virgule de...",
            "choices": ["1 rang vers la droite", "2 rangs vers la droite", "3 rangs vers la droite"],
            "answer": 1,
        },
        {
            "question": "[Exercice 3a] 12,753 × 100 =",
            "choices": ["127,53", "1 275,3", "12 753"],
            "answer": 1,
        },
        {
            "question": "[Exercice 3b] 0,435 × 1 000 =",
            "choices": ["4,35", "43,5", "435"],
            "answer": 2,
        },
        {
            "question": "[Exercice 3c] 2,714 × 10 × 100 : quel facteur global utilise-t-on ?",
            "choices": ["100", "1 000", "10 000"],
            "answer": 1,
        },
        {
            "question": "[Exercice 3d] 14,203 × 100 × 100 =",
            "choices": ["1 420,3", "14 203", "142 030"],
            "answer": 2,
        },

        # Exercice 4 (5 questions)
        {
            "question": "[Exercice 4] Pour 1 000 maillots à 87,99 €, quel raisonnement est correct ?",
            "choices": [
                "On additionne 87,99 € à lui-même 1 000 fois, donc on fait 1 000 × 87,99",
                "On fait 1 000 + 87,99 car il y a deux nombres",
                "On fait 87,99 ÷ 1 000 pour trouver une recette",
            ],
            "answer": 0,
        },
        {
            "question": "[Exercice 4] Recette des maillots : 1 000 × 87,99 =",
            "choices": ["8 799 €", "87 990 €", "879 900 €"],
            "answer": 1,
        },
        {
            "question": "[Exercice 4] Pour 100 équipements à 143,40 €, quelle opération choisir ?",
            "choices": ["100 × 143,40", "100 + 143,40", "143,40 ÷ 100"],
            "answer": 0,
        },
        {
            "question": "[Exercice 4] Recette des équipements : 100 × 143,40 =",
            "choices": ["1 434 €", "14 340 €", "143 400 €"],
            "answer": 1,
        },
        {
            "question": "[Exercice 4] Recette totale de la boutique : 87 990 + 14 340 = ?",
            "choices": ["101 330 €", "102 330 €", "103 330 €"],
            "answer": 1,
        },
    ]

    print(
        "Quiz guidé : réponds avec la lettre (a, b, c...). "
        "Tu peux utiliser les flèches pour naviguer. Tape 'q' pour quitter."
    )

    score = 0
    for i, q in enumerate(questions, start=1):
        print(f"\nQuestion {i}: {q['question']}")
        student, option_letters, quit_requested = ask_choice_with_navigation(q["choices"])
        if quit_requested:
            print("\nFin du quiz demandée. Retour au menu.\n")
            return

        correct = q["answer"]
        if student == correct:
            print(f"{GREEN}Exact ! ✅{RESET}")
            score += 1
        else:
            correct_letter = option_letters[correct]
            correct_text = q["choices"][correct]
            print(f"{RED}Incorrect. Bonne réponse : {correct_letter}) {correct_text} ❌{RESET}")

    total = len(questions)
    print(f"\n{BOLD}Score final : {score}/{total}{RESET}")
    if score == total:
        print(f"{GREEN}Parfait ! Tu maîtrises le raisonnement pas à pas. 🥳{RESET}")
    elif score >= total * 0.6:
        print(f"{CYAN}Très bien ! Continue à détailler chaque étape. 👍{RESET}")
    else:
        print(f"{RED}Relis la méthode et recommence : chaque étape compte. 💪{RESET}")

    log_result("math_exercices_2_3_4_recettes", score / total * 100)


if __name__ == "__main__":
    main()
