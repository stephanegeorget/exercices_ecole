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
        # Exercice 2 : compréhension
        {
            "question": "[Exercice 2] Quelle opération représente la recette de la catégorie A ?",
            "choices": [
                "63,50 + 100",
                "100 × 63,50",
                "100 ÷ 63,50",
            ],
            "answer": 1,
        },
        {
            "question": "[Exercice 2] 100 × 63,50 revient à déplacer la virgule de combien de rangs ?",
            "choices": ["1 rang", "2 rangs", "3 rangs"],
            "answer": 1,
        },
        {
            "question": "[Exercice 2] Quelle est alors la recette de la catégorie A ?",
            "choices": ["635 €", "6 350 €", "63 500 €"],
            "answer": 1,
        },
        {
            "question": "[Exercice 2] Quelle opération représente la recette de la catégorie B ?",
            "choices": [
                "1 000 × 42,30",
                "42,30 ÷ 1 000",
                "1 000 + 42,30",
            ],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] Multiplier par 1 000 déplace la virgule de...",
            "choices": ["1 rang", "2 rangs", "3 rangs"],
            "answer": 2,
        },
        {
            "question": "[Exercice 2] Recette de la catégorie B :",
            "choices": ["4 230 €", "42 300 €", "423 000 €"],
            "answer": 1,
        },
        {
            "question": "[Exercice 2] Recette totale du concert : 6 350 + 42 300 = ?",
            "choices": ["48 650 €", "49 650 €", "50 650 €"],
            "answer": 0,
        },
        # Exercice 3 : produits en ligne
        {
            "question": "[Exercice 3a] 12,753 × 100 : la virgule se déplace de...",
            "choices": ["1 rang", "2 rangs", "3 rangs"],
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
            "question": "[Exercice 3c] Dans 2,714 × 10 × 100, le facteur global est...",
            "choices": ["10", "100", "1 000"],
            "answer": 2,
        },
        {
            "question": "[Exercice 3c] Donc 2,714 × 10 × 100 =",
            "choices": ["27,14", "271,4", "2 714"],
            "answer": 2,
        },
        {
            "question": "[Exercice 3d] Dans 14,203 × 100 × 100, le facteur global est...",
            "choices": ["1 000", "10 000", "100 000"],
            "answer": 1,
        },
        {
            "question": "[Exercice 3d] 14,203 × 10 000 =",
            "choices": ["142,03", "1 420,3", "142 030"],
            "answer": 2,
        },
        # Exercice 4 : boutique
        {
            "question": "[Exercice 4] Quelle opération modélise la recette des maillots ?",
            "choices": ["1 000 × 87,99", "87,99 + 1 000", "1 000 ÷ 87,99"],
            "answer": 0,
        },
        {
            "question": "[Exercice 4] Recette des maillots :",
            "choices": ["8 799 €", "87 990 €", "879 900 €"],
            "answer": 1,
        },
        {
            "question": "[Exercice 4] Quelle opération modélise la recette des équipements ?",
            "choices": ["100 × 143,40", "143,40 + 100", "143,40 ÷ 100"],
            "answer": 0,
        },
        {
            "question": "[Exercice 4] Recette des équipements :",
            "choices": ["1 434 €", "14 340 €", "143 400 €"],
            "answer": 1,
        },
        {
            "question": "[Exercice 4] Recette totale de la boutique : 87 990 + 14 340 = ?",
            "choices": ["101 330 €", "102 330 €", "103 330 €"],
            "answer": 1,
        },
        # Questions de contrôle de raisonnement
        {
            "question": "Quand on multiplie un décimal par 100, on obtient en général un nombre...",
            "choices": [
                "100 fois plus grand",
                "100 fois plus petit",
                "inchangé",
            ],
            "answer": 0,
        },
        {
            "question": "Pourquoi la méthode sans poser d'opération fonctionne ici ?",
            "choices": [
                "Parce que les facteurs sont 10, 100, 1 000 et on déplace la virgule",
                "Parce qu'on arrondit tous les prix",
                "Parce qu'on remplace les multiplications par des divisions",
            ],
            "answer": 0,
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
