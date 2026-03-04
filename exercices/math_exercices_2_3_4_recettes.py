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
        # Exercice 2 : concert (20 questions, très guidé)
        {
            "question": "[Exercice 2] Dans ce problème, que cherche-t-on à la fin ?",
            "choices": ["Le nombre total de places", "La recette totale en euros", "Le prix moyen d'une place"],
            "answer": 1,
        },
        {
            "question": "[Exercice 2] La catégorie A contient...",
            "choices": ["100 places à 63,50 €", "1 000 places à 42,30 €", "100 places à 42,30 €"],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] La catégorie B contient...",
            "choices": ["1 000 places à 42,30 €", "100 places à 63,50 €", "1 000 places à 63,50 €"],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] Pour calculer une recette, on fait en général...",
            "choices": ["quantité × prix unitaire", "quantité + prix unitaire", "quantité - prix unitaire"],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] Pourquoi ne fait-on pas 100 + 63,50 pour la catégorie A ?",
            "choices": [
                "Parce qu'on additionnerait des grandeurs différentes (places et euros)",
                "Parce que 100 est pair",
                "Parce qu'il faut toujours une division",
            ],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] L'écriture correcte de la recette A est...",
            "choices": ["100 × 63,50", "100 + 63,50", "63,50 ÷ 100"],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] Multiplier par 100 revient à déplacer la virgule de...",
            "choices": ["1 rang à droite", "2 rangs à droite", "3 rangs à droite"],
            "answer": 1,
        },
        {
            "question": "[Exercice 2] 63,50 × 100 =",
            "choices": ["635", "6 350", "63 500"],
            "answer": 1,
        },
        {
            "question": "[Exercice 2] Recette de la catégorie A :",
            "choices": ["6 350 €", "635 €", "63 500 €"],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] L'écriture correcte de la recette B est...",
            "choices": ["1 000 × 42,30", "1 000 + 42,30", "42,30 ÷ 1 000"],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] Multiplier par 1 000 revient à déplacer la virgule de...",
            "choices": ["1 rang", "2 rangs", "3 rangs"],
            "answer": 2,
        },
        {
            "question": "[Exercice 2] 42,30 × 1 000 =",
            "choices": ["4 230", "42 300", "423 000"],
            "answer": 1,
        },
        {
            "question": "[Exercice 2] Recette de la catégorie B :",
            "choices": ["4 230 €", "42 300 €", "423 000 €"],
            "answer": 1,
        },
        {
            "question": "[Exercice 2] Avant l'addition finale, on a donc...",
            "choices": ["6 350 € et 42 300 €", "635 € et 4 230 €", "63 500 € et 423 000 €"],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] Pourquoi additionne-t-on ensuite ?",
            "choices": [
                "Parce qu'on regroupe deux recettes partielles en une recette totale",
                "Parce qu'on veut le prix d'une place",
                "Parce qu'on change d'unité",
            ],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] 6 350 + 42 300 =",
            "choices": ["48 650", "49 650", "50 650"],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] La recette totale du concert est donc...",
            "choices": ["48 650 €", "49 650 €", "50 650 €"],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] Vérification rapide : 42,30 € est environ...",
            "choices": ["40 €", "4 €", "400 €"],
            "answer": 0,
        },
        {
            "question": "[Exercice 2] Donc 1 000 places à environ 40 € donnent un ordre de grandeur proche de...",
            "choices": ["4 000 €", "40 000 €", "400 000 €"],
            "answer": 1,
        },
        {
            "question": "[Exercice 2] Cet ordre de grandeur confirme que 42 300 € pour la catégorie B est...",
            "choices": ["cohérent", "impossible", "forcément trop petit"],
            "answer": 0,
        },

        # Exercice 3 : produits en ligne (13 questions)
        {
            "question": "[Exercice 3] Idée générale : multiplier par 10, 100, 1 000 fait bouger la virgule vers...",
            "choices": ["la gauche", "la droite", "nulle part"],
            "answer": 1,
        },
        {
            "question": "[Exercice 3a] Pour 12,753 × 100, la virgule bouge de...",
            "choices": ["1 rang", "2 rangs", "3 rangs"],
            "answer": 1,
        },
        {
            "question": "[Exercice 3a] 12,753 × 100 =",
            "choices": ["127,53", "1 275,3", "12 753"],
            "answer": 1,
        },
        {
            "question": "[Exercice 3b] Pour 0,435 × 1 000, la virgule bouge de...",
            "choices": ["1 rang", "2 rangs", "3 rangs"],
            "answer": 2,
        },
        {
            "question": "[Exercice 3b] 0,435 × 1 000 =",
            "choices": ["4,35", "43,5", "435"],
            "answer": 2,
        },
        {
            "question": "[Exercice 3c] Dans 2,714 × 10 × 100, on peut d'abord regrouper 10 × 100 =",
            "choices": ["100", "1 000", "10 000"],
            "answer": 1,
        },
        {
            "question": "[Exercice 3c] Donc 2,714 × 10 × 100 = 2,714 × ...",
            "choices": ["100", "1 000", "10 000"],
            "answer": 1,
        },
        {
            "question": "[Exercice 3c] 2,714 × 1 000 =",
            "choices": ["27,14", "271,4", "2 714"],
            "answer": 2,
        },
        {
            "question": "[Exercice 3d] Dans 14,203 × 100 × 100, 100 × 100 =",
            "choices": ["1 000", "10 000", "100 000"],
            "answer": 1,
        },
        {
            "question": "[Exercice 3d] Donc 14,203 × 100 × 100 = 14,203 × ...",
            "choices": ["1 000", "10 000", "100 000"],
            "answer": 1,
        },
        {
            "question": "[Exercice 3d] 14,203 × 10 000 =",
            "choices": ["14 203", "142 030", "1 420 300"],
            "answer": 1,
        },
        {
            "question": "[Exercice 3] Pourquoi peut-on regrouper les facteurs (10 × 100) ?",
            "choices": [
                "Parce que la multiplication est associative",
                "Parce qu'on change le résultat au hasard",
                "Parce qu'il faut d'abord additionner",
            ],
            "answer": 0,
        },
        {
            "question": "[Exercice 3] Quel résultat est correct pour 12,753 × 100 ?",
            "choices": ["1 275,3", "127,53", "12,753"],
            "answer": 0,
        },

        # Exercice 4 : boutique (13 questions)
        {
            "question": "[Exercice 4] Quelles sont les deux ventes à traiter ?",
            "choices": [
                "1 000 maillots à 87,99 € et 100 équipements à 143,40 €",
                "1 000 équipements à 87,99 € et 100 maillots à 143,40 €",
                "1 000 maillots à 143,40 € et 100 équipements à 87,99 €",
            ],
            "answer": 0,
        },
        {
            "question": "[Exercice 4] Pour les maillots, l'opération correcte est...",
            "choices": ["1 000 × 87,99", "1 000 + 87,99", "87,99 ÷ 1 000"],
            "answer": 0,
        },
        {
            "question": "[Exercice 4] Pourquoi choisit-on la multiplication pour les maillots ?",
            "choices": [
                "Parce qu'on répète 87,99 € un grand nombre de fois",
                "Parce que 87,99 a deux décimales",
                "Parce que 1 000 est pair",
            ],
            "answer": 0,
        },
        {
            "question": "[Exercice 4] 87,99 × 1 000 =",
            "choices": ["8 799", "87 990", "879 900"],
            "answer": 1,
        },
        {
            "question": "[Exercice 4] Recette maillots :",
            "choices": ["8 799 €", "87 990 €", "879 900 €"],
            "answer": 1,
        },
        {
            "question": "[Exercice 4] Pour les équipements, l'opération correcte est...",
            "choices": ["100 × 143,40", "100 + 143,40", "143,40 ÷ 100"],
            "answer": 0,
        },
        {
            "question": "[Exercice 4] 143,40 × 100 =",
            "choices": ["1 434", "14 340", "143 400"],
            "answer": 1,
        },
        {
            "question": "[Exercice 4] Recette équipements :",
            "choices": ["1 434 €", "14 340 €", "143 400 €"],
            "answer": 1,
        },
        {
            "question": "[Exercice 4] Pourquoi additionne-t-on ensuite 87 990 et 14 340 ?",
            "choices": [
                "Parce qu'on veut la recette totale de deux familles de produits",
                "Parce qu'on veut le prix d'un seul produit",
                "Parce qu'il faut toujours additionner après une multiplication",
            ],
            "answer": 0,
        },
        {
            "question": "[Exercice 4] 87 990 + 14 340 =",
            "choices": ["101 330", "102 330", "103 330"],
            "answer": 1,
        },
        {
            "question": "[Exercice 4] Recette totale de la boutique :",
            "choices": ["101 330 €", "102 330 €", "103 330 €"],
            "answer": 1,
        },
        {
            "question": "[Exercice 4] Vérification d'ordre de grandeur : 1 000 × 88 ≈",
            "choices": ["8 800", "88 000", "880 000"],
            "answer": 1,
        },
        {
            "question": "[Exercice 4] Ce contrôle confirme que 87 990 € pour les maillots est...",
            "choices": ["cohérent", "beaucoup trop grand", "forcément nul"],
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
