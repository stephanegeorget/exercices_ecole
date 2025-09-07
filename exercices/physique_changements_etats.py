"""Leçon et quiz sur les changements d'état de la matière."""


def main():
    """Présente la leçon puis un quiz corrigé."""
    # Leçon introductive
    print("Changements d'état de la matière\n")
    print("1. Fusion : passage de l'état solide à l'état liquide. \n"
          "   Exemple : la glace qui devient de l'eau." )
    print("2. Solidification : passage du liquide au solide. \n"
          "   Exemple : l'eau qui gèle dans le congélateur.")
    print("3. Vaporisation : passage du liquide au gaz. \n"
          "   Exemple : l'eau qui bout devient de la vapeur.")
    print("4. Condensation : passage du gaz au liquide. \n"
          "   Exemple : la vapeur d'eau qui forme des gouttes sur une vitre froide.")
    print("5. Sublimation : passage direct du solide au gaz sans devenir liquide. \n"
          "   Exemple : la glace sèche qui disparaît en fumée.")
    print("6. Condensation solide : passage direct du gaz au solide. \n"
          "   Exemple : le givre qui se forme sur une fenêtre en hiver.\n")

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
            print("Exact !")
            score += 1
        else:
            print(f"Non, la bonne réponse était {correct + 1}. {correct_text}")

    total = len(questions)
    print(f"\nScore final : {score}/{total}")
    if score == total:
        print("Excellent travail ! Tu maîtrises parfaitement les changements d'état.")
    elif score >= total / 2:
        print("Bravo ! Continue à réviser pour progresser encore.")
    else:
        print("Courage, relis la leçon et essaie à nouveau !")


if __name__ == "__main__":
    main()
